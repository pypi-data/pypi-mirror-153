#!/usr/bin/env python
#
# core.py - The data import stage
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides the :func:`importData` function, which implements
the data importing stage of the ``funpack`` sequence
"""


import itertools             as it
import functools             as ft
import multiprocessing       as mp
import multiprocessing.dummy as mpd
import                          logging
import                          warnings
import                          collections

import pandas                as pd
import numpy                 as np
import funpack.util          as util
import funpack.custom        as custom
import funpack.merging       as merging
import funpack.datatable     as datatable
import funpack.loadtables    as loadtables
from . import                   filter   # noqa
from . import                   reindex


log = logging.getLogger(__name__)


NUM_ROWS = 10000
"""Default number of rows read at a time by :func:`loadData` - it reads the
data in chunks.
"""


MERGE_AXIS = 'variables'
"""Default merge axis when loading multiple data files - see :func:`mergeData`.
"""


MERGE_STRATEGY = 'intersection'
"""Default merge strategy when loading multiple data files - see
:func:`mergeData`.
"""


MERGE_AXIS_OPTIONS = ['0', 'rows', 'subjects',
                      '1', 'cols', 'columns', 'variables']
"""Values accepted for the ``axis`` option to the :func:`mergeData` function.
"""


MERGE_STRATEGY_OPTIONS = ['naive', 'union', 'intersection', 'inner', 'outer']
"""Values accepted for the ``strategy`` option to the :func:`mergeData`
function.
"""


def importData(fileinfo,
               vartable,
               proctable,
               cattable,
               variables=None,
               colnames=None,
               excludeColnames=None,
               categories=None,
               subjects=None,
               subjectExprs=None,
               exclude=None,
               excludeVariables=None,
               excludeCategories=None,
               trustTypes=False,
               mergeAxis=None,
               mergeStrategy=None,
               indexVisits=False,
               dropNaRows=False,
               njobs=1,
               mgr=None,
               dryrun=False):
    """The data import stage.

    This function does the following:

      1. Figures out which columns to load (using the :func:`.columnsToLoad`
         function).

      2. Loads the data (using :func:`loadFiles`),

      3. Creates and returns a :class:`DataTable`.

    :arg fileinfo:          :class:`.FileInfo` object describing the input
                            file(s).

    :arg vartable:          The data coding table

    :arg proctable:         The processing table

    :arg cattable:          The category table

    :arg variables:         List of variable IDs to import

    :arg colnames:          List of names/glob-style wildcard patterns
                            specifying columns to import.

    :arg excludeColnames:   List of column name suffixes specifying columns
                            to exclude.

    :arg categories:        List of category names/IDs to import

    :arg subjects:          List of subjects to include

    :arg subjectExprs:      List of subject inclusion expressions

    :arg exclude:           List of subjects to exclude

    :arg excludeVariables:  List of variables to exclude

    :arg excludeCategories: List of category names/IDs to exclude

    :arg trustTypes:        If ``True``, it is assumed that columns with a
                            known data type do not contain any bad/unparseable
                            values. This improves performance, but will cause
                            an error if the assumption does not hold.

    :arg mergeAxis:         Merging axis to use when loading multiple data
                            files - see the :func:`mergeData` function.

    :arg mergeStrategy:     Merging strategy to use when loading multiple
                            data files - see the :func:`mergeData` function.

    :arg indexVisits:       Re-arrange the data so that rows are indexed by
                            subject ID and visit, rather than visits being
                            split into separate columns. Only applied to
                            variables which are labelled with Instancing 2.

    :arg dropNaRows:        If ``True``, rows which do not contain data for any
                            columns are not loaded.

    :arg njobs:             Number of processes to use for parallelising tasks.

    :arg mgr:               :class:`multiprocessing.Manager` object for
                            parallelisation

    :arg dryrun:            If ``True`` the data is not loaded.

    :returns:               A tuple containing:

                             - A :class:`DataTable`, which contains references
                               to the data, and the variable and procesing
                               tables.

                             - A list of :class:`.Column` objects that were not
                               loaded from each input file.
    """

    variables, excludevars = filter.restrictVariables(
        cattable, variables, categories, excludeVariables, excludeCategories)

    # Figure out which columns to load
    cols, drop = filter.columnsToLoad(fileinfo,
                                      vartable,
                                      variables,
                                      excludevars,
                                      colnames,
                                      excludeColnames)

    # Load those columns, merging
    # multiple input files.
    if njobs > 1: Pool = mp.Pool
    else:         Pool = mpd.Pool

    with Pool(njobs) as pool:
        data, cols = loadFiles(fileinfo,
                               vartable,
                               cols,
                               subjects=subjects,
                               subjectExprs=subjectExprs,
                               exclude=exclude,
                               mergeAxis=mergeAxis,
                               mergeStrategy=mergeStrategy,
                               indexVisits=indexVisits,
                               dropNaRows=dropNaRows,
                               trustTypes=trustTypes,
                               pool=pool,
                               dryrun=dryrun)
        pool.close()
        pool.join()

    # Re-order the columns according to
    # specified variables, if provided
    if variables is not None:

        # Build a list of all loaded vids -
        # this will include those loaded
        # via the colnames argument
        allvars = variables
        for c in cols:
            if c.vid == 0:
                continue
            if c.vid not in allvars:
                allvars.insert(0, c.vid)

        # organise columns by vid
        # (skipping the index column)
        newcols = collections.defaultdict(list)
        for c in cols:
            if c.vid == 0:
                continue
            newcols[c.vid].append(c)

        # order them by the variable list
        # (including the ID column(s) for
        # the first file)
        cols = list(it.chain([cols[0]], *[newcols[v] for v in allvars]))

        if not dryrun:
            data = data[[c.name for c in cols[1:]]]

    dtable = datatable.DataTable(
        data, cols, vartable, proctable, cattable, njobs, mgr)

    return dtable, drop


def loadFiles(fileinfo,
              vartable,
              columns,
              nrows=None,
              subjects=None,
              subjectExprs=None,
              exclude=None,
              trustTypes=False,
              mergeAxis=None,
              mergeStrategy=None,
              indexVisits=False,
              dropNaRows=False,
              pool=None,
              dryrun=False):
    """Load data from ``datafiles``, using :func:`.mergeDataFrames` if multiple
    files are provided.

    :arg fileinfo:      :class:`.FileInfo` object describing the input file(s).

    :arg vartable:      Variable table

    :arg columns:       Dict of ``{ file : [Column] }`` mappings,
                        defining the columns to load, as returned by
                        :func:`columnsToLoad`.

    :arg nrows:         Number of rows to read at a time. Defaults to
                       :attr:`NUM_ROWS`.

    :arg subjects:      List of subjects to include.

    :arg subjectExprs:  List of subject inclusion expressions

    :arg exclude:       List of subjects to exclude

    :arg trustTypes:    Assume that columns with known data type do not contain
                        any bad/unparseable values.

    :arg mergeAxis:     Merging axis to use when loading multiple data files -
                        see the :func:`mergeDataFrames` function. Defaults to
                        :attr:`MERGE_AXIS`.

    :arg mergeStrategy: Strategy for merging multiple data files - see the
                        :func:`mergeData` function. Defaults to
                        :attr:`MERGE_STRATEGY`.

    :arg indexVisits:   Re-arrange the data so that rows are indexed by subject
                        ID and visit, rather than visits being split into
                        separate columns. Only applied to variables which are
                        labelled with Instancing 2.

    :arg dropNaRows:    If ``True``, rows which do not contain data for any
                        columns are not loaded.

    :arg pool:          ``multiprocessing.Pool`` object for running tasks in
                        parallel.

    :arg dryrun:        If ``True``, the data is not loaded.

    :returns:           A tuple containing:

                         - A ``pandas.DataFrame`` containing the data,
                           or ``None`` if ``dryrun is True``.
                         - A list of :class:`.Column` objects representing the
                           columns that were loaded.
    """

    if mergeStrategy is None: mergeStrategy = MERGE_STRATEGY
    if mergeAxis     is None: mergeAxis     = MERGE_AXIS

    # load the data
    data       = []
    loadedcols = []
    for fname in fileinfo.datafiles:

        toload = columns[        fname]
        loader = fileinfo.loader(fname)
        fdata  = None
        fcols  = None

        if loader is not None:
            log.debug('Loading %s with custom loader %s', fname, loader)
            fdata = custom.runLoader(loader, fname)
            fcols = toload

        else:
            log.debug('Loading %s with pandas', fname)
            fdata, fcols = loadFile(fname,
                                    fileinfo,
                                    vartable,
                                    toload,
                                    nrows=nrows,
                                    subjects=subjects,
                                    subjectExprs=subjectExprs,
                                    exclude=exclude,
                                    indexVisits=indexVisits,
                                    dropNaRows=dropNaRows,
                                    trustTypes=trustTypes,
                                    pool=pool)

        data      .append(fdata)
        loadedcols.append(fcols)

    # Merge data from multiple files
    # into a single dataframe
    data, cols = merging.mergeDataFrames(
        data, loadedcols, mergeAxis, mergeStrategy, dryrun)

    # if a subject list was provided,
    # re-order the data according to
    # that list
    if (not dryrun) and subjects is not None:

        # if exclude/subjectExpr lists were
        # provided, and they overlap with
        # the subjects list, there will be
        # more IDs in the subject list than
        # the dataframe. Fix it.
        if len(data.index) != len(subjects):
            if data.index.nlevels == 1: oldsubjects = data.index
            else:                       oldsubjects = data.index.levels[0]
            subjects = pd.Index(subjects, name=data.index.names[0])
            subjects = subjects.intersection(oldsubjects, sort=False)

        if data.index.nlevels == 1: idx = subjects
        else:                       idx = (subjects, slice(None))

        data = data.loc[idx, :]

    return data, cols


def loadFile(fname,
             fileinfo,
             vartable,
             toload,
             nrows=None,
             subjects=None,
             subjectExprs=None,
             exclude=None,
             indexVisits=False,
             dropNaRows=False,
             trustTypes=False,
             pool=None):
    """Loads data from the specified file. The file is loaded in chunks of
    ``nrows`` rows, using the :func:`loadChunk` file.

    :arg fname:        Path to the data file

    :arg fileinfo:     :class:`.FileInfo` object describing the input file.

    :arg vartable:     Variable table

    :arg toload:       Sequence of :class:`.Column` objects describing the
                       columns that should be loaded, as generated by
                       :func:`columnsToLoad`.

    :arg nrows:        Number of rows to read at a time. Defaults to
                       attr:`NUM_ROWS`.

    :arg subjects:     List of subjects to include.

    :arg subjectExprs: List of subject inclusion expressions

    :arg exclude:      List of subjects to exclude

    :arg indexVisits:  Re-arrange the data so that rows are indexed by subject
                       ID and visit, rather than visits being split into
                       separate columns. Only applied to variables which are
                       labelled with Instancing 2.

    :arg dropNaRows:   If ``True``, rows which do not contain data for any
                       columns are not loaded.

    :arg trustTypes:   Assume that columns with known data type do not contain
                       any bad/unparseable values.

    :arg pool:         ``multiprocessing.Pool`` object for running tasks in
                       parallel.

    :returns:          A tuple containing:

                        - A ``pandas.DataFrame`` containing the data.
                        - A list of :class:`.Column` objects representing the
                          columns that were loaded. Note that this may be
                          different from ``toload``, if ``indexByVisit`` was
                          set.
    """

    ownPool = pool is None
    toload  = list(toload)

    if nrows is None: nrows = NUM_ROWS
    if pool  is None: pool  = mpd.Pool(1)

    # The read_csv function requires the
    # index argument to be specified
    # relative to the usecols argument:
    #
    #   - https://stackoverflow.com/a/45943627
    #   - https://github.com/pandas-dev/pandas/issues/9098
    #   - https://github.com/pandas-dev/pandas/issues/2654
    #
    # So here we make index relative to
    # toload.
    index = fileinfo.index(fname)
    index = [i for i, c in enumerate(toload) if c.index in index]

    # Figure out suitable data types to
    # store the data for each column.
    # pd.read_csv wants the date columns
    # to be specified separately.
    vttypes, dtypes = loadtables.columnTypes(vartable, toload)
    datecols        = [c.name for c, t in zip(toload, vttypes)
                       if t in (util.CTYPES.date, util.CTYPES.time)]

    # If we think there might be bad data
    # in the input (trustTypes is False),
    # only the types for date/time/non-numeric
    # columns are specified during load, and
    # we manually perform numeric conversion
    # after load, via the coerceToNumeric
    # function. This is to avoid pandas.read_csv
    # crashing on bad data - instead, we set bad
    # data to nan.
    if not trustTypes:
        dtypes = {n : t for n, t in dtypes.items()
                  if not np.issubdtype(t, np.number)}

    # input may or may not
    # have a header row
    if fileinfo.header(fname): header = 0
    else:                      header = None

    if indexVisits:
        indexVisits = reindex.genReindexedColumns(toload, vartable)
    else:
        indexVisits = None

    log.debug('Loading %u columns from %s: %s ...',
              len(toload), fname, [c.name for c in toload[:5]])

    # Prepare arguments to
    # the loadChunk function
    allcols  = fileinfo.columns( fname)
    dialect  = fileinfo.dialect( fname)
    encoding = fileinfo.encoding(fname)

    args = {'fname'        : fname,
            'vartable'     : vartable,
            'header'       : header,
            'allcols'      : allcols,
            'toload'       : toload,
            'index'        : index,
            'nrows'        : nrows,
            'subjects'     : subjects,
            'subjectExprs' : subjectExprs,
            'exclude'      : exclude,
            'indexByVisit' : indexVisits,
            'dropNaRows'   : dropNaRows,
            'encoding'     : encoding,
            'trustTypes'   : trustTypes,
            'dtypes'       : dtypes,
            'datecols'     : datecols}

    if dialect == 'whitespace':
        dlargs = {'delim_whitespace' : True}
    else:
        dlargs = {'delimiter'        : dialect.delimiter,
                  'doublequote'      : dialect.doublequote,
                  'escapechar'       : dialect.escapechar,
                  'skipinitialspace' : dialect.skipinitialspace,
                  'quotechar'        : dialect.quotechar,
                  'quoting'          : dialect.quoting,
                  'delim_whitespace' : False}

    args['dlargs'] = dlargs

    # Load chunks of rows separately,
    # so we can parallelise. We do this
    # by passing different offsets to
    # the loadChunk function.
    totalrows = util.wc(fname)
    offsets   = list(range(0, totalrows,  nrows))
    offsets   = [[i, o] for (i, o) in zip(range(len(offsets)), offsets)]

    # just for the log message
    if header:
        totalrows -= 1
    log.debug('Loading %u rows in %u chunks', totalrows, len(offsets))

    func   = ft.partial(loadChunk, **args)
    chunks = pool.starmap(func, offsets)
    fdata  = pd.concat(chunks, axis=0)

    if indexVisits is not None: fcols = indexVisits[0]
    else:                       fcols = toload

    if ownPool:
        pool.close()
        pool.join()

    log.debug('Loaded %i rows from %s', len(fdata), fname)

    return fdata, fcols


def loadChunk(i,
              offset,
              fname,
              vartable,
              header,
              allcols,
              toload,
              index,
              nrows,
              subjects,
              subjectExprs,
              exclude,
              indexByVisit,
              dropNaRows,
              encoding,
              trustTypes,
              dtypes,
              datecols,
              dlargs):
    """Loads a chunk of ``nrows`` from ``fname``, starting at ``offset``.

    :arg i:            Chunk number, just used for logging.

    :arg offset:       Row number to start reading from.

    :arg fname:        Path to the data file

    :arg vartable:     Variable table

    :arg header:       ``True`` if the file has a header row, ``False``
                       otherwise.

    :arg allcols:      Sequence of :class:`.Column` objects describing all
                       columns in the file.

    :arg toload:       Sequence of :class:`.Column` objects describing the
                       columns that should be loaded, as generated by
                       :func:`columnsToLoad`.

    :arg index:        List containing position(s) of index column(s)
                       (starting from 0).

    :arg nrows:        Number of rows to read at a time. Defaults to
                       attr:`NUM_ROWS`.

    :arg subjects:     List of subjects to include.

    :arg subjectExprs: List of subject inclusion expressions

    :arg exclude:      List of subjects to exclude

    :arg indexByVisit: ``None``, or the return value of
                       :func:`generateReindexedColumns`, which will be used
                       to re-arrange the loaded data so it is indexed by
                       visit number, in addition to row ID.

    :arg dropNaRows:   If ``True``, rows which do not contain data for any
                       columns are not loaded.

    :arg encoding:     Character encoding (or sequence of encodings, one
                       for each data file). Defaults to ``latin1``.

    :arg trustTypes:   Assume that columns with known data type do not contain
                       any bad/unparseable values.

    :arg dtypes:       A dict of ``{ column_name : dtype }`` mappings
                       containing a suitable internal data type to use for some
                       columns.

    :arg datecols:     List of column names denoting columns which should be
                       interpreted as dates/times.

    :arg dlargs:       Dict of arguments to pass through to
                       ``pandas.read_csv``.

    :returns:          ``pandas.DataFrame``
    """

    if encoding is None:
        encoding = 'latin1'

    allcolnames = [c.name for c in allcols]
    toloadnames = [c.name for c in toload]

    def shouldLoad(c):
        return c in toloadnames

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', module='pandas.io.parsers')
        warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)

        df = pd.read_csv(fname,
                         header=header,
                         names=allcolnames,
                         index_col=index,
                         dtype=dtypes,
                         usecols=shouldLoad,
                         parse_dates=datecols,
                         infer_datetime_format=True,
                         skiprows=offset,
                         nrows=nrows,
                         encoding=encoding,
                         **dlargs)
        gotrows = len(df)

        # drop NA rows if requested
        if dropNaRows:
            df.dropna(how='all', inplace=True)

        # If a subject/expression/exclude list
        # is provided, filter the rows accordingly
        df = filter.filterSubjects(df, toload, subjects, subjectExprs, exclude)

        log.debug('Processing chunk %i (kept %i / %i rows)',
                  i + 1, len(df), gotrows)

        # re-arrange the data so that visits
        # form part of the index, rather than
        # being stored in separate columns for
        # each variable
        cols = toload
        if indexByVisit is not None:
            df   = reindex.reindexByVisit(df, cols, *indexByVisit)
            cols = indexByVisit[0]

        # If not trustTypes, we manually convert
        # each column to its correct type.
        #
        # We have to do this after load, as
        # pd.read_csv will raise an error if
        # a column that is specified as
        # numeric contains non-numeric data.
        # So we coerce data types after the
        # data has been loaded. This causes
        # non-numeric data to be set to nan.
        if not trustTypes:
            for c in cols:
                if c.vid == 0:
                    continue
                df.loc[:, c.name] = coerceToNumeric(vartable,
                                                    df.loc[:, c.name],
                                                    c)

        return df


def coerceToNumeric(vartable, series, column):
    """Coerces the given column to numeric, if necessary.

    :arg vartable: The variable table

    :arg series:   ``pandas.Series`` containing the data to be coerced.

    :arg column:   :class:`.Column` object representing the column to coerce.

    :returns:      Coerced ``pandas.Series``
    """

    name      = column.name
    dtype     = loadtables.columnTypes(vartable, [column])[1]
    has_dtype = series.dtype
    exp_dtype = dtype.get(name, None)

    if (exp_dtype is not None)             and \
       np.issubdtype(exp_dtype, np.number) and \
       (has_dtype != exp_dtype):

        # We can't force a specific numpy
        # dtype *and* coerce bad values to
        # nan in one step. So we do it in
        # two steps: to_numeric handles
        # coercion to NaN, and astype casts
        # to the exact type.
        s = pd.to_numeric(series, errors='coerce')
        s = s.astype(exp_dtype, copy=False)

        return s

    return series
