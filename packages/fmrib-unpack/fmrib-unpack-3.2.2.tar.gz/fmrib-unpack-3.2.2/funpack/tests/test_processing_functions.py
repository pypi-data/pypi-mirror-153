#!/usr/bin/env python
#
# test_processing_functions.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import string
import random
import textwrap as tw
import multiprocessing as mp

import io

from unittest import mock

import numpy  as np
import pandas as pd

from pandas.testing import assert_frame_equal

import funpack.importing            as importing
import funpack.fileinfo             as fileinfo
import funpack.util                 as util
import funpack.processing_functions as pfns

from . import (gen_DataTable,
               gen_DataTableFromDataFrame,
               tempdir,
               patch_logging,
               gen_tables)


@patch_logging
def test_removeIfSparse():

    sparse = np.random.random(100)
    good   = np.random.random(100)

    sparse[:50] = np.nan

    dtable = gen_DataTable([good, sparse])
    remove = pfns.removeIfSparse(dtable, [1, 2], minpres=60)
    remove = [r.name for r in remove]
    assert remove == ['2-0.0']

    dtable = gen_DataTable([good, sparse])
    remove = pfns.removeIfSparse(dtable, [1, 2], minpres=40)
    remove = [r.name for r in remove]
    assert remove == []


@patch_logging
def test_removeIfSparse_typed():

    mincat = np.zeros(100)
    good   = np.zeros(100)
    maxcat = np.zeros(100)

    mincat[:5]  = 1
    maxcat[:95] = 1
    good[  :50] = 1

    dtable = gen_DataTable([mincat, good, maxcat])
    dtable.vartable.loc[1, 'Type'] = util.CTYPES.categorical_single
    dtable.vartable.loc[2, 'Type'] = util.CTYPES.categorical_single
    dtable.vartable.loc[3, 'Type'] = util.CTYPES.categorical_single
    remove = pfns.removeIfSparse(dtable, [1, 2, 3], mincat=10, maxcat=90)
    remove = [r.name for r in remove]
    assert remove == ['1-0.0', '3-0.0']

    dtable.vartable.loc[1, 'Type'] = util.CTYPES.unknown
    dtable.vartable.loc[2, 'Type'] = util.CTYPES.unknown
    dtable.vartable.loc[3, 'Type'] = util.CTYPES.unknown
    remove = pfns.removeIfSparse(dtable, [1, 2, 3], mincat=10, maxcat=90)
    remove = [r.name for r in remove]
    assert remove == []

    remove = pfns.removeIfSparse(dtable, [1, 2, 3], mincat=10, maxcat=90,
                                 ignoreType=True)
    remove = [r.name for r in remove]
    assert remove == ['1-0.0', '3-0.0']


@patch_logging
def test_removeIfRedundant():

    series1 = np.sin(np.linspace(0, np.pi * 6, 100))
    series2 = series1 + np.random.random(100)
    series3 = ['abc'] * 100
    corr    = pd.Series(series1).corr(pd.Series(series2))

    dtable = gen_DataTable([series1, series2, series3])
    remove = pfns.removeIfRedundant(dtable, [1, 2, 3], corr * 0.9)
    remove = [r.name for r in remove]
    assert remove == ['2-0.0']

    dtable = gen_DataTable([series1, series2, series3])
    remove = pfns.removeIfRedundant(dtable, [1, 2, 3], corr * 1.1)
    remove = [r.name for r in remove]
    assert remove == []


@patch_logging
def test_removeIfRedundant_nathres():

    size    = 50
    series1 = np.sin(np.linspace(0, np.pi * 6, size))
    series2 = series1 + np.random.random(size)

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

    corr   = pd.Series(series1).corr(pd.Series(series2))
    nacorr = np.corrcoef(np.isnan(series1), np.isnan(series2))[0, 1]

    vids   = [1, 2]
    dtable = gen_DataTable([series1, series2])

    def asrt(res, exp):
        assert [int(c.name.split('-')[0]) for c in res] == exp

    asrt(pfns.removeIfRedundant(dtable, vids, corr * 1.01), [])
    asrt(pfns.removeIfRedundant(dtable, vids, corr * 0.99), [2])

    # both present and missing values must
    # be above the threshold for the column
    # to be considered redundant
    asrt(pfns.removeIfRedundant(dtable, vids, corr * 0.99, nacorr * 0.99), [2])
    asrt(pfns.removeIfRedundant(dtable, vids, corr * 1.01, nacorr * 0.99), [])
    asrt(pfns.removeIfRedundant(dtable, vids, corr * 0.99, nacorr * 1.01), [])
    asrt(pfns.removeIfRedundant(dtable, vids, corr * 1.01, nacorr * 1.01), [])

    # the column with more missing values
    # should be the one flagged as redundant
    dtable = gen_DataTable([series2, series1])
    asrt(pfns.removeIfRedundant(dtable, vids, corr * 1.01)               , [])
    asrt(pfns.removeIfRedundant(dtable, vids, corr * 0.99)               , [1])
    asrt(pfns.removeIfRedundant(dtable, vids, corr * 0.99, nacorr * 0.99), [1])
    asrt(pfns.removeIfRedundant(dtable, vids, corr * 1.01, nacorr * 0.99), [])
    asrt(pfns.removeIfRedundant(dtable, vids, corr * 0.99, nacorr * 1.01), [])
    asrt(pfns.removeIfRedundant(dtable, vids, corr * 1.01, nacorr * 1.01), [])




@patch_logging
def test_removeIfRedundant_parallel():

    for _ in range(10):
        npts, ncols      = 50, 500
        hcols            = ncols // 2
        seed             = np.random.randint(1, 10000000)

        np.random.seed(seed)

        data             = np.random.randn(npts, ncols)
        data[:, :hcols] += data[:, hcols:]
        naprops          = np.random.random(ncols) * 0.75

        # make sure some cols are all present or all missing
        naprops[:5]  = 1
        naprops[-5:] = 0

        namask           = np.random.random((npts, ncols)) < naprops
        data[namask]     = np.nan

        df = pd.DataFrame(data)

        nacorr    = np.corrcoef(namask.T)
        dcorr     = df.corr().to_numpy()
        nathres   = np.abs(nacorr[~np.isclose(nacorr, 1)]).mean()
        corrthres = np.abs(dcorr[ ~np.isclose(dcorr,  1)]).mean()

        pardt  = gen_DataTableFromDataFrame(df, njobs=8)
        seqdt  = gen_DataTableFromDataFrame(df)
        vids   = range(1, ncols + 1)

        parrem = pfns.removeIfRedundant(pardt, vids, corrthres, nathres, pairwise=True)
        seqrem = pfns.removeIfRedundant(seqdt, vids, corrthres, nathres, pairwise=True)

        parrem = sorted(parrem, key=lambda c: c.vid)
        seqrem = sorted(seqrem, key=lambda c: c.vid)

        assert parrem == seqrem


@patch_logging
def test_removeIfRedundant_skipUnknowns():
    series1 = np.sin(np.linspace(0, np.pi * 6, 100))
    series2 = series1 + np.random.random(100)
    series3 = series2

    corr    = pd.Series(series1).corr(pd.Series(series2))
    dtable  = gen_DataTable([series1, series2, series3])
    # 1 will be in uncategorised
    dtable.cattable['some category'] = [2, 3]
    remove = pfns.removeIfRedundant(dtable, [1, 2, 3], corr * 0.9)
    remove = [r.name for r in remove]
    assert remove == ['2-0.0', '3-0.0']

    remove = pfns.removeIfRedundant(dtable, [1, 2, 3], corr * 0.9,
                                    skipUnknowns=True)
    remove = [r.name for r in remove]
    assert remove == []


@patch_logging
def test_binariseCateorical():

    data = np.random.randint(1, 10, (50, 14))
    data[:, 0] = np.arange(1, 51)
    cols = ['eid',
            '1-0.0', '1-1.0',
            '2-0.0', '2-1.0', '2-2.0',
            '3-0.0',
            '4-0.0', '4-0.1', '4-0.2',
            '5-0.0', '5-0.1', '5-1.0', '5-1.1']

    vids  = list(range(1, 6))
    didxs = list(range(1, 14))

    with tempdir():
        np.savetxt('data.txt', data, delimiter=',', header=','.join(cols))
        vartable, proctable, cattable = gen_tables(range(1, 13))[:3]
        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo, vartable, proctable, cattable)

        remove, add, addvids, kwargs = pfns.binariseCategorical(
            dt, vids,
            acrossVisits=False,
            acrossInstances=False,
            nameFormat='{vid}-{visit}.{instance}.{value}')

        names = [cols[i] for i in didxs]
        assert [r.name for r in remove] == names

        uniqs = [(i, np.unique(data[:, i])) for i in didxs]
        offset = 0

        for didx, duniqs in uniqs:

            for u in duniqs:

                exp = data[:, didx] == u
                i = offset
                offset += 1

                assert addvids[i] == int(cols[didx].split('-')[0])
                assert add[i].name == '{}.{}'.format(cols[didx], int(u))
                assert (add[i] == exp).all()
                assert kwargs[i]['metadata'] == u

        remove, add, addvids, kwargs = pfns.binariseCategorical(
            dt, vids,
            acrossVisits=True,
            acrossInstances=False,
            nameFormat='{vid}.{instance}.{value}')

        names = []
        offset = 0
        for vid in vids:
            for instance in dt.instances(vid):
                cols = [c.name for c in dt.columns(vid, instance=instance)]
                uniqs = sorted(np.unique(dt[:, cols]))
                names.extend(cols)

                for u in uniqs:
                    exp = np.any(dt[:, cols] == u, axis=1)

                    i = offset
                    offset += 1
                    got = add[i]
                    assert addvids[i] == vid
                    assert got.name == '{}.{}.{}'.format(vid, instance, int(u))
                    assert (got == exp).all()
                    assert kwargs[i]['metadata'] == u
        assert names == [r.name for r in remove]

        remove, add, addvids, kwargs = pfns.binariseCategorical(
            dt, vids,
            acrossVisits=False,
            acrossInstances=True,
            nameFormat='{vid}.{visit}.{value}')

        names = []
        offset = 0
        for vid in vids:
            for visit in dt.visits(vid):
                cols = [c.name for c in dt.columns(vid, visit=visit)]
                uniqs = sorted(np.unique(dt[:, cols]))
                names.extend(cols)

                for u in uniqs:
                    exp = np.any(dt[:, cols] == u, axis=1)

                    i = offset
                    offset += 1
                    got = add[i]
                    assert addvids[i] == vid
                    assert got.name == '{}.{}.{}'.format(vid, visit, int(u))
                    assert (got == exp).all()
                    assert kwargs[i]['metadata'] == u
        assert names == [r.name for r in remove]

        remove, add, addvids, kwargs = pfns.binariseCategorical(
            dt, vids,
            acrossVisits=True,
            acrossInstances=True,
            nameFormat='{vid}.{value}')

        names = []
        offset = 0
        for vid in vids:
            cols = [c.name for c in dt.columns(vid)]
            uniqs = sorted(np.unique(dt[:, cols]))
            names.extend(cols)

            for u in uniqs:
                exp = np.any(dt[:, cols] == u, axis=1)

                i = offset
                offset += 1
                got = add[i]
                assert addvids[i] == vid
                assert got.name == '{}.{}'.format(vid, int(u))
                assert (got == exp).all()
                assert kwargs[i]['metadata'] == u
        assert names == [r.name for r in remove]


@patch_logging
def test_binariseCateorical_no_replace():

    data = np.random.randint(1, 10, (50, 3))
    data[:, 0] = np.arange(1, 51)
    cols = ['eid', '1-0.0', '2-0.0']
    vids  = [1, 2]

    with tempdir():
        np.savetxt('data.txt', data, delimiter=',', header=','.join(cols))
        vartable, proctable, cattable = gen_tables(vids)[:3]
        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo, vartable, proctable, cattable)

        remove, add, addvids, kwargs = pfns.binariseCategorical(
            dt, [1], replace=False, nameFormat='{vid}.{value}')

        uniq = np.unique(data[:, 1])

        assert len(remove)  == 0
        assert len(add)     == len(uniq)
        assert len(addvids) == len(uniq)
        meta = [kw['metadata'] for kw in kwargs]
        assert sorted(uniq) == sorted(meta)

        assert sorted([c.name for c in add]) == \
               sorted(['1.{}'.format(u) for u in uniq])
        assert np.all([v == 1 for v in addvids])


@patch_logging
def test_binariseCategorical_nonnumeric():

    data = [random.choice(string.ascii_letters[:8]) for i in range(40)]
    data = [data[:20], data[20:]]

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid, 1-0.0, 1-1.0\n')
            for i, (v1, v2) in enumerate(zip(*data)):
                f.write('{}, {}, {}\n'.format(i + 1, v1, v2))

        vartable, proctable, cattable = gen_tables(
            [1], vtypes={1 : 'text'})[:3]
        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo, vartable, proctable, cattable)

        remove, add, addvids, kwargs = pfns.binariseCategorical(
            dt, [1],
            acrossVisits=True,
            acrossInstances=True,
            nameFormat='{vid}.{value}')

        unique   = set(data[0] + data[1])
        remnames = [r.name for r in remove]
        addnames = [a.name for a in add]

        assert '1-0.0' in remnames and '1-1.0' in remnames
        assert len(addvids) == len(add)
        assert all([v == 1 for v in addvids])
        meta = [kw['metadata'] for kw in kwargs]
        assert sorted(unique) == sorted(meta)

        for u in unique:
            name = '1.{}'.format(u)
            assert name in addnames

            series = add[addnames.index(name)]
            mask = [u == data[0][i] or u == data[1][i] for i in range(20)]

            assert (series == mask).all()


@patch_logging
def test_binariseCategorical_take():
    data = tw.dedent("""
    1,A,B,C,D,E,1,2,3,4,5
    2,A,,,,,6,,,,
    3,B,D,E,,,7,8,9,,
    4,D,E,,,,10,11,,,
    5,C,E,,,,12,13,,,
    6,A,C,D,,,14,15,16,,
    7,B,D,,,,17,18,,,
    8,C,,,,,19,,,,
    9,,,,,,,,,,
    10,B,E,,,,20,21,,,
    """).strip()

    # across all columns
    cols1 = ['eid'] + \
            ['1-0.1', '1-0.2', '1-0.3', '1-0.4', '1-0.5'] + \
            ['2-0.1', '2-0.2', '2-0.3', '2-0.4', '2-0.5']
    cols1 = ','.join(cols1)
    exp1  = tw.dedent("""
    eid,1-0.A,1-0.B,1-0.C,1-0.D,1-0.E
    1,1,2,3,4,5
    2,6,,,,
    3,,7,,8,9
    4,,,,10,11
    5,,,12,,13
    6,14,,15,16,
    7,,17,,18,
    8,,,19,,
    9,,,,,
    10,,20,,,21
    """).strip()

    # across instances (within visit)
    cols2 = ['eid'] + \
            ['1-0.0', '1-0.1', '1-1.0', '1-1.1', '1-1.2'] + \
            ['2-0.0', '2-0.1', '2-1.0', '2-1.1', '2-1.2']
    cols2 = ','.join(cols2)
    exp2  = tw.dedent("""
    eid,1-0.A,1-0.B,1-0.C,1-0.D,1-0.E,1-1.C,1-1.D,1-1.E
    1,1,2,,,,3,4,5
    2,6,,,,,,,
    3,,7,,8,,,,9
    4,,,,10,11,,,
    5,,,12,,13,,,
    6,14,,15,,,,16,
    7,,17,,18,,,,
    8,,,19,,,,,
    9,,,,,,,,
    10,,20,,,21,,,
    """).strip()

    # across visits (within instance)
    cols3 = ['eid'] + \
            ['1-0.0', '1-1.0', '1-0.1', '1-1.1', '1-2.1'] + \
            ['2-0.0', '2-1.0', '2-0.1', '2-1.1', '2-2.1']
    cols3 = ','.join(cols3)
    exp3  = tw.dedent("""
    eid,1-A.0,1-B.0,1-C.0,1-D.0,1-E.0,1-C.1,1-D.1,1-E.1
    1,1,2,,,,3,4,5
    2,6,,,,,,,
    3,,7,,8,,,,9
    4,,,,10,11,,,
    5,,,12,,13,,,
    6,14,,15,,,,16,
    7,,17,,18,,,,
    8,,,19,,,,,
    9,,,,,,,,
    10,,20,,,21,,,
    """).strip()

    # within each column
    # across all columns
    cols4 = ['eid'] + \
            ['1-0.0', '1-0.1', '1-0.2', '1-0.3', '1-0.4'] + \
            ['2-0.0', '2-0.1', '2-0.2', '2-0.3', '2-0.4']
    cols4 = ','.join(cols4)
    exp4 = tw.dedent("""
    eid,1-0.0_A,1-0.0_B,1-0.0_C,1-0.0_D,1-0.1_B,1-0.1_C,1-0.1_D,1-0.1_E,1-0.2_C,1-0.2_D,1-0.2_E,1-0.3_D,1-0.4_E
    1,1,,,,2,,,,3,,,4,5
    2,6,,,,,,,,,,,,
    3,,7,,,,,8,,,,9,,
    4,,,,10,,,,11,,,,,
    5,,,12,,,,,13,,,,,
    6,14,,,,,15,,,,16,,,
    7,,17,,,,,18,,,,,,
    8,,,19,,,,,,,,,,
    9,,,,,,,,,,,,,
    10,,20,,,,,,21,,,,,
    """).strip()

    tests = [(cols1, exp1, True, True),
             (cols2, exp2, False, True),
             (cols3, exp3, True, False),
             (cols4, exp4, False, False),
    ]

    with tempdir():
        for cols, exp, av, ai in tests:
            with open('data.txt', 'wt') as f:
                f.write(cols + '\n')
                f.write(data)

            vartable, proctable, cattable = gen_tables(
                [1, 2], vtypes={1 : 'text'})[:3]
            finfo = fileinfo.FileInfo('data.txt')
            dt, _ = importing.importData(finfo, vartable, proctable, cattable)

            remove, add, addvids, kwargs = pfns.binariseCategorical(
                dt, [1],
                acrossVisits=av,
                acrossInstances=ai, take=2)

            exp = pd.read_csv(io.StringIO(exp), index_col=0)
            got = pd.DataFrame({a.name : a for a in add})
            assert_frame_equal(got, exp, check_dtype=False, check_like=False)



def test_binariseCategorical_missing_vars():

    data = np.random.randint(1, 10, (50, 5))
    data[:, 0] = np.arange(1, 51)
    cols = ['eid', '1-0.0', '2-0.0', '3-0.0', '4-0.0']
    vids  = [1, 2, 3, 4]

    nuniq = {i :  len(np.unique(data[:, i])) for i in [1, 2, 3, 4]}

    with tempdir():
        np.savetxt('data.txt', data, delimiter=',', header=','.join(cols))
        vartable, proctable, cattable = gen_tables(vids)[:3]
        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo, vartable, proctable, cattable)

        series = pfns.binariseCategorical(dt, [1], take=[3])[1]
        assert len(series) == nuniq[1]

        series = pfns.binariseCategorical(dt, [1, 2], take=[3, 4])[1]
        assert len(series) == nuniq[1] + nuniq[2]

        series = pfns.binariseCategorical(dt, [1], take=[5])[1]
        assert len(series) == 0

        series = pfns.binariseCategorical(dt, [1, 2], take=[3, 5])[1]
        assert len(series) == nuniq[1]

        series = pfns.binariseCategorical(dt, [1, 5], take=[3, 6])[1]
        assert len(series) == nuniq[1]

        series = pfns.binariseCategorical(dt, [5])[1]
        assert len(series) == 0

        series = pfns.binariseCategorical(dt, [5], take=[6])[1]
        assert len(series) == 0

        series = pfns.binariseCategorical(dt, [5], take=[6])[1]
        assert len(series) == 0



@patch_logging
def test_expandCompound():

    data = []

    for i in range(20):
        rlen = np.random.randint(1, 20)
        row = np.random.randint(1, 100, rlen)
        data.append(row)

    exp = np.full((len(data), max(map(len, data))), np.nan)

    for i in range(len(data)):
        exp[i, :len(data[i])] = data[i]

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid\t1-0.0\n')
            for i in range(len(data)):
                f.write(str(i + 1) + '\t' + ','.join(map(str, data[i])))
                f.write('\n')

        vartable, proctable, cattable = gen_tables(
            [1], vtypes={1 : 'text'})[:3]
        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo, vartable, proctable, cattable)

        dt[:, '1-0.0'] = dt[:, '1-0.0'].apply(
            lambda v: np.fromstring(v, sep=','))

        remove, add, addvids = pfns.expandCompound(dt, [1])

        assert [r.name for r in remove] == ['1-0.0']
        assert len(add) == max(map(len, data))
        assert len(addvids) == len(add)
        assert all([v == 1 for v in addvids])

        for col in range(exp.shape[1]):
            expcol = exp[:, col]
            gotcol = add[col].values

            expna = np.isnan(expcol)
            gotna = np.isnan(gotcol)

            assert np.all(        expna  ==         gotna)
            assert np.all(expcol[~expna] == gotcol[~gotna])
