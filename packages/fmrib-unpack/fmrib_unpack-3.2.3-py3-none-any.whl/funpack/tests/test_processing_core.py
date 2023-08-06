#!/usr/bin/env python
#
# test_processing_core.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import string
import random
import datetime
import itertools as it
import functools as ft

import pytest

import numpy  as np
import pandas as pd


import funpack.util                      as util
import funpack.processing_functions_core as core


def test_isSparse_minpres():

    size = 100
    actual_present    = [0,  0.01, 0.1, 0.5, 1]
    minpres_threshold = [0,  0.01, 0.1, 0.5, 1]

    for present, threshold in it.product(actual_present, minpres_threshold):

        data     = np.random.random(size)
        expected = present < threshold

        missing = int(round(size - present * size))
        missing = np.random.choice(range(size), missing, replace=False)
        data[missing] = np.nan

        data = pd.Series(data)

        absres  = core.isSparse(
            data, util.CTYPES.continuous, minpres=threshold * size)
        propres = core.isSparse(
            data, util.CTYPES.continuous, minpres=threshold, abspres=False)

        if expected:
            expcause = 'minpres'
            expval   =  size - len(missing)
        else:
            expcause = None
            expval   = None

        assert absres  == (expected, expcause, expval)
        assert propres == (expected, expcause, expval)

    # minpres should be ignored if
    # number of points in data is
    # less than or equal to it
    data = np.random.random(10)
    data[:2] = np.nan

    res = core.isSparse(pd.Series(data),
                         util.CTYPES.continuous,
                         minpres=9)
    assert res == (True, 'minpres', 8)

    res = core.isSparse(pd.Series(data),
                        util.CTYPES.continuous,
                        minpres=10)
    assert res == (True, 'minpres', 8)

    res = core.isSparse(pd.Series(data),
                        util.CTYPES.continuous,
                        minpres=11)
    assert res == (False, None, None)

    res = core.isSparse(pd.Series(data),
                        util.CTYPES.continuous,
                        minpres=100)
    assert res == (False, None, None)


def test_isSparse_minstd():

    actualstds = np.linspace(0, 2, 10)
    minstds    = np.linspace(0, 2, 10)

    size = 500

    for actualstd, minstd in it.product(actualstds, minstds):

        data      = np.random.randn(size) * actualstd
        data      = pd.Series(data)
        actualstd = data.std()
        expected  = actualstd <= minstd

        result = core.isSparse(data, util.CTYPES.continuous,
                               minstd=minstd)
        if expected:
            assert result[:2] == (expected, 'minstd')
            assert np.isclose(result[2], actualstd)


def test_isSparse_maxcat():

    size          = 20
    actualmaxcats = np.arange(1, 21, 2)
    maxcats       = np.arange(1, 21, 2)

    dtypes = [util.CTYPES.integer,
              util.CTYPES.categorical_single,
              util.CTYPES.categorical_multiple]

    # test should only be applied
    # for integer/categoricals
    data = pd.Series(np.arange(size))
    result = core.isSparse(data, util.CTYPES.continuous, maxcat=1)
    assert result == (False, None, None)

    # threshold should be ignored if
    # bigger than size of data set
    data[:] = 123
    result = core.isSparse(data, util.CTYPES.integer, maxcat=25)
    assert result == (False, None, None)

    for actualmaxcat, maxcat in it.product(actualmaxcats, maxcats):

        data = np.arange(size)
        data[:actualmaxcat] = size + 1

        data = pd.Series(data)

        expected = actualmaxcat >= maxcat

        if expected:
            expected = (expected, 'maxcat', actualmaxcat)
        else:
            expected = (expected, None, None)

        for dt in dtypes:

            maxcatprop = maxcat / len(data)

            resultabs  = core.isSparse(data, dt, maxcat=maxcat)
            resultprop = core.isSparse(data, dt, maxcat=maxcatprop,
                                       abscat=False)

            assert resultabs  == expected
            assert resultprop == expected

    # when maxcat is a proportion, test should ignore nans
    data        = np.zeros(100, dtype=np.float)
    data[:40]   = np.nan
    data[40:80] = 1
    data        = pd.Series(data)
    assert core.isSparse(data, None, maxcat=0.5, abscat=False) == \
        (True, 'maxcat', 40)
    assert core.isSparse(data, None, maxcat=0.6, abscat=False) == \
        (True, 'maxcat', 40)
    assert core.isSparse(data, None, maxcat=0.7, abscat=False) == \
        (False, None, None)


def test_isSparse_mincat():

    size          = 100
    actualmincats = np.arange(1, 21, 2)
    mincats       = np.arange(1, 21, 2)

    dtypes = [util.CTYPES.integer,
              util.CTYPES.categorical_single,
              util.CTYPES.categorical_multiple]

    # test should only be applied
    # for integer/categoricals
    data     = np.zeros(size)
    data[:5] = size + 1
    data     = pd.Series(data)
    result   = core.isSparse(data, util.CTYPES.continuous,
                             mincat=2)
    assert result == (False, None, None)

    # threshold should be ignored if
    # bigger than size of data set
    data[:] = size + 1
    result = core.isSparse(data, util.CTYPES.integer, mincat=size + 5)
    assert result == (False, None, None)

    for actualmincat, mincat in it.product(actualmincats, mincats):

        data = np.zeros(size)
        data[:actualmincat] = size + 1

        data = pd.Series(data)

        if actualmincat < mincat:
            expected = (True, 'mincat', actualmincat)
        else:
            expected = (False, None, None)

        for dt in dtypes:

            mincatprop = mincat / len(data)

            resultabs  = core.isSparse(data, dt, mincat=mincat)
            resultprop = core.isSparse(data, dt, mincat=mincatprop,
                                       abscat=False)

            assert resultabs  == expected
            assert resultprop == expected

    # when mincat is a proportion, test should ignore nans
    data        = np.zeros(100, dtype=np.float)
    data[:40]   = np.nan
    data[40:60] = 1
    data        = pd.Series(data)
    assert core.isSparse(data, None, mincat=0.1, abscat=False) == \
        (False, None, None)
    assert core.isSparse(data, None, mincat=0.2, abscat=False) == \
        (False, None, None)
    assert core.isSparse(data, None, mincat=0.3, abscat=False) == \
        (False, None, None)
    assert core.isSparse(data, None, mincat=0.4, abscat=False) == \
        (True, 'mincat', 20)

# https://git.fmrib.ox.ac.uk/fsl/funpack/-/merge_requests/81
def test_isSparse_mincat_maxcat_empty():

    data = np.full(10, np.nan, dtype=np.float32)
    data = pd.Series(data)

    result = core.isSparse(data, util.CTYPES.categorical_single, mincat=2)
    assert result == (True, 'mincat', 0)

    result = core.isSparse(data, util.CTYPES.categorical_single, maxcat=2)
    assert result == (True, 'maxcat', 0)


def test_isSparse_non_numeric():


    data     = list(np.random.randint(1, 10, 100))
    data[50] = 'abcde'
    data[51] = np.nan
    data     = pd.Series(data)
    assert core.isSparse(data, minstd=10) == (False, None, None)

    data = pd.Series(['a', 'a', 'b', 'b', 'b', np.nan, np.nan])
    assert core.isSparse(data, mincat=1) == (False, None, None)
    assert core.isSparse(data, mincat=2) == (False, None, None)
    assert core.isSparse(data, mincat=3) == (True, 'mincat', 2)
    assert core.isSparse(data, maxcat=4) == (False, None, None)
    assert core.isSparse(data, maxcat=3) == (True, 'maxcat', 3)


def test_isSparse_naval():

    data = np.random.randint(1, 10, 100)
    data = pd.Series(data)

    data.iloc[:10] = -1
    assert core.isSparse(data, minpres=89, naval=-1) == (False, None,      None)
    assert core.isSparse(data, minpres=90, naval=-1) == (False, None,      None)
    assert core.isSparse(data, minpres=91, naval=-1) == (True,  'minpres', 90)

    # nan is not missing
    data.iloc[:10] = np.nan
    assert core.isSparse(data, minpres=91, naval=-1) == (False, None, None)

    # non-numeric
    data = random.choices(string.ascii_lowercase, k=100)
    data = pd.Series(data)

    data.iloc[:10] = 'A'
    assert core.isSparse(data, minpres=89, naval='A') == (False, None,      None)
    assert core.isSparse(data, minpres=90, naval='A') == (False, None,      None)
    assert core.isSparse(data, minpres=91, naval='A') == (True,  'minpres', 90)
    data.iloc[:10] = np.nan
    assert core.isSparse(data, minpres=91, naval='A') == (False, None, None)

    # mixed type
    data.iloc[:10] = 0
    assert core.isSparse(data, minpres=91, naval=0) == (True,  'minpres', 90)


def test_isSparse_date():

    data = []
    for i in range(100):
        data.append(datetime.date(2020,
                                  np.random.randint(1, 13),
                                  np.random.randint(1, 29)))

    data = pd.Series(data)

    data.iloc[:10] = np.nan
    assert core.isSparse(data, minpres=89) == (False, None,      None)
    assert core.isSparse(data, minpres=90) == (False, None,      None)
    assert core.isSparse(data, minpres=91) == (True,  'minpres', 90)


def test_naCorrelation():
    size    = 50
    series1 = np.sin(np.linspace(0, np.pi * 6, size))
    series2 = series1 + np.random.random(size)
    series3 = series1 + np.random.random(size)

    # insert some missing values, making
    # sure there are more missing values
    # in series2, and the missingness will
    # be positively correlated
    s1miss = np.random.choice(
        np.arange(size, dtype=np.int), 10, replace=False)
    s2miss = list(s1miss)
    while len(s2miss) < 13:
        idx = np.random.randint(0, size, 1)
        if idx not in s1miss:
            s2miss.append(idx)
    s2miss = np.array(s2miss, dtype=np.int)

    series1[s1miss] = np.nan
    series2[s2miss] = np.nan

    nacorr = np.corrcoef(np.isnan(series1), np.isnan(series2))[0, 1]

    def check(df, nathres, exp):
        got = core.naCorrelation(df.isna(), nathres)
        exp = np.array(exp)
        assert np.all(np.isclose(got, exp))

    df = pd.DataFrame({0 : series1, 1 : series2})
    check(df, nacorr * 1.01, np.eye(2))
    check(df, nacorr * 0.99, [[1, 1], [1, 1]])

    # cols with no missing values
    # should always pass the test
    df = pd.DataFrame({0 : series1, 1 : series2, 2 : series3})
    check(df, nacorr * 1.01, [[1, 0, 1],
                              [0, 1, 1],
                              [1, 1, 1]])
    check(df, nacorr * 0.99, [[1, 1, 1],
                              [1, 1, 1],
                              [1, 1, 1]])


def wrapped_pairwiseRedundantColumns(df, corrthres):
    xs, ys   = np.triu_indices(len(df.columns), k=1)
    colpairs = np.vstack((xs, ys)).T
    return core.pairwiseRedundantColumns(df, colpairs, corrthres)

def test_pairwiseRedundantColumns():
    with np.errstate(divide='ignore'):
        _test_redundantColumns(wrapped_pairwiseRedundantColumns)

def test_matrixRedundantColumns():
    with np.errstate(divide='ignore'):
        _test_redundantColumns(core.matrixRedundantColumns)

def _test_redundantColumns(rcfunc):

    size    = 50
    series1 = np.sin(np.linspace(0, np.pi * 6, size))
    series2 = series1 + np.random.random(size)
    corr = pd.Series(series1).corr(pd.Series(series2))

    data = pd.DataFrame({0 : pd.Series(series1), 1 : pd.Series(series2)})

    assert np.all(rcfunc(data, corr * 1.01) == [])
    # later (naturally ordered) columns will be
    # the ones flagged as redundant, if they
    # have the same number of missing values
    assert np.all(rcfunc(data, corr * 0.99) == [(1, 0)])

    # the column with more missing values
    # should be the one flagged as redundant
    data.loc[0, 0] = np.nan
    corr = pd.Series(data[0]).corr(data[1])
    assert np.all(rcfunc(data, corr * 1.01) == [])
    assert np.all(rcfunc(data, corr * 0.99) == [(0, 1)])
    data.loc[0:2, 1] = np.nan
    corr = pd.Series(data[0]).corr(data[1])
    assert np.all(rcfunc(data, corr * 1.01) == [])
    assert np.all(rcfunc(data, corr * 0.99) == [(1, 0)])


def test_pairwiseRedundantColumns_associative():
    with np.errstate(divide='ignore'):
        _test_redundantColumns_associative(wrapped_pairwiseRedundantColumns)

def test_matrixRedundantColumns_associative():
    with np.errstate(divide='ignore'):
        _test_redundantColumns_associative(core.matrixRedundantColumns)

def _test_redundantColumns_associative(rcfunc):

    # Three columns a, b, and c, where
    # corr(a,b) > corr(a,c) > corr(b,c)
    cov = np.array([[10,  8,  4],
                    [ 8, 10,  2],
                    [ 4,  2, 10]])
    a, b, c = np.random.multivariate_normal([1, 1, 1], cov, 100).T

    # make sure that a is always selected
    # over b and b is always selected over
    # c, i.e. nans(a) < nans(b) < nans(c)
    b[-1]    = np.nan
    c[-2:]   = np.nan
    df       = pd.DataFrame(np.array([a, b, c]).T, columns=['a', 'b', 'c'])

    corrmat  = df.corr()
    abthres  = corrmat.loc['a', 'b']
    acthres  = corrmat.loc['a', 'c']
    bcthres  = corrmat.loc['b', 'c']

    colorder = 'abc'
    if True: # for colorder in it.permutations('abc', 3):
        df = df[list(colorder)]

        a = colorder.index('a')
        b = colorder.index('b')
        c = colorder.index('c')

        # threshold higher than all corrlations
        assert np.all(rcfunc(df,  abthres * 1.05) == [])
        # threshold lower than a+b, higher than others
        assert np.all(rcfunc(df, (abthres + acthres) / 2) == [(b, a)])
        # threshold lower than a+b, a+c, higher than b+c
        assert np.all(rcfunc(df, (acthres + bcthres) / 2) == [(b, a), (c, a)])
        # threshold lower than all - both b and c
        # should be redundant. Depending on column
        # order, c will be redundant w.r.t. a or
        # to b
        if a < b: exp = [(b, a), (c, a)]
        else:     exp = [(b, a), (c, b)]
        assert np.all(sorted(rcfunc(df,  bcthres * 0.95)) == sorted(exp))


# test that pairwise/matrix implementations produce same result
def test_redundantColumns_na():
    for _ in range(10):
        npts, ncols      = 100, 100
        hcols            = ncols // 2
        seed             = np.random.randint(1, 10000000)
        np.random.seed(seed)

        data             = np.random.randn(npts, ncols)
        data[:, :hcols] += data[:, hcols:]
        naprops          = np.random.random(ncols) * 0.75
        namask           = np.random.random((npts, ncols)) < naprops
        data[namask]     = np.nan

        df = pd.DataFrame(data)

        nacorr    = np.corrcoef(namask.T)
        dcorr     = df.corr().to_numpy()
        nathres   = np.abs(nacorr[~np.isclose(nacorr, 1)]).mean()
        corrthres = np.abs(dcorr[ ~np.isclose(dcorr,  1)]).mean()

        with np.errstate(divide='ignore'):
            nacorr   = core.naCorrelation(pd.isna(df), nathres)
            colpairs = np.where(np.triu(nacorr, k=1))
            colpairs = np.vstack(colpairs).T

            pairwise = core.pairwiseRedundantColumns(df, colpairs, corrthres)
            matrix   = core.matrixRedundantColumns(  df, corrthres, nathres)

        nacounts = np.isnan(data).sum(axis=0)
        corrmask = nacorr & (np.abs(dcorr) > corrthres)
        colpairs = np.where(np.triu(corrmask, k=1))
        colpairs = np.vstack(colpairs).T
        exp = {}
        for ci, cj in colpairs:
            if nacounts[ci] > nacounts[cj]: drop, keep = ci, cj
            else:                           drop, keep = cj, ci

            if drop not in exp:
                exp[drop] = keep
        exp = list(exp.items())

        assert np.all(sorted(exp)      == sorted(matrix))
        assert np.all(sorted(pairwise) == sorted(matrix))


def test_redundantColumns_constant_allna():

    seed = np.random.randint(1, 10000000)
    np.random.seed(seed)

    data       = np.random.randint(1, 100, (20, 10)).astype(np.float32)
    data[0, :] = 20
    data[1, :] = 30
    data[2, :] = 40
    data[3, :] = 50
    data[4, :] = np.nan
    data[5, :] = np.nan
    data[6, :] = np.nan
    data[7, :] = np.nan
    data[0, 0] = np.nan
    data[1, 1] = np.nan
    data[4, 2] = 7
    data[5, 3] = 8
    data[8, 0] = np.nan
    data[9, 1] = np.nan
    df         = pd.DataFrame(data.T)

    with np.errstate(divide='ignore'):
        nacorr   = core.naCorrelation(pd.isna(df), 0.1)
        colpairs = np.where(np.triu(nacorr, k=1))
        colpairs = np.vstack(colpairs).T
        pairwise = core.pairwiseRedundantColumns(df, colpairs, 0.2)
        matrix   = core.matrixRedundantColumns(  df, 0.2, 0.1)

    pairwise = np.array(sorted(pairwise))
    matrix   = np.array(sorted(matrix))
    assert np.all(pairwise == matrix)


def test_binariseCategorical():

    nvals = 100
    ncols = 100
    nrows = 1000
    data = np.random.randint(1, nvals + 1, (nrows, ncols))
    cols = {str(i + 1) : data[:, i] for i in range(ncols)}
    df   = pd.DataFrame(cols)

    bindata, uniq = core.binariseCategorical(df)

    assert sorted(uniq) == sorted(np.unique(data))

    for i, v in enumerate(uniq):
        exp = np.any(data == v, axis=1)
        assert np.all(bindata[:, i] == exp)

    data[data == 5] = 6
    data[:10, 0] = 5
    cols = {str(i + 1) : data[:, i] for i in range(ncols)}
    df   = pd.DataFrame(cols)

    bindata, uniq = core.binariseCategorical(df, minpres=11)

    assert sorted(uniq) == sorted(set(range(1, nvals + 1)).difference([5]))

    for i, v in enumerate(uniq):
        exp = np.any(data == v, axis=1)
        assert np.all(bindata[:, i] == exp)


def test_binariseCategorical_missing():

    data = np.full((50, 5), np.nan)

    for i in range(data.shape[1]):
        namask = np.random.random(data.shape[0]) < 0.1
        data[~namask, i] = np.random.randint(1, 10, (~namask).sum())

    expuniq = list(sorted(np.unique(data[~np.isnan(data)])))

    expdata = np.zeros((data.shape[0], len(expuniq)))

    for i, v in enumerate(expuniq):
        expdata[:, i] = np.any(data == v, axis=1)

    cols = {str(i + 1) : data[:, i] for i in range(data.shape[1])}
    df   = pd.DataFrame(cols)

    gotdata, gotuniq = core.binariseCategorical(df)
    assert np.all(gotuniq == expuniq)
    assert np.all(gotdata == expdata)


def test_binariseCategorical_take():

    nvals = 100
    ncols = 100
    nrows = 1000

    data = np.full((nrows, ncols), np.nan)
    aux  = np.full((nrows, ncols), np.nan)

    for i in range(data.shape[1]):
        namask = np.random.random(data.shape[0]) < 0.7
        data[~namask, i] = np.random.randint(1, nvals + 1, (~namask).sum())

    mask      = np.isfinite(data)
    aux[mask] = np.random.randint(1, 100, data.shape)[mask]

    expuniq = list(sorted(np.unique(data[~np.isnan(data)])))

    expdata = np.full((data.shape[0], len(expuniq)), np.nan)

    for i, v in enumerate(expuniq):
        rows, cols = np.where(data == v)
        for r in range(data.shape[0]):
            if r not in rows:
                continue
            c = cols[np.where(rows == r)[0][0]]
            expdata[r, i] = aux[r, c]

    cols = {str(i + 1) : data[:, i] for i in range(data.shape[1])}
    df   = pd.DataFrame(cols)

    cols = {str(i + 1) : aux[:, i] for i in range(aux.shape[1])}
    adf  = pd.DataFrame(cols)

    gotdata, gotuniq = core.binariseCategorical(df, take=adf)

    gotna = pd.isnull(gotdata)
    expna = pd.isnull(expdata)

    assert np.all(gotuniq         == expuniq)
    assert np.all(gotna           == expna)
    assert np.all(gotdata[~gotna] == expdata[~expna])


def test_binariseCategorical_take_error():

    data = pd.DataFrame(np.random.randint(1, 10, (100, 10)))
    take = pd.DataFrame(np.random.randint(1, 10, (100, 9)))

    with pytest.raises(ValueError):
        core.binariseCategorical(data, take=take)


def test_binariseCategorical_parallel():

    nrows = 10000
    ncols = 100
    nvals = 500
    data = np.random.randint(1, nvals + 1, (nrows, ncols))
    cols = {str(i + 1) : data[:, i] for i in range(ncols)}
    df   = pd.DataFrame(cols)

    seqbindata, sequniq = core.binariseCategorical(df)
    parbindata, paruniq = core.binariseCategorical(df, njobs=6)

    assert np.all(seqbindata == parbindata)
    assert np.all(sequniq == paruniq)

    aux  = np.random.randint(nvals, nvals + 500, (nrows, ncols))
    cols = {str(i + 1) : aux[:, i] for i in range(aux.shape[1])}
    adf  = pd.DataFrame(cols)

    seqbindata, sequniq = core.binariseCategorical(df, take=adf)
    parbindata, paruniq = core.binariseCategorical(df, take=adf, njobs=6)

    assert np.all(seqbindata == parbindata)
    assert np.all(sequniq == paruniq)


def test_binariseCategorical_datetime():
    nrows = 5
    ncols = 10
    nvals = 10
    data = np.random.randint(1, nvals + 1, (nrows, ncols))
    cols = {str(i + 1) : data[:, i] for i in range(ncols)}
    df   = pd.DataFrame(cols)

    aux  = np.random.randint(100, 1000000, (nrows, ncols),
                             dtype=np.uint64).astype('<M8[s]')
    cols = {str(i + 1) : aux[:, i] for i in range(ncols)}
    adf  = pd.DataFrame(cols)

    seqbindata, sequniq = core.binariseCategorical(df, take=adf)
    parbindata, paruniq = core.binariseCategorical(df, take=adf, njobs=6)

    expuniq = list(sorted(np.unique(data)))
    expdata = np.full((data.shape[0], len(expuniq)), np.nan, '<M8[s]')

    for i, v in enumerate(expuniq):
        rows, cols = np.where(data == v)
        for r in range(data.shape[0]):
            if r not in rows:
                continue
            c = cols[np.where(rows == r)[0][0]]
            expdata[r, i] = aux[r, c]

    expnan = np.isnan(expdata)

    assert np.all(sequniq              == expuniq)
    assert np.all(paruniq              == expuniq)
    assert np.all(np.isnan(seqbindata) == expnan)
    assert np.all(np.isnan(parbindata) == expnan)
    assert np.all(expdata[~expnan]     == seqbindata[~expnan])
    assert np.all(expdata[~expnan]     == parbindata[~expnan])


# https://git.fmrib.ox.ac.uk/fsl/funpack/-/merge_requests/81
def test_binariseCategorical_empty():

    data = np.full(10, np.nan, dtype=np.float32)
    data = pd.DataFrame(data)

    columns, values = core.binariseCategorical(data)

    assert columns.shape[1] == 0
    assert len(values)      == 0


def test_expandCompound():

    data = []

    for i in range(20):
        rlen = np.random.randint(1, 20)
        row = np.random.randint(1, 100, rlen)
        data.append(row)

    exp = np.full((20, max(map(len, data))), np.nan)

    for i in range(20):
        exp[i, :len(data[i])] = data[i]

    series = pd.Series(data)

    got = core.expandCompound(series)

    expna = np.isnan(exp)
    gotna = np.isnan(got)

    assert np.all(     expna  ==      gotna)
    assert np.all(exp[~expna] == got[~gotna])
