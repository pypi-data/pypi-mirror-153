#!/usr/bin/env python
#
# exporting.py - Functions for exporting data
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides functions for exporting data to a file. """


import                     logging
import                     collections

import numpy            as np
import pandas.api.types as pdtypes

from . import util
from . import custom


log = logging.getLogger(__name__)


def exportData(dtable, outfile, fileFormat, **kwargs):
    """Export the data contained in ``dtable`` to ``outfile`` using the
    specified ``fileFormat``.

    :arg dtable:        :class:`.DataTable` containing the data to export.

    :arg outfile:       File to export data to.

    :arg fileFormat:    File format to export to - the name of a ``@exporter``
                        plugin.

    All other arguments are passed through to the exporter plugin.
    """

    if dtable.shape[0] == 0 or dtable.shape[1] == 0:
        raise RuntimeError('No data to export (rows: {}, columns: '
                           '{})'.format(*dtable.shape))

    custom.runExporter(fileFormat, dtable, outfile, **kwargs)


def formatColumn(col,
                 dtable,
                 dateFormat,
                 timeFormat,
                 formatters,
                 logmsg=None):
    """Formats the data for the specified column. The ``dtable`` is updated
    in-place.

    :arg col:        :class:`.Column` to format

    :arg dtable:     :class:`.DataTable` containing the data

    :arg dateFormat: Name of formatter to use for date columns.

    :arg timeFormat: Name of formatter to use for time columns.

    :arg formatters: Dict of ``{ [vid|column] : formatter }`` mappings,
                     specifying custom formatters to use for specific
                     variables.

    :arg logmsg:     Message to include in log message.

    :returns:        A reference to ``dtable``.
    """

    if dateFormat is None: dateFormat = 'default'
    if timeFormat is None: timeFormat = 'default'
    if formatters is None: formatters = {}

    if logmsg is None: logmsg = ''
    else:              logmsg = ' [{}]'.format(logmsg)

    vid      = col.basevid
    vartable = dtable.vartable
    series   = dtable[:, col.name]

    # formatters can be specified
    # by VID or by column name
    formatter = formatters.get(vid, None)
    if formatter is None:
        formatter = formatters.get(col.name, None)

    if vid in vartable.index: vtype = vartable['Type'][vid]
    else:                     vtype = None

    # fall back to date/time formatting
    # if relevant for this column
    if formatter is None and pdtypes.is_datetime64_any_dtype(series):
        # use dateFormat if we know the column
        # is a date (and not datetime), otherwise
        # use timeFormat if the column is a
        # datetime, or unknown type.
        if vtype == util.CTYPES.date: formatter = dateFormat
        else:                         formatter = timeFormat

    if formatter is not None:
        log.debug('Formatting column %s%s with %s formatter',
                  col.name, logmsg, formatter)
        series = custom.runFormatter(formatter, dtable, col, series)

    # apply column-specific fill
    # value, if there is one
    if col.fillval is not None:
        series = series.fillna(value=col.fillval)

    # update datatable if any
    # formatting took place
    if (formatter is not None) or (col.fillval is not None):
        dtable[:, col.name] = series

    return dtable


@custom.formatter('default')
def defaultDateTimeFormat(dtable, column, series):
    """Default format converter for date and time columns. """

    if pdtypes.is_datetime64_any_dtype(series):

        # pandas uses the same data type
        # (pandas.Timestamp) for all date/time
        # types. So to distinguish between
        # dates, and full time stamps, we
        # need to look at the biobank type
        vttype = dtable.vartable.loc[column.basevid, 'Type']

        # The biobank "Date" type is just a date
        if vttype == util.CTYPES.date: fmtstr = '%Y-%m-%d'
        else:                          fmtstr = '%Y-%m-%dT%H:%M:%S%z'

        def fmt(val):
            try:
                return val.strftime(fmtstr)
            except Exception:
                return np.nan

        return series.apply(fmt)

    else:
        return series


@custom.formatter('compound')
def formatCompound(dtable, column, series, delim=','):
    """Format a compound (multi-valued) column which is stored in-memory
    as a list or ``numpy`` array.
    """

    if len(series) == 0:
        return series

    sample = series.iloc[0]

    if isinstance(sample, str):
        return series
    if not isinstance(sample, (np.ndarray, collections.abc.Sequence)):
        return series

    def fmt(val):
        return delim.join([str(v) for v in val])

    return series.apply(fmt)


@custom.formatter('escapeString')
def escapeString(dtable, column, series):
    """Encodes every value of ``series`` as a string, with any escape
    characters (``\\n``, ``\\t``, etc) formatted literally. This has the
    effect that the series is coerced to a string type (if not already).
    """
    if len(series) == 0:
        return series

    def fmt(val):
        return str(val).encode('unicode_escape').decode('utf-8')

    return series.apply(fmt)
