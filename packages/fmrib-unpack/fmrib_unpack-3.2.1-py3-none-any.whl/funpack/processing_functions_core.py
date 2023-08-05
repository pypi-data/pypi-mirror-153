#!/usr/bin/env python
#
# processing_functions_core.py - Functions used by processing_functions.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains utility algorithms and functions used by the
:mod:`processing_functions` module.

 .. autosummary::
   :nosignatures:

   isSparse
   naCorrelation
   pairwiseRedundantColumns
   matrixRedundantColumns
   binariseCategorical
   expandCompound
"""


import                          enum
import                          logging
import                          collections
import functools             as ft
import multiprocessing       as mp
import multiprocessing.dummy as mpd

from typing import Optional, Tuple, List, Union, Any

import numpy                 as np
import pandas                as pd
import pandas.api.types      as pdtypes

import funpack.util          as util


log = logging.getLogger(__name__)


def isSparse(
        data    : pd.Series,
        ctype   : Optional[enum.Enum] = None,
        minpres : Optional[float]     = None,
        minstd  : Optional[float]     = None,
        mincat  : Optional[float]     = None,
        maxcat  : Optional[float]     = None,
        abspres : bool                = True,
        abscat  : bool                = True,
        naval   : Optional[Any]       = None
) -> Tuple[bool, Union[str, None], Any]:
    """Returns ``True`` if the given data looks sparse, ``False`` otherwise.

    Used by :func:`.removeIfSparse` - see that function for details.

    By default, the ``minstd`` test is only performed on numeric columns, and
    the ``mincat``/``maxcat`` tests are only performed on integer/categorical
    columns. This behaviour can be overridden by passing in a ``ctype`` of
    ``None``, in which case all speified tests will be performed.

    :arg data:     ``pandas.Series`` containing the data

    :arg ctype:    The series column type (one of the :attr:`.util.CTYPES`
                   values), or ``None`` to disable type-specific logic.

    :returns:      A tuple containing:

                    - ``True`` if the data is sparse, ``False`` otherwise.

                    - If the data is sparse, one of ``'minpres'``,
                      ``'minstd'``, ``mincat``, or ``'maxcat'``, indicating
                      the cause of its sparsity. ``None`` if the data is not
                      sparse.

                    - If the data is sparse, the value of the criteria which
                      caused the data to fail the test.  ``None`` if the data
                      is not sparse.
    """

    if naval is None: presmask = data.notnull()
    else:             presmask = data != naval

    present  = data[presmask]
    ntotal   = len(data)
    npresent = len(present)

    def fixabs(val, isabs, limit=ntotal, repl=npresent):

        # Turn proportion into
        # an absolute count
        if not isabs:
            val = val * limit
            if (val % 1) >= 0.5: val = np.ceil(val)
            else:                val = np.floor(val)

        # ignore the threshold if it is
        # bigger than the total data length
        if limit < val: return repl
        else:           return val

    iscategorical = ctype in (None,
                              util.CTYPES.integer,
                              util.CTYPES.categorical_single,
                              util.CTYPES.categorical_single_non_numeric,
                              util.CTYPES.categorical_multiple,
                              util.CTYPES.categorical_multiple_non_numeric)
    isnumeric     = ctype in (None,
                              util.CTYPES.continuous,
                              util.CTYPES.integer,
                              util.CTYPES.categorical_single,
                              util.CTYPES.categorical_multiple) and \
                    pdtypes.is_numeric_dtype(data)

    # not enough values
    if minpres is not None:
        if npresent < fixabs(minpres, abspres):
            return True, 'minpres', npresent

    # stddev is not large enough (for
    # numerical/categorical types)
    if isnumeric and minstd is not None:
        std = (present - present.mean()).std()
        if std <= minstd:
            return True, 'minstd', std

    # for categorical types
    if iscategorical and ((maxcat is not None) or (mincat is not None)):

        if maxcat is not None:
            maxcat = fixabs(maxcat, abscat, npresent, npresent + 1)
        if mincat is not None:
            mincat = fixabs(mincat, abscat, npresent)

        # mincat - smallest category is too small
        # maxcat - one category is too dominant
        uniqvals   = pd.unique(present)
        uniqcounts = [sum(present == u) for u in uniqvals]

        # Column is empty - force the test to fail
        if len(uniqcounts) == 0:
            if mincat is not None:
                mincat  = 1
                nmincat = 0
            if maxcat is not None:
                maxcat  = 0
                nmaxcat = 0
        else:
            nmincat = min(uniqcounts)
            nmaxcat = max(uniqcounts)

        if mincat is not None:
            if nmincat < mincat:
                return True, 'mincat', nmincat

        if maxcat is not None:
            if nmaxcat >= maxcat:
                return True, 'maxcat', nmaxcat

    return False, None, None


def naCorrelation(
        namask   : np.ndarray,
        nathres  : float,
        nacounts : Optional[np.ndarray] = None
) -> np.ndarray:
    """Compares the missingness correlation of every pair of columns in
    ``namask``.

    :arg namask:   2D ``numpy`` array of shape ``(nsamples, ncolumns)``
                   containing binary missingness classification

    :arg nathres:  Threshold above which column pairs should be classed
                   as correlated.

    :arg nacounts: 1D ``numpy`` array containing the umber of missing values
                   in each column. Calculated if not provided.

    :returns:      A ``(ncolumns, ncolumns)`` boolean ``numpy`` array
                   containing ``True`` for column pairs which exceed
                   ``nathres``, ``False`` otherwise.
    """

    log.debug('Calculating missingness correlation '
              '(%u columns)', namask.shape[1])

    if nacounts is None:
        nacounts = namask.sum(axis=0)

    # must be float32 to take
    # advantage of parallelism
    namask = namask.astype(np.float32)
    nacorr = np.corrcoef(namask.T)
    nacorr = np.abs(nacorr) > nathres

    # columns with no/all missing values
    # will contain invalid correlation
    # values. But we pass them because
    # these results will be combined with
    # a data correlation test.
    flatmask            = (nacounts == 0) | (nacounts == namask.shape[0])
    nacorr[flatmask, :] = True
    nacorr[:, flatmask] = True

    return nacorr


def pairwiseRedundantColumns(
        data      : pd.DataFrame,
        colpairs  : np.ndarray,
        corrthres : float,
        token     : Optional[str] = None
) -> List[Tuple[int, int]]:
    """Identifies redundant columns based on their correlation with each
    other by comparing each pair of columns one by one.

    :arg data:      ``pandas.DataFrame`` containing the data

    :arg colpairs:  ``numpy`` array of shape ``(N, 2)``, containing indices
                    of the column pairs to be evaluated.

    :arg corrthres: Correlation threshold - columns with a correlation greater
                    than this are identified as redundant.

    :arg token:     Identifier string for log messages.

    :returns:       Sequence of tuples of column indices, where each tuple
                    ``(a, b)`` indicates that column ``a`` is redundant with
                    respect to column ``b``.
    """

    if len(colpairs) == 0:
        return []

    if token is None: token = ''
    else:             token = '[{}] '.format(token)

    redundant = {}
    nacounts  = data.isna().sum(axis=0).to_numpy()

    # calculate correlation between column pairs
    for i, (coli, colj) in enumerate(colpairs):

        if i % 1000 == 0:
            log.debug('%sTesting column pair %u / %u',
                      token, i + 1, len(colpairs))

        datai = data.iloc[:, coli]
        dataj = data.iloc[:, colj]
        corr  = np.abs(datai.corr(dataj))

        # i and j are highly correlated -
        # flag the one with more missing
        # values as redundant
        if corr > corrthres:
            if nacounts[coli] > nacounts[colj]: drop, keep = coli, colj
            else:                               drop, keep = colj, coli

            if drop not in redundant:
                log.debug('%sColumn %s is redundant (correlation with %s: %f)',
                          token, data.columns[drop], data.columns[keep], corr)
                redundant[drop] = keep

    return list(redundant.items())


def matrixRedundantColumns(
        data      : pd.DataFrame,
        corrthres : float,
        nathres   : float = None,
        precision : str   = None) -> List[Tuple[int, int]]:
    """Identifies redundant columns based on their correlation with each
    other using dot products to calculate a correlation matrix.

    :arg data:      ``pandas.DataFrame`` containing the data

    :arg corrthres: Correlation threshold - columns with a correlation greater
                    than this are identified as redundant.

    :arg nathres:   Correlation threshold to use for missing values. If
                    provided, columns must have a correlation greater than
                    ``corrthres`` *and* a missing-value correlation greater
                    than ``nathres`` to be identified as redundant.

    :arg precision: ``'double'`` (the default) or ``'single'``, specifying
                    the floating point precision to use. Note that the
                    algorithm used to calculate the correlation values is
                    unstable for data with a range larger than ~10e5, so
                    double precision is used as default.

    :returns:       Sequence of tuples of column indices, where each tuple
                    ``(a, b)`` indicates that column ``a`` is redundant with
                    respect to column ``b``.
    """

    if len(data.columns) < 2:
        return []

    if precision == 'single':
        dtype = np.float32
    elif precision in (None, 'double'):
        dtype = np.float64
    else:
        raise ValueError(f'Invalid precision: {precision}')

    # Keep a copy of the column names for logging.
    # Create a 2D matrix containing all data
    columns = data.columns
    data    = data.to_numpy(dtype=dtype, copy=True)

    namask   = np.isnan(data)
    nacounts = namask.sum(axis=0)

    # missingness correlation
    if nathres is None: nacorr = None
    else:               nacorr = naCorrelation(namask, nathres, nacounts)

    log.debug('Calculating pairwise correlations '
              '(matrix shape: %s)', data.shape)

    # zero out nan elements
    data[namask] = 0

    # p=present elements
    namask  = (~namask).astype(dtype)
    Ap = Bp = namask
    A  = B  = data

    # sum x_i y_i
    xy = A.T @ B

    # number of items defined both in x and y
    n  = Ap.T @ Bp

    # mean values in x, calculated across items defined both in x and y
    # mean values in y, calculated across items defined both in x and y
    mx = (A.T @ Bp) / n
    my = (Ap.T @ B) / n

    # sum x^2_i, calculated across items defined both in x and y
    # sum y^2_i, calculated across items defined both in x and y
    x2 = (A * A).T @ Bp
    y2 = Ap.T @ (B * B)

    # sx, sy - standard deviations
    # sx = sqrt(x2 - n .* (mx.^2));
    # sy = sqrt(y2 - n .* (my.^2));
    sx         = x2 - n * (mx ** 2)
    sx[sx < 0] = 0
    sx         = np.sqrt(sx)

    sy         = y2 - n * (my ** 2)
    sy[sy < 0] = 0
    sy         = np.sqrt(sy)

    # correlation coefficient
    coef = (xy - n * mx * my) / (sx * sy)

    # ignore nans/infs, binarise. Keep a copy
    # of the raw correlations for logging.
    rawcoef                  = coef
    coef[~np.isfinite(coef)] = 0
    coef                     = np.abs(coef) > corrthres

    # columns must have a correlation greater than
    # corrthres and a missing-value correlation greater
    # than nathres to be identified as redundant.
    if nacorr is not None:
        coef = coef & nacorr

    # generate indices of correlated column
    # pairs; we only need to consider one half
    # of the triangle
    coef     = np.triu(coef, k=1)
    colpairs = np.vstack(np.where(coef))

    # for each correlated pair, we flag the
    # one with more missing values as redundant
    def correlatedPairs(coli, colj):
        if nacounts[coli] > nacounts[colj]: drop, keep = coli, colj
        else:                               drop, keep = colj, coli

        # coef is only the upper triangle
        if coli <= colj: corr = rawcoef[coli, colj]
        else:            corr = rawcoef[colj, coli]

        log.debug('Column %s is redundant (correlation with %s: %0.6f)',
                  columns[drop], columns[keep], corr)

        return drop, keep

    # Generate a sequence of pairs, where the first
    # element is the column to drop, and the second
    # element is the column it is redundant w.r.t.
    correlatedPairs = np.vectorize(correlatedPairs, [np.uint32, np.uint32])
    colsa, colsb    = correlatedPairs(colpairs[0], colpairs[1])

    if len(colsa) == 0:
        return []

    # Return only one pair for each column
    # that is to be dropped (the first
    # pair in the natural column ordering).
    idxs      = np.unique(colsa, return_index=True)[1]
    colsa     = colsa[idxs]
    colsb     = colsb[idxs]

    return list(zip(colsa, colsb))


def binariseCategorical(
        data    : pd.DataFrame,
        minpres : Optional[int]          = None,
        take    : Optional[pd.DataFrame] = None,
        token   : Optional[str]          = None,
        njobs   : Optional[int]          = None
) -> Tuple[np.ndarray, np.ndarray]:
    """Takes one or more columns containing categorical data,, and generates a
    new set of binary columns (as ``np.uint8``), one for each unique
    categorical value, containing ``1`` in rows where the value was present,
    ``0`` otherwise.

    :arg data:    A ``pandas.DataFrame`` containing the input columns

    :arg minpres: Optional threshold - values with less than this number of
                  occurrences will not be included in the output

    :arg take:    Optional ``pandas.DataFrame`` containing values to use in
                  the output. Instead of using binary ``0``/``1`` values,
                  rows where a unique value is present will be populated with
                  the corresponding value from ``take``, and rows where a
                  unique value is not present will be populated with
                  ``np.nan``. Must contain the same number of columns (and
                  rows) as ``data``.

    :arg token:   Unique token to identify this function call, to make it
                  re-entrant (in case multiple calls are made in a parallel
                  execution environment).

    :arg njobs:   Number of jobs to parallelise tasks with - the
                  :func:`generateBinaryColumns` function is called in parallel
                  for different blocks of unique values.

    :returns:     A tuple containing:

                   - A ``(nrows, nvalues)`` ``numpy`` array containing the
                     generated binary columns

                   - A 1D ``numpy`` array of length ``nvalues`` containing
                     the unique values that are encoded in the binary columns.
    """

    if njobs is None: njobs = 1
    if njobs < 1:     njobs = 1

    if njobs == 1: Pool = mpd.Pool
    else:          Pool = mp.Pool

    if (take is not None) and take.shape != data.shape:
        takes = take.shape
        datas = data.shape
        takec = take.columns.difference(data.columns)
        datac = data.columns.difference(take.columns)
        raise ValueError('take {} must have same shape as data {}. '
                         'Column difference: {} -- {}'.format(
                             takes, datas, datac, takec))

    if minpres is None:
        minpres = 0

    if token is None: token = ''
    else:             token = '[{}] '.format(token)

    log.debug('%sCounting unique values across %u '
              'columns...', token, len(data.columns))

    cols    = [data[c]      for c in data.columns]
    cols    = [c[c.notna()] for c in cols]
    coluniq = [np.unique(c, return_counts=True) for c in cols]
    uniq    = collections.defaultdict(lambda : 0)

    for coluniq, colcounts in coluniq:
        for val, count in zip(coluniq, colcounts):
            uniq[val] += count

    # drop values with low occurrence
    uniq = [v for v, c in uniq.items() if c >= minpres]
    uniq = list(sorted(uniq))

    if len(uniq) == 0:
        return np.zeros((len(data), 0)), np.zeros((0,))

    log.debug('%sCounted %u unique values [minpres: %u]',
              token, len(uniq), minpres)

    # Prepare inputs for parallelising the
    # binarise using binariseUniqueValues
    data = data.to_numpy()

    # Figure out the type and fill value
    # of the output array. if take is
    # provided, we assume that every
    # column in it has the same dtype
    if take is None:
        dtype = np.uint8
        fill  = 0
    else:
        dtype = take.dtypes[0]
        take  = take.to_numpy()

        if   np.issubdtype(dtype, np.integer):    fill = 0
        elif np.issubdtype(dtype, np.datetime64): fill = np.datetime64('NAT')
        else:                                     fill = np.nan

    # We parallelise binarisation across
    # blocks of unique values - each call
    # to generateBinaryColumns will binarise
    # one block. Only read access is needed
    # for the uniq, data, and take arrays,
    # so they are made available at the
    # module level (and thus accessible to
    # the worker processes in shared parent
    # process memory).
    #
    # Write access is needed for the bindata
    # array (where the result is written),
    # so it is shared as a mp.RawArray.
    #
    # If take is None, bindata is a uint8
    # array; otherwise it is a take.dtype
    # array.  If take has a dtype of
    # np.datetime64, we need a hack, as we
    # can't create a sharedmem array of that
    # type (it is not supported by
    # numpy.ctypeslib.as_ctypes_type). So
    # for datetime, we make bindata uint64,
    # and then cast it back to datetime64
    # afterwards.
    if np.issubdtype(dtype, np.datetime64):
        cdtype = np.uint64
    else:
        cdtype = dtype

    # Shared array to store binarised
    # columns. If not parallelising,
    # we use a regular numpy array
    binshape = (len(data), len(uniq))

    if njobs > 1:
        rawbindata = mp.RawArray(np.ctypeslib.as_ctypes_type(cdtype),
                                 int(np.prod(binshape)))
        bindata    = np.ctypeslib.as_array(rawbindata).reshape(binshape)
    else:
        bindata    = np.empty(binshape, dtype=dtype)

    # make the inputs module-level accessible
    # before creating worker processess. We
    # use a unique token for this invocation
    # in case this function has been called
    # multiple times
    if not hasattr(generateBinaryColumns, 'inputs'):
        generateBinaryColumns.inputs = {}
    generateBinaryColumns.inputs[token] = (uniq, data, bindata, take)

    # create an offset into the uniq
    # list for each worker process
    valsperjob = int(np.ceil(len(uniq) / njobs))
    offsets    = np.arange(0, len(uniq), valsperjob)
    func       = ft.partial(generateBinaryColumns,
                            nvals=valsperjob,
                            fill=fill,
                            token=token)

    try:
        with Pool(njobs) as pool:
            pool.map(func, offsets)
            pool.close()
            pool.join()
    finally:
        generateBinaryColumns.inputs.pop(token)

    # cast the result if necessary
    if dtype != cdtype:
        bindata = bindata.astype(dtype)

    return bindata, uniq


def generateBinaryColumns(offset, nvals, fill, token):
    """Called by :func:`binariseCategorical`. Generates binarised columns for
    a subset of unique values for a data set.

    The following arguments are passed internally from
    :func:`binariseCategorical` to this function:

     - Sequence of unique values
     - Numpy array containing the data
     - Numpy array to store the output
     - Numpy array to take values from

    :arg offset: Offset into the sequence of unique values
    :arg nvals:  Number of unique values to binarise
    :arg fill:   Default value
    :arg token:  Unique token used to retrieve the data for one invocation of
                 this function.
    """

    # get refs to the shared inputs,
    uniq, data, bindata, take = generateBinaryColumns.inputs[token]

    # are all values being binarised in one go?
    allvals = (offset == 0) and (len(uniq) == nvals)

    # don't overflow on the last
    # block of unique values
    if offset + nvals > len(uniq):
        nvals = len(uniq) - offset

    # rather than writing to bindata directly
    # (which could be a mem-mapped file,
    # therefore slow), we write to a smaller
    # in-memory array and then copy afterwards
    # (but not if this function call is
    # binarising all unique values)
    if allvals: binblock = bindata
    else:       binblock = np.empty((len(data), nvals), bindata.dtype)

    binblock[:] = fill

    for i in range(nvals):

        v = uniq[i + offset]

        if (i + offset) % 100 == 0:
            log.debug('%sUnique value %u / %u [%s] ...',
                      token, i + offset + 1, len(uniq), v)

        mask = data == v

        # if take is None, each column is 1
        #  where the subject had an entry
        #  equal to that value, 0 otherwise.
        if take is None:
            binblock[:, i] = mask.any(axis=1)

        # if take is provided, each column
        # contains the value from take where
        # the subject had an entry equal to
        # that value, or nan otherwise.
        # If a subject had multiple entries
        # equal to value, the first
        # corresponding entry from take is
        # used (via this first function)
        else:
            rowmask              = mask.any(axis=1)
            idxs                 = np.argmax(mask, axis=1)
            values               = take[np.arange(take.shape[0]), idxs]
            binblock[rowmask, i] = values[rowmask]

    # copy results to the output array
    if not allvals:
        bindata[:, offset:offset + nvals] = binblock


def expandCompound(data : pd.Series) -> np.ndarray:
    """Takes a ``pandas.Series`` containing sequence data (potentially of
    variable length), and returns a 2D ``numpy`` array containing the parsed
    data.

    The returned array has shape ``(X, Y)``, where ``X`` is the number of rows
    in the data, and ``Y`` is the maximum number of values for any of the
    entries.

    :arg data: ``pandas.Series`` containing the compound data.
    :returns:   2D ``numpy`` array containing expanded data.
    """

    nrows = len(data)
    lens  = data.apply(len).values
    ncols = max(lens)

    # Create a 2D array from
    # rows of different lengths
    #
    # https://stackoverflow.com/a/32043366
    #
    # 2D mask array of shape (nrows, max(lens))
    # which identifies positions to be filled
    mask          = np.arange(ncols) < np.atleast_2d(lens).T
    newdata       = np.full((nrows, ncols), np.nan, dtype=np.float32)
    newdata[mask] = np.concatenate(data.values)

    return newdata
