#!/usr/bin/env python
#
# test_cleaning.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import warnings
import random
import string
import textwrap as tw

import multiprocessing as mp
from   unittest import mock

import pytest

import numpy  as np
import pandas as pd

import funpack.loadtables as lt
import funpack.cleaning as cleaning
import funpack.custom as custom
import funpack.cleaning_functions as cfns

import funpack.fileinfo  as fileinfo
import funpack.importing as importing
import funpack.hierarchy as hierarchy

from . import tempdir, gen_test_data, gen_tables, clear_plugins


def test_remove():
    assert cfns.remove(None, 0, ['a', 'b', 'c']) == []


def test_keepVisits():
    # first,
    # last,
    # number

    with tempdir():

        gen_test_data(10, 20, 'data.txt', max_visits=10, start_var=50)
        vartable, proctable, cattable, _ = gen_tables(range(50, 60))
        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo,
                                     vartable,
                                     proctable,
                                     cattable)

        for v in dt.variables[1:]:

            cols = dt.columns(v)
            assert cfns.keepVisits(vartable, v, cols, 'first') == [cols[0]]
            assert cfns.keepVisits(vartable, v, cols, 'last')  == [cols[-1]]

            if len(cols) >= 5:
                assert cfns.keepVisits(vartable, v, cols, 2)       == [cols[2]]
                assert cfns.keepVisits(vartable, v, cols, 3, 4)    == cols[3:5]


def test_keepVisits_not_instancing_2():

    data = tw.dedent("""
    eid\t1-0.0\t1-1.0\t1-2.0\t2-0.0\t2-1.0\t2-2.0
    1\t10\t11\t12\t20\t21\t22
    2\t10\t11\t12\t20\t21\t22
    3\t10\t11\t12\t20\t21\t22
    4\t10\t11\t12\t20\t21\t22
    5\t10\t11\t12\t20\t21\t22
    """).strip()
    with tempdir():

        with open('data.tsv', 'wt') as f:
            f.write(data)

        vartable, proctable, cattable, _ = gen_tables([1, 2])

        vartable.loc[1, 'Instancing'] = 2
        vartable.loc[2, 'Instancing'] = 0

        finfo = fileinfo.FileInfo('data.tsv')
        dt, _ = importing.importData(finfo, vartable, proctable, cattable)

        v1cols = dt.columns(1)
        v2cols = dt.columns(2)

        assert cfns.keepVisits(dt.vartable, 1, v1cols, 'first') == [v1cols[0]]
        assert cfns.keepVisits(dt.vartable, 1, v1cols, 'last')  == [v1cols[-1]]
        assert cfns.keepVisits(dt.vartable, 1, v1cols, 0, 1)    ==  v1cols[:2]
        assert cfns.keepVisits(dt.vartable, 1, v1cols, 1)       == [v1cols[1]]

        # v2 does not have instancing 2, should be ignored
        assert cfns.keepVisits(dt.vartable, 2, v2cols, 'first') == v2cols
        assert cfns.keepVisits(dt.vartable, 2, v2cols, 'last')  == v2cols
        assert cfns.keepVisits(dt.vartable, 2, v2cols, 0)       == v2cols
        assert cfns.keepVisits(dt.vartable, 2, v2cols, 2)       == v2cols
        assert cfns.keepVisits(dt.vartable, 2, v2cols, 1)       == v2cols
        assert cfns.keepVisits(dt.vartable, 2, v2cols, 0, 1)    == v2cols


def test_fillVisits():

    with tempdir():

        mgr = mp.Manager()

        data        = np.zeros((20, 4), dtype=np.float32)
        data[:, 0]  = np.arange(1, 21)
        data[:, 1:] = np.random.randint(1, 100, (20, 3))

        cols = ['eid', '1-0.0', '1-1.0', '1-2.0']

        data[ 0:10, 1] = np.nan
        data[ 5:15, 2] = np.nan
        data[10:,   3] = np.nan

        meanexp           = np.copy(data)
        meanexp[ 0:5,  1] = np.mean(data[0:5, 2:4], axis=1)
        meanexp[ 5:10, 1] = data[ 5:10, 3]
        meanexp[ 5:10, 2] = data[ 5:10, 3]
        meanexp[10:15, 2] = data[10:15, 1]
        meanexp[10:15, 3] = data[10:15, 1]
        meanexp[15:20, 3] = np.mean(data[15:20, 1:3], axis=1)

        modeexp           = np.copy(meanexp)

        m1 = pd.DataFrame({'a' : data[ 0:5,  2], 'b' : data[ 0:5,  3]})
        m1 = np.asarray(m1.mode(axis=1).iloc[:, 0])

        m2 = pd.DataFrame({'a' : data[15:20, 1], 'b' : data[15:20, 2]})
        m2 = np.asarray(m2.mode(axis=1).iloc[:, 0])

        modeexp[ 0:5,  1] = m1
        modeexp[15:20, 3] = m2

        with open('data.txt', 'wt') as f:

            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')

        vartable, proctable, cattable, _ = gen_tables([1])

        for method in ['mean', 'mode']:

            finfo = fileinfo.FileInfo('data.txt')
            dt, _ = importing.importData(finfo,
                                         vartable,
                                         proctable,
                                         cattable,
                                         njobs=mp.cpu_count(),
                                         mgr=mgr)

            cfns.fillVisits(dt, 1, method)

            if   method == 'mean': exp = meanexp
            elif method == 'mode': exp = modeexp

            assert np.all(dt[:, '1-0.0'] == exp[:, 1])
            assert np.all(dt[:, '1-1.0'] == exp[:, 2])
            assert np.all(dt[:, '1-2.0'] == exp[:, 3])

        with pytest.raises(ValueError):
            cfns.fillVisits(dt, 1, 'bad_method')
        dt = None
        mgr = None
        pool = None



def test_fillMissing():
    with tempdir():

        mgr = mp.Manager()

        data        = np.zeros((20, 3), dtype=np.float32)
        data[:, 0]  = np.arange(1, 21)
        data[:, 1:] = np.random.randint(1, 100, (20, 2))

        cols = ['eid', '1-0.0', '2-0.0']

        data[ 0:10, 1] = np.nan
        data[ 5:15, 2] = np.nan

        exp = np.copy(data)
        exp[ 0:10, 1] = 999
        exp[ 5:15, 2] = 12345

        with open('data.txt', 'wt') as f:

            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')

        vartable, proctable, cattable, _ = gen_tables([1])

        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo,
                                     vartable,
                                     proctable,
                                     cattable,
                                     njobs=mp.cpu_count(),
                                     mgr=mgr)

        cfns.fillMissing(dt, 1, 999)
        cfns.fillMissing(dt, 2, 12345)

        assert np.all(dt[:, '1-0.0'] == exp[:, 1])
        assert np.all(dt[:, '2-0.0'] == exp[:, 2])
        dt = None
        mgr = None
        pool = None


def test_codeToNumeric():

    hier  = hierarchy.getHierarchyFilePath(name='opcs3')
    hier  = hierarchy.loadHierarchyFile(hier)
    codes = list(random.sample(hier.codings, 20)) + ['badcode']
    exp   = [hier.index(c) for c in codes[:-1]] + [np.nan]

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid\t1-0.0\n')
            for i, c in enumerate(codes, 1):
                f.write('{}\t{}\n'.format(i, c))

        vartable, proctable, cattable, _ = gen_tables([1], vtypes={1:'text'})

        vartable.loc[1, 'DataCoding'] = hierarchy.HIERARCHY_DATA_NAMES['opcs3']

        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo,
                                     vartable,
                                     proctable,
                                     cattable)
        cfns.codeToNumeric(dt, 1)

        got = dt[:, '1-0.0']
        exp = pd.Series(exp, name='1-0.0', index=got.index)

        gotna = pd.isna(got)
        expna = pd.isna(exp)

        assert np.all(got[~gotna] == exp[~expna])
        assert np.all(gotna       == expna)
        dt = None


def test_makeNa():

    data        = np.zeros((100, 3), dtype=np.float32)
    data[:, 0]  = np.arange(1, 101)
    data[:, 1:] = np.random.randint(1, 100, (100, 2))

    cols = ['eid', '1-0.0', '2-0.0']

    with tempdir():

        mgr = mp.Manager()
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')
        vartable, proctable, cattable, _ = gen_tables([1, 2])

        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo,
                                     vartable,
                                     proctable,
                                     cattable,
                                     njobs=mp.cpu_count(),
                                     mgr=mgr)

        cfns.makeNa(dt, 1, '>= 25')
        cfns.makeNa(dt, 2, '<  50')

        na1mask = data[:, 1] >= 25
        na2mask = data[:, 2] <  50

        dt1 = dt[dt[:, '1-0.0'].notna(), '1-0.0']
        dt2 = dt[dt[:, '2-0.0'].notna(), '2-0.0']

        assert np.all(      na1mask     == dt[:, '1-0.0'].isna())
        assert np.all(      na2mask     == dt[:, '2-0.0'].isna())
        assert np.all(data[~na1mask, 1] == dt1)
        assert np.all(data[~na2mask, 2] == dt2)
        dt = None
        mgr = None
        pool = None


def test_applyNewLevels():

    eids  = np.arange(1, 51)
    data1 = np.random.randint(0, 10, 50)
    data2 = np.random.randint(0, 10, 50)
    data3 = np.random.randint(0, 10, 50)
    data4 = np.array(random.choices(string.digits, k=50))

    codes1 = np.random.randint(100, 200, 10)
    codes2 = np.random.randint(100, 200, 10)
    codes3 = np.arange(9, -1, -1)
    codes4 = list(string.digits)
    random.shuffle(codes4)
    codes4 = np.array(codes4)

    exp1 = [codes1[    data1[i]]  for i in range(50)]
    exp2 = [codes2[    data2[i]]  for i in range(50)]
    exp3 = [codes3[    data3[i]]  for i in range(50)]
    exp4 = [codes4[int(data4[i])] for i in range(50)]

    vartable, proctable, cattable, _ = gen_tables(
        [1, 2, 3, 4],
        vtypes={1 : 'integer',
                2 : 'integer',
                3 : 'integer',
                4 : 'text'})

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        vartable['RawLevels'][1] = np.arange(10)
        vartable['NewLevels'][1] = codes1
        vartable['RawLevels'][2] = np.arange(10)
        vartable['NewLevels'][2] = codes2
        vartable['RawLevels'][3] = np.arange(10)
        vartable['NewLevels'][3] = codes3
        vartable['RawLevels'][4] = np.array([c for c in string.digits])
        vartable['NewLevels'][4] = codes4

    cols = ['eid', '1-0.0', '2-0.0', '3-0.0', '4-0.0']

    with tempdir():

        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            for eid, d1, d2, d3, d4 in zip(eids, data1, data2, data3, data4):
                f.write(f'{eid}\t{d1}\t{d2}\t{d3}\t{d4}\n')

        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo,
                                     vartable,
                                     proctable,
                                     cattable)

        cleaning.applyNewLevels(dt)

        assert np.all(dt[:, '1-0.0'] == exp1)
        assert np.all(dt[:, '2-0.0'] == exp2)
        assert np.all(dt[:, '3-0.0'] == exp3)
        assert np.all(dt[:, '4-0.0'] == exp4)

        col3 = dt.columns(3)[0]

        assert dt.getFlags(col3) == set(['inverted'])
        dt = None


def test_applyNAInsertion():


    eids  = np.arange(1, 101)
    data1 = np.random.randint(0, 10, 100).astype(np.float32)
    data2 = np.random.randint(0, 10, 100).astype(np.float32)
    data3 = np.array(random.choices(string.ascii_letters, k=100))
    data4 = np.datetime64('2020-01-01') + np.random.choice(366, 100)

    data1 = pd.Series(data1, index=eids)
    data2 = pd.Series(data2, index=eids)
    data3 = pd.Series(data3, index=eids)
    data4 = pd.Series(data4, index=eids)

    miss1 = np.random.choice(data1, 4, replace=False)
    miss2 = np.random.choice(data2, 4, replace=False)
    miss3 = np.random.choice(data3, 4, replace=False)
    miss4 = np.random.choice(data4, 4, replace=False)

    exp1 = data1.copy()
    exp2 = data2.copy()
    exp3 = data3.copy()
    exp4 = data4.copy()

    for m in miss1: exp1[exp1 == m] = np.nan
    for m in miss2: exp2[exp2 == m] = np.nan
    for m in miss3: exp3[exp3 == m] = np.nan
    for m in miss4: exp4[exp4 == m] = np.nan

    vartable, proctable, cattable, _ = gen_tables(
        [1, 2, 3, 4], vtypes={1 : 'integer',
                              2 : 'integer',
                              3 : 'text',
                              4 : 'time'})

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        vartable['NAValues'][1] = miss1
        vartable['NAValues'][2] = miss2
        vartable['NAValues'][3] = miss3
        vartable['NAValues'][4] = miss4

    cols = ['eid', '1-0.0', '2-0.0', '3-0.0', '4-0.0']

    with tempdir():

        mgr = mp.Manager()
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            for eid, d1, d2, d3, d4 in zip(eids, data1, data2, data3, data4):
                f.write(f'{eid}\t{d1}\t{d2}\t{d3}\t{d4}\n')

        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo,
                                     vartable,
                                     proctable,
                                     cattable,
                                     njobs=mp.cpu_count(),
                                     mgr=mgr)

        cleaning.applyNAInsertion(dt)

        na1mask = dt[:, '1-0.0'].isna()
        na2mask = dt[:, '2-0.0'].isna()
        na3mask = dt[:, '3-0.0'].isna()
        na4mask = dt[:, '4-0.0'].isna()

        d1 = dt[:, '1-0.0'][~na1mask]
        d2 = dt[:, '2-0.0'][~na2mask]
        d3 = dt[:, '3-0.0'][~na3mask]
        d4 = dt[:, '4-0.0'][~na4mask]

        assert np.all(na1mask == pd.isna(exp1))
        assert np.all(na2mask == pd.isna(exp2))
        assert np.all(na3mask == pd.isna(exp3))
        assert np.all(na4mask == pd.isna(exp4))

        assert np.all(d1 == exp1[~na1mask])
        assert np.all(d2 == exp2[~na2mask])
        assert np.all(d3 == exp3[~na3mask])
        assert np.all(d4 == exp4[~na4mask])
        dt = None
        mgr = None
        pool = None


def test_applyChildValues():

    sz          = 100
    ndata        = np.zeros((sz, 6), dtype=np.float32)
    ndata[:, 0]  = np.arange(1, sz + 1)
    ndata[:, 1:] = np.random.randint(1, 10, (sz, 5))
    sdata        = np.array(random.choices(string.ascii_letters, k=sz))
    sdata        = pd.Series(sdata, index=ndata[:, 0])

    cols = ['eid', '1-0.0', '2-0.0', '3-0.0', '4-0.0', '5-0.0', '6-0.0']

    # parents
    # 1: 2, 3
    # 2: 3
    # 3: 4
    # 4: 5
    # 6: 5

    pvals = {
        1 : 'v2 == 5, v3 > 5',
        2 : 'v3 < 8',
        3 : 'v4 >= 6',
        4 : 'v5 == 2',
        5 : 'v123 == 7',
        6 : 'v5 < 5',
        7 : 'v8 < 5'
    }
    cvals = {
        1 : '100, 101',
        2 : '200',
        3 : '300',
        4 : '400',
        5 : '123',
        6 : 'abc',
        7 : '1234'
    }

    ndata[ ndata[:, 5] == 2,                      4] = np.nan
    ndata[ ndata[:, 4] >= 6,                      3] = np.nan
    ndata[ ndata[:, 3] <  8,                      2] = np.nan
    ndata[(ndata[:, 2] == 5) | (ndata[:, 3] > 5), 1] = np.nan
    sdata[ ndata[:, 5] < 5]                          = np.nan

    nexp = np.copy(ndata)
    nan1 = np.isnan(nexp[:, 1])
    nexp[    nan1             & (nexp[:, 2] == 5), 1] = 100
    nexp[    nan1             & (nexp[:, 3] >  5), 1] = 101
    nexp[np.isnan(nexp[:, 2]) & (nexp[:, 3] <  8), 2] = 200
    nexp[np.isnan(nexp[:, 3]) & (nexp[:, 4] >= 6), 3] = 300
    nexp[np.isnan(nexp[:, 4]) & (nexp[:, 5] == 2), 4] = 400
    sexp = sdata.copy()
    sexp[pd.isna(sexp)] = 'abc'


    with tempdir():

        mgr = mp.Manager()
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            for i in range(sz):
                f.write('\t'.join([str(i) for i in ndata[i, :]]))
                f.write(f'\t{sdata.iloc[i]}\n')

        vartable, proctable, cattable, _ = gen_tables(
            [1, 2, 3, 4, 5, 6, 7],
            vtypes={1 : 'integer',
                    2 : 'integer',
                    3 : 'integer',
                    4 : 'integer',
                    5 : 'integer',
                    6 : 'text',
                    7 : 'integer'})

        vartable.loc[pvals.keys(), 'ParentValues'] = np.array(
            [lt.convert_ParentValues(v) for v in pvals.values()],
            dtype=object)
        vartable.loc[cvals.keys(), 'ChildValues'] = np.array(
            [lt.convert_comma_sep_text(v) for v in cvals.values()],
            dtype=object)

        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo,
                                     vartable,
                                     proctable,
                                     cattable,
                                     njobs=mp.cpu_count(),
                                     mgr=mgr)

        cleaning.applyChildValues(dt)

        ngot = dt[:, cols[1:-1]]
        sgot = dt[:, cols[-1]]
        assert np.all(np.asarray(ngot.values) == nexp[:, 1:])
        assert np.all(np.asarray(sgot.values) == sexp)
        dt = None
        mgr = None
        pool = None


@clear_plugins
def test_applyCleaningFunctions():

    data        = np.zeros((100, 3), dtype=np.float32)
    data[:, 0]  = np.arange(1, 101)
    data[:, 1:] = np.random.randint(1, 100, (100, 2))

    cols = ['eid', '1-0.0', '2-0.0']

    @custom.cleaner()
    def proc1(dtable, vid):
        columns = dtable.columns(vid)
        for c in columns:
            dtable[:, c.name] = dtable[:, c.name] + 5


    @custom.cleaner()
    def proc2(dtable, vid, factor):
        columns = dtable.columns(vid)
        for c in columns:
            dtable[:, c.name] = dtable[:, c.name] * factor


    with tempdir():

        mgr = mp.Manager()
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')
        vartable, proctable, cattable, _ = gen_tables([1, 2, 3])

        vartable.loc[(1, ), 'Clean'] = (lt.convert_Process(
            'cleaner', 'proc1'), )
        vartable.loc[(2, ), 'Clean'] = (lt.convert_Process(
            'cleaner', 'proc2(50)'), )
        vartable.loc[(3, ), 'Clean'] = (lt.convert_Process(
            'cleaner', 'proc2(50)'), )

        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo,
                                     vartable,
                                     proctable,
                                     cattable,
                                     njobs=mp.cpu_count(),
                                     mgr=mgr)

        cleaning.applyCleaningFunctions(dt)

        assert np.all(dt[:, '1-0.0'] == data[:, 1] + 5)
        assert np.all(dt[:, '2-0.0'] == data[:, 2] * 50)
        dt = None
        mgr = None
        pool = None


def test_cleanData():

    data        = np.zeros((100, 3), dtype=np.float32)
    data[:, 0]  = np.arange(1, 101)
    data[:, 1:] = np.random.randint(1, 100, (100, 2))

    cols = ['eid', '1-0.0', '2-0.0']

    with tempdir():

        mgr = mp.Manager()
        custom.registerBuiltIns()
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')
        vartable, proctable, cattable, _ = gen_tables([1, 2])
        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo,
                                     vartable,
                                     proctable,
                                     cattable,
                                     njobs=mp.cpu_count(),
                                     mgr=mgr)

        # not crashing -> pass
        cleaning.cleanData(dt)
        dt = None
        mgr = None
        pool = None


def test_parseSpirometryData():

    data = tw.dedent("""
    eid\t1-0.0\t1-0.1\t1-0.2
    1\tblow1,5,1,2,3,4,5\tblow2,3,4,5,6\tblow3,6,1,2,3,4,5,6
    2\tblow2,5,1,2,3,4,5\tblow3,5,5,4,3,2,1\tblow1,3,3,2,1
    3\tblow1,5,1,2,3,4,5\tblow3,4,6,7,8,9\tblow2,2,1,2
    """).strip()

    # arranged by column
    exp = [
        [[1, 2, 3, 4, 5],    [3, 2, 1],       [1, 2, 3, 4, 5]],
        [[4, 5, 6],          [1, 2, 3, 4, 5], [1, 2]],
        [[1, 2, 3, 4, 5, 6], [5, 4, 3, 2, 1], [6, 7, 8, 9]]]

    exp = [[np.array(row) for row in col] for col in exp]
    exp = [pd.Series(col) for col in exp]

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write(data)

        mgr = mp.Manager()
        vartable, proctable, cattable, _ = gen_tables(
            [1, 2], vtypes={1:'compound'})

        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo,
                                     vartable,
                                     proctable,
                                     cattable,
                                     njobs=mp.cpu_count(),
                                     mgr=mgr)

        cfns.parseSpirometryData(dt, 1)

        for coli, col in enumerate(['1-0.0', '1-0.1', '1-0.2']):
            got = dt[:, col]

            for rowi in range(len(got)):
                assert np.all(exp[coli][rowi] == got.iloc[rowi])
        dt = None
        mgr = None
        pool = None


def test_flattenHierarchical():

    data = tw.dedent("""
    eid,1-0.0
    1,10
    2,20
    3,30
    4,40
    5,50
    6,60
    7,70
    8,80
    9,90
    10,
    """).strip()

    hier = tw.dedent("""
    coding	meaning	node_id	parent_id
    10	meaning 10	1	0
    20	meaning 20	2	0
    30	meaning 30	3	1
    40	meaning 40	4	1
    50	meaning 50	5	4
    60	meaning 60	6	2
    70	meaning 70	7	2
    80	meaning 80	8	6
    90	meaning 90	9	8
    """).strip()

    tests = [
        (0, [10, 20, 10, 10, 10, 20, 20, 20, 20]),
        (1, [10, 20, 30, 40, 40, 60, 70, 60, 60]),
        (2, [10, 20, 30, 40, 50, 60, 70, 80, 80]),
        (3, [10, 20, 30, 40, 50, 60, 70, 80, 90]),
        (4, [10, 20, 30, 40, 50, 60, 70, 80, 90]),
    ]

    with tempdir():

        with open('data.txt', 'wt') as f:
            f.write(data)

        # the encoding number used here (2) is a real
        # one which uses integer coding values. See
        # hierarchy.codingDataType
        with open('coding2.tsv', 'wt') as f:
            f.write(hier)

        mgr = mp.Manager()
        vartable, proctable, cattable, _ = gen_tables([1])

        for level, exp in tests:

            finfo = fileinfo.FileInfo('data.txt')
            dt, _ = importing.importData(finfo,
                                         vartable,
                                         proctable,
                                         cattable,
                                         njobs=mp.cpu_count(),
                                         mgr=mgr)

            with mock.patch('funpack.hierarchy.getHierarchyFilePath',
                            return_value='coding2.tsv'):
                cfns.flattenHierarchical(dt, 1, level)

            vals = dt[:, '1-0.0'].values

            assert pd.isna(vals[ -1])
            assert np.all( vals[:-1] == exp)

        dt = None
        mgr = None



def test_flattenHierarchical_numeric():

    data = tw.dedent("""
    eid,1-0.0
    1,10
    2,20
    3,30
    4,40
    5,50
    6,60
    7,70
    8,80
    9,90
    10,
    """).strip()

    hier = tw.dedent("""
    coding	meaning	node_id	parent_id
    10	meaning 10	1	0
    20	meaning 20	2	0
    30	meaning 30	3	1
    40	meaning 40	4	1
    50	meaning 50	5	4
    60	meaning 60	6	2
    70	meaning 70	7	2
    80	meaning 80	8	6
    90	meaning 90	9	8
    """).strip()

    # level, expected
    tests = [
        (0, [1, 2, 1, 1, 1, 2, 2, 2, 2]),
        (1, [1, 2, 3, 4, 4, 6, 7, 6, 6]),
        (2, [1, 2, 3, 4, 5, 6, 7, 8, 8]),
        (3, [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (4, [1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ]

    with tempdir():

        with open('data.txt', 'wt') as f:
            f.write(data)

        # the encoding number used here (2) is a real
        # one which uses integer coding values. See
        # hierarchy.codingDataType
        with open('coding2.tsv', 'wt') as f:
            f.write(hier)

        mgr = mp.Manager()
        vartable, proctable, cattable, _ = gen_tables([1])

        for level, exp in tests:

            finfo = fileinfo.FileInfo('data.txt')
            dt, _ = importing.importData(finfo,
                                         vartable,
                                         proctable,
                                         cattable,
                                         njobs=mp.cpu_count(),
                                         mgr=mgr)

            with mock.patch('funpack.hierarchy.getHierarchyFilePath',
                            return_value='coding2.tsv'):
                cfns.flattenHierarchical(dt, 1, level,
                                         convertNumeric=True)

            vals = dt[:, '1-0.0'].values

            assert pd.isna(vals[ -1])
            assert np.all( vals[:-1] == exp)

        dt = None
        mgr = None
