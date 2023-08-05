#!/usr/bin/env python
#
# exporting_hdf5.py - Export data to HDF5 files
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains functions for exporting data to HDF5 files. """


import logging

import                     h5py
import numpy            as np
import pandas           as pd
import pandas.api.types as pdtypes

from . import custom
from . import exporting


log = logging.getLogger(__name__)


HDF5_KEY = 'funpack'
"""Default group key to use when exporting to a HDF5 file. """


HDF5_STYLES = ['pandas', 'funpack']
"""Available styles to use when saving to HDF5, specified via the ``style``
argument passed to the :func:`exportHDF5` function.
"""


HDF5_STYLE = 'pandas'
"""Default style to use when exporting to a HDF5 file. """


@custom.exporter('hdf5')
def exportHDF5(dtable,
               outfile,
               key=None,
               style=None,
               dropNaRows=False,
               dateFormat=None,
               timeFormat=None,
               formatters=None,
               **kwargs):
    """Export data to a HDF5 file.

    The ``style`` argument determins the internal format of the resulting HDF5
    file. Available styles are ``'pandas'`` and ``'funpack'`` - see the
    :func:`exportPandasStyle` and :func:`exportFunpackStyle` functions
    for details.

    .. note:: Both functions assume that every column in ``dtable`` has either
              numeric or string type. Storage of other types is not supported,
              and columns with an unsupported type will not be exported.

    :arg dtable:     :class:`.DataTable` containing the data

    :arg outfile:    File to output to

    :arg key:        Name to give the HDF5 group. Defaults to :attr:`HDF5_KEY`.

    :arg style:      HDF5 style to use (see above). Defaults to
                     :attr:`HDF5_STYLE`.

    :arg dropNaRows: If ``True``, rows which do not contain data for any
                     columns are not exported.

    :arg dateFormat: Name of formatter to use for date columns.

    :arg timeFormat: Name of formatter to use for time columns.

    :arg formatters: Dict of ``{ [vid|column] : formatter }`` mappings,
                     specifying custom formatters to use for specific
                     variables.
    """

    if key   is None: key   = HDF5_KEY
    if style is None: style = HDF5_STYLE

    if style not in HDF5_STYLES:
        raise ValueError('Unrecognised HDF5 style: {}'.format(style))

    # drop non-[numeric/string] types
    cols = []
    for col in dtable.dataColumns:

        exporting.formatColumn(col,
                               dtable,
                               dateFormat=dateFormat,
                               timeFormat=timeFormat,
                               formatters=formatters)

        series = dtable[:, col.name]
        if pdtypes.is_numeric_dtype(series) or \
           pdtypes.is_string_dtype( series):
            cols.append(col)
        else:
            log.warning('Column %s will not be exported to %s - only '
                        'numeric/string columns can be exported to HDF5.',
                        col.name, outfile)

    if dropNaRows: rows = dtable[:, :].notna().any('columns')
    else:          rows = None

    dtable = dtable.subtable(cols, rows)

    if style == 'pandas':
        exportPandasStyle(dtable,
                          outfile,
                          key=key,
                          **kwargs)

    elif style == 'funpack':
        exportFunpackStyle(dtable,
                           outfile,
                           key=key,
                           **kwargs)


def exportPandasStyle(dtable,
                      outfile,
                      key,
                      numRows=None,
                      **kwargs):
    """Save the data to a ``pandas``-style HDF5 file.

    The entire data frame is saved using the ``pandas.to_hdf`` function,
    under a single group named according to the ``key`` argument.

    The data can be reloaded via the ``pandas.read_hdf`` function.

    :arg dtable:     :class:`.DataTable` containing the data

    :arg outfile:    File to output to

    :arg key:        Name to give the HDF5 group.

    :arg numRows:    Number of rows to write at time (only used for
                     ``pandas``-style files).
    """

    if numRows is None:
        numRows = len(dtable)

    with pd.HDFStore(outfile, 'w') as s:

        index   = dtable.index
        nchunks = int(np.ceil(len(index) / numRows))

        log.info('Writing %u columns in %u chunk(s) to %s ...',
                 len(dtable.allColumns), nchunks, outfile)

        for chunki in range(nchunks):
            cstart  = chunki * numRows
            cend    = cstart + numRows
            cidxs   = index[cstart:cend]
            towrite = dtable[cidxs, :]

            if chunki == 0: s.put(   key, towrite, format='table')
            else:           s.append(key, towrite, format='table')


def exportFunpackStyle(dtable, outfile, key, **kwargs):
    """Save the data to a ``funpack``-style HDF5 file.

    Each column is saved as a separate data set, and named according to the
    column name. All columns are saved under a single group named according to
    the ``key`` argument.

    :arg dtable:  :class:`.DataTable` containing the data

    :arg outfile: File to output to

    :arg key:     Name to give the HDF5 group.
    """

    log.info('Writing %u columns in to %s ...',
             len(dtable.allColumns), outfile)

    with h5py.File(outfile, 'w') as f:

        name = '/'.join((key, dtable.index.name))
        data = np.asarray(dtable.index)
        f.create_dataset(name, data=data)

        for col in dtable.dataColumns:

            name   = '/'.join((key, col.name))
            series = np.asarray(dtable[:, col.name])

            if np.issubdtype(series.dtype, np.number):
                dtype = None
            else:
                dtype = h5py.special_dtype(vlen=str)

            f.create_dataset(name, dtype=dtype, data=series)


def importFunpackStyle(infile, idcol, key=None):
    """Load a ``funpack``-style HDF5 file as a ``pandas.DataFrame``.
    See the :func:`exportFunpackStyle` function.

    :arg infile: File to load

    :arg idocol: Name of index column.

    :arg key:    HDF5 group key containing the data. If not provided, and
                 the file only has one group, that group is assumed to
                 contain the data. If not provided, and the file contains
                 more than one group, a :exc:`ValueError` is raised.

    :returns:    A ``pandas.DataFrame`` containing the data.
    """

    df = pd.DataFrame()

    with h5py.File(infile, 'r') as f:

        if key is None and len(f.keys()) != 1:
            raise ValueError('Key not provided, and file contains '
                             'multiple keys: {}'.format(infile))

        if key is None:
            key = f.keys()[0]

        cols = list(f[key].keys())

        if idcol not in cols:
            raise ValueError('Index column not in file: {}'.format(idcol))

        for colname in cols:
            df[colname] = np.asarray(f['/'.join((key, colname))])

    return df.set_index(idcol)
