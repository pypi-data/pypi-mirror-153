#!/usr/bin/env python
#
# test_importing.py
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import multiprocessing as mp
import textwrap as tw

import numpy as np
import pandas as pd

import funpack.importing      as importing
import funpack.importing.core as core
import funpack.loadtables     as loadtables
import funpack.util           as util
import funpack.custom         as custom
import funpack.fileinfo       as fileinfo

from funpack.tests import tempdir, gen_tables


def test_loadFiles():

    vartable = gen_tables([10, 100])[0]
    data     = np.random.randint(1, 100, (10, 2))

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid, 10-0.0, 100-0.0\n')
            for i, d in enumerate(data):
                f.write('{}, {}, {}\n'.format(i, *d))
            f.write('11, 54, abcde\n')

        finfo = fileinfo.FileInfo('data.txt')

        cols = {'data.txt' : finfo.columns('data.txt')}

        vartable.loc[10,  'Type'] = util.CTYPES.integer
        vartable.loc[100, 'Type'] = util.CTYPES.continuous

        loaded = core.loadFiles(finfo, vartable, cols)[0]
        got10  = loaded['10-0.0'].values
        got100 = loaded['100-0.0'].values

        # both 10 and 100 should be numeric
        exp10  = np.array(list(data[:, 0]) + [54])
        exp100 = np.array(list(data[:, 1]) + [np.nan])

        gotnan = np.isnan(got100)

        assert np.all(exp10 == got10)
        assert np.all(np.isnan(exp100) == gotnan)
        assert np.all(exp100[~gotnan] == got100[~gotnan])


def test_loadFiles_multiple_files_cols():
    vartable = gen_tables([10, 20, 30, 40])[0]
    data = [
        np.random.randint(1, 100, (10, 2)),
        np.random.randint(1, 100, (10, 2))]

    with tempdir():
        dfiles = ['data{}.txt'.format(i) for i in range(len(data))]
        for fi, d in enumerate(data):
            with open(dfiles[fi], 'wt') as f:

                cols = ['eid'] + ['{}-0.0'.format((ci + 1) * 10)
                                  for ci in range(fi * 2, fi * 2 + 2)]

                f.write('{}\n'.format(','.join(cols)))

                for ri, c in enumerate(d):
                    f.write('{}, {}, {}\n'.format(ri, *c))

        finfo   = fileinfo.FileInfo(dfiles)
        cols    = [finfo.columns(f) for f in dfiles]
        coldict = dict(zip(dfiles, cols))

        loaded, lcols = core.loadFiles(finfo, vartable, coldict)

        assert lcols == cols[0] + cols[1][1:]

        assert np.all(loaded['10-0.0'] == data[0][:, 0])
        assert np.all(loaded['20-0.0'] == data[0][:, 1])
        assert np.all(loaded['30-0.0'] == data[1][:, 0])
        assert np.all(loaded['40-0.0'] == data[1][:, 1])


def test_loadFiles_multiple_files_rows():
    vartable = gen_tables([10, 20])[0]
    data = [
        np.random.randint(1, 100, (10, 2)),
        np.random.randint(1, 100, (10, 2))]

    with tempdir():
        dfiles = ['data{}.txt'.format(i) for i in range(len(data))]
        for fi, d in enumerate(data):
            with open(dfiles[fi], 'wt') as f:

                f.write('eid, 10-0.0, 20-0.0\n')

                for ri, c in enumerate(d):
                    f.write('{}, {}, {}\n'.format(10 * fi + ri, *c))

        finfo   = fileinfo.FileInfo(dfiles)
        cols    = [finfo.columns(f) for f in dfiles]
        coldict = dict(zip(dfiles, cols))

        loaded, lcols = core.loadFiles(
            finfo, vartable, coldict, mergeAxis='subjects')

        assert lcols == cols[0]
        assert np.all(loaded['10-0.0'] ==
                      np.concatenate((data[0][:, 0], data[1][:, 0])))
        assert np.all(loaded['20-0.0'] ==
                      np.concatenate((data[0][:, 1], data[1][:, 1])))


def test_loadFiles_indexes_cols():
    vartable = gen_tables([10, 20, 30, 40])[0]
    data = [
        np.random.randint(1, 100, (10, 2)),
        np.random.randint(1, 100, (10, 2))]

    with tempdir():
        dfiles = ['data{}.txt'.format(i) for i in range(len(data))]
        with open(dfiles[0], 'wt') as f:
            f.write('10-0.0,eid,20-0.0\n')
            for ri, c in enumerate(data[0]):
                f.write('{}, {}, {}\n'.format(c[0], ri, c[1]))
        with open(dfiles[1], 'wt') as f:
            f.write('30-0.0,40-0.0,eid\n')
            for ri, c in enumerate(data[1]):
                f.write('{}, {}, {}\n'.format(c[0], c[1], ri))

        idxdict = {'data0.txt' : [1], 'data1.txt' : [2]}
        finfo   = fileinfo.FileInfo(dfiles, indexes=idxdict)
        cols    = [finfo.columns(f) for f in dfiles]
        coldict = {}

        # loadFiles expects the first
        # column to be the index
        coldict['data0.txt'] = cols[0]
        coldict['data1.txt'] = cols[1]

        loaded, lcols = core.loadFiles(finfo, vartable, coldict)

        assert lcols == [cols[0][1], cols[0][0], cols[0][2],
                         cols[1][0], cols[1][1]]

        assert np.all(loaded['10-0.0'] == data[0][:, 0])
        assert np.all(loaded['20-0.0'] == data[0][:, 1])
        assert np.all(loaded['30-0.0'] == data[1][:, 0])
        assert np.all(loaded['40-0.0'] == data[1][:, 1])


def test_loadFiles_indexes_rows():
    vartable = gen_tables([10, 20])[0]
    data = [
        np.random.randint(1, 100, (10, 2)),
        np.random.randint(1, 100, (10, 2))]

    with tempdir():
        dfiles = ['data{}.txt'.format(i) for i in range(len(data))]
        with open(dfiles[0], 'wt') as f:
            f.write('10-0.0, eid, 20-0.0\n')
            for ri, c in enumerate(data[0]):
                f.write('{}, {}, {}\n'.format(c[0], 10 * 0 + ri, c[1]))
        with open(dfiles[1], 'wt') as f:
            f.write('10-0.0, 20-0.0, eid\n')
            for ri, c in enumerate(data[1]):
                f.write('{}, {}, {}\n'.format(c[0], c[1], 10 * 1 + ri))

        idxdict = {'data0.txt' : [1], 'data1.txt' : [2]}
        finfo   = fileinfo.FileInfo(dfiles, indexes=idxdict)
        cols    = [finfo.columns(f) for f in dfiles]
        coldict = {}

        coldict['data0.txt'] = cols[0]
        coldict['data1.txt'] = cols[1]

        loaded, lcols = core.loadFiles(
            finfo, vartable, coldict,
            mergeAxis='subjects')

        assert lcols == [cols[0][1], cols[0][0], cols[0][2]]
        assert np.all(loaded.index     == range(20))
        assert np.all(loaded['10-0.0'] ==
                      np.concatenate((data[0][:, 0], data[1][:, 0])))
        assert np.all(loaded['20-0.0'] ==
                      np.concatenate((data[0][:, 1], data[1][:, 1])))


def test_loadFiles_subjects_exclude():
    vartable = gen_tables([10, 20])[0]
    data = np.random.randint(1, 100, (10, 2))

    with tempdir():
        dfile = 'data.txt'
        with open(dfile, 'wt') as f:
            f.write('eid, 10-0.0, 20-0.0\n')
            for ri, c in enumerate(data):
                f.write('{}, {}, {}\n'.format(ri+1, c[0], c[1]))

        finfo   = fileinfo.FileInfo([dfile])
        cols    = finfo.columns(dfile)

        loaded, lcols = core.loadFiles(
            finfo, vartable, {dfile : cols},
            subjects=np.arange(1, 10),
            exclude=np.arange(5, 11))

        assert loaded.index.name == 'eid'
        assert (loaded.index == [1, 2, 3, 4]).all()



def test_importData_indexes():
    """
    """

    data1 = tw.dedent("""
    col1,idcol
    10,1
    20,2
    30,3
    40,4
    50,5
    60,6
    70,7
    80,8
    90,9
    100,10
    """).strip()

    data2 = tw.dedent("""
    idcol,col2
    2,200
    4,400
    6,600
    8,800
    10,1000
    """).strip()

    vartable, proctable, cattable = gen_tables([1])[:3]

    custom.registerBuiltIns()

    with tempdir():
        with open('data1.txt', 'wt') as f: f.write(data1)
        with open('data2.txt', 'wt') as f: f.write(data2)

        # check that loaded column order matches
        # order in which input files are specified
        idxdict = {'data1.txt' : [1]}
        finfo1  = fileinfo.FileInfo(['data1.txt', 'data2.txt'],
                                     indexes=idxdict)
        finfo2  = fileinfo.FileInfo(['data2.txt', 'data1.txt'],
                                     indexes=idxdict)

        loaded1, _ = importing.importData(
            finfo1, vartable, proctable, cattable)
        loaded2, _ = importing.importData(finfo2,
            vartable, proctable, cattable)

        loaded1 = loaded1[:, :]
        loaded2 = loaded2[:, :]

        assert np.all(loaded1.index == [2, 4, 6, 8, 10])
        assert len(loaded1.columns) == 2

        assert loaded1.index.name == 'idcol'
        assert loaded2.index.name == 'idcol'
        assert np.all(loaded1.columns == ['col1', 'col2'])
        assert np.all(loaded2.columns == ['col2', 'col1'])

        assert np.all(loaded1['col1'] == [20,  40,  60,  80,  100])
        assert np.all(loaded1['col2'] == [200, 400, 600, 800, 1000])

        assert np.all(loaded1 == loaded2[loaded1.columns])


def test_importData_non0_index_with_dropped_columns():
    data = tw.dedent("""
    1-0.0,2-0.0,eid,3-0.0,4-0.0
    10,20,1,30,40
    11,21,2,31,41
    12,22,3,32,42
    13,23,4,33,43
    14,24,5,34,44
    """).strip()

    vartable, proctable, cattable = gen_tables([1, 2, 3, 4])[:3]

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f: f.write(data)

        indexes = {'data.txt' : [2]}

        finfo = fileinfo.FileInfo('data.txt', indexes=indexes)

        loaded, _ = importing.importData(
            finfo, vartable, proctable, cattable,
            variables=[2, 4])

        allcols = finfo.columns('data.txt')
        expcols = [allcols[2], allcols[1], allcols[4]]

        assert loaded.allColumns == expcols


def test_importData():
    vartable, proctable, cattable = gen_tables([100])[:3]
    data = np.random.randint(1, 100, (10, 2))

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid, 10-0.0, 100-0.0\n')
            for i, d in enumerate(data):
                f.write('{}, {}, {}\n'.format(i, *d))

            # bad data should be interpreted as nan
            f.write('11, 54, abcde\n')

        finfo = fileinfo.FileInfo('data.txt')
        cols = {'data.txt' : finfo.columns('data.txt')}

        vartable.loc[10,  'Type'] = util.CTYPES.integer
        vartable.loc[100, 'Type'] = util.CTYPES.continuous

        loaded, _ = importing.importData(finfo, vartable, proctable, cattable)

        assert loaded.allColumns == cols['data.txt']
        got10  = loaded[:, '10-0.0']
        got100 = loaded[:, '100-0.0']

        # 10 and 100 should be numeric,
        # non-numeric valuus should be
        # set to nan
        exp10     = np.array(list(data[:, 0]) + [54])
        exp100    = np.array(list(data[:, 1]) + [np.nan])
        got100nan = got100.isna()

        assert np.all(exp10 == got10)
        assert np.all(np.isnan(exp100) == got100nan)
        assert np.all(exp100[~got100nan] == got100[~got100nan])


def test_importData_dropped():
    vartable, proctable, cattable = gen_tables([100])[:3]
    data = np.random.randint(1, 100, (10, 3))

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid, 1-0.0, 2-0.0, 3-0.0\n')
            for i, d in enumerate(data):
                f.write('{}, {}, {}, {}\n'.format(i, *d))

        finfo = fileinfo.FileInfo('data.txt')
        cols  = finfo.columns('data.txt')

        loaded, dropped = importing.importData(
            finfo, vartable, proctable, cattable, variables=[1, 3])

        assert dropped           == [cols[2]]
        assert loaded.allColumns == [cols[0]] + cols[1::2]


def test_encoding():

    ascii_val  = 'abc'
    latin1_val = '\xa1\xa2\xa3'
    utf8_val   = '\u1F610\u1F632\u1F640'

    vartable, proctable, cattable = gen_tables(
        range(1, 2), vtypes={1:'text'})[:3]

    with tempdir():

        for val, enc in zip(
                [ascii_val, latin1_val, utf8_val],
                ['ascii', 'latin1', 'utf8']):

            data = tw.dedent("""
            eid, 1-0.0
            1, {}
            """.format(val)).strip()

            with open('data.txt', 'wt', encoding=enc) as f:
                f.write(data)

            encodings = {'data.txt' : enc}
            finfo     = fileinfo.FileInfo('data.txt', encodings=encodings)

            df_enc, _ = importing.importData(
                finfo,
                vartable,
                proctable,
                cattable)
            assert df_enc[1, '1-0.0'] == val
            del df_enc
            df_enc = None

            # ascii/latin1 should load ok without
            # us having to specify the encoding
            if enc in ('ascii', 'latin1'):
                finfo       = fileinfo.FileInfo('data.txt')
                df_noenc, _ = importing.importData(
                    finfo,
                    vartable,
                    proctable,
                    cattable)
                assert df_noenc[1, '1-0.0'] == val
                del df_noenc
                df_noenc = None


def test_importData_nonnumeric_looks_like_numeric():
    vartable, proctable, cattable = gen_tables([100])[:3]
    data = np.random.randint(1, 100, 10)

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('eid, 100-0.0\n')
            for i, d in enumerate(data):
                f.write('{}, {}\n'.format(i + 1, d))

            # make sure leading zeros are preserved
            f.write('11, 0029\n')

        finfo = fileinfo.FileInfo('data.txt')

        vartable.loc[100, 'Type'] = util.CTYPES.text

        exp = [str(v) for v in data] + ['0029']

        loaded, _ = importing.importData(
            finfo, vartable, proctable, cattable)
        assert (loaded[:, '100-0.0'] == exp).all()

        loaded, _ = importing.importData(
            finfo, vartable, proctable, cattable, trustTypes=True)
        assert (loaded[:, '100-0.0'] == exp).all()


def test_loadFile_parallel():

    ncols      = 100
    nsubjs     = 50000

    vartable   = gen_tables(range(ncols))[0]
    data       = np.random.randint(1, 100, (nsubjs, ncols + 1))
    data[:, 0] = np.arange(1, nsubjs + 1)
    colnames   = ['eid'] + ['{}-0.0'.format(i) for i in range(1, ncols + 1)]

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(colnames) + '\n')
            np.savetxt(f, data, fmt='%i', delimiter='\t')

        finfo = fileinfo.FileInfo('data.txt')
        cols  = finfo.columns('data.txt')

        exp = pd.DataFrame(data[:, 1:],
                           index=data[:, 0],
                           columns=colnames[1:])
        exp.index.name = 'eid'

        # loaded in one go
        got1 = core.loadFile(
            'data.txt',
            finfo,
            vartable,
            cols,
            nrows=100000)[0]

        # loaded in chunks in a single process
        got2 = core.loadFile(
            'data.txt',
            finfo,
            vartable,
            cols,
            nrows=9987)[0]

        # loaded in chunks in
        # multiple processes
        with mp.Pool(8) as pool:
            got3 = core.loadFile(
                'data.txt',
                finfo,
                vartable,
                cols,
                nrows=9987,
                pool=pool)[0]

        def eq(df, exp):
            assert np.all(df.eq(exp))
            assert np.all(df.columns    == exp.columns)
            assert np.all(df.index      == exp.index)
            assert        df.index.name == exp.index.name

        eq(got1, exp)
        eq(got2, exp)
        eq(got3, exp)

        # loaded in chunks in
        # multiple processes,
        # with subject inclusion
        # criteria
        include = np.random.choice(data[:, 0], 40000)
        exclude = np.random.choice(data[:, 0], 5000)
        exprs   = ['v1 > 25 && v2 < 75', 'v20 >= 10']

        with mp.Pool(8) as pool:
            got = core.loadFile(
                'data.txt',
                finfo,
                vartable,
                cols,
                subjects=include,
                subjectExprs=exprs,
                exclude=exclude,
                nrows=6987,
                pool=pool)[0]
        mask              = np.zeros(nsubjs, dtype=np.bool)
        mask[include - 1] = 1
        emask             = (data[:, 1] > 25) & (data[:, 2] < 75)
        emask             = emask | (data[:, 20] >= 10)
        mask              = mask & emask
        mask[exclude - 1] = 0

        eq(got, exp[mask])



def test_importData_dropNaRows():

    data = tw.dedent("""
    eid, 1-0.0, 2-0.0
    1,10,100
    2,,
    3,30,
    4,40,400
    5,,500
    6,60,600
    7,,
    8,80,800
    9,,
    10,100,1000
    """).strip()

    vartable, proctable, cattable = gen_tables([2])[:3]

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write(data)

        finfo = fileinfo.FileInfo('data.txt')
        loaded, _ = importing.importData(
            finfo, vartable, proctable, cattable, dropNaRows=True)

        assert list(loaded.index) == [1, 3, 4, 5, 6, 8, 10]


def test_importData_duplicate_columns_rename():

    data       = np.random.randint(1, 100, (10, 3))
    data[:, 0] = np.arange(1, 10 + 1)
    colnames   = ['eid'] + ['1-0.0', '1-0.0']

    vartable, proctable, cattable = gen_tables([1])[:3]

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(colnames) + '\n')
            np.savetxt(f, data, fmt='%i', delimiter='\t')

        finfo     = fileinfo.FileInfo('data.txt', renameDuplicates=True)
        dtable, _ = importing.importData(finfo, vartable, proctable, cattable)

        cols = dtable.dataColumns

        assert dtable.variables == [0, 1]
        assert [c.name     for c in cols] == ['1-0.0', '1-0.0.1']
        assert [c.origname for c in cols] == ['1-0.0', '1-0.0']
        assert (dtable[:, :] == data[:, 1:]).all().all()


def test_importData_duplicate_columns_multiple_files_rename():

    data       = np.random.randint(1, 100, (10, 5))
    data[:, 0] = np.arange(1, 10 + 1)
    colnames1  = ['eid'] + ['1-0.0', '2-0.0']
    colnames2  = ['eid'] + ['2-0.0', '3-0.0']

    vartable, proctable, cattable = gen_tables([1, 2, 3])[:3]

    custom.registerBuiltIns()

    with tempdir():
        with open('data1.txt', 'wt') as f:
            f.write('\t'.join(colnames1) + '\n')
            np.savetxt(f, data[:, [0, 1, 2]], fmt='%i', delimiter='\t')

        with open('data2.txt', 'wt') as f:
            f.write('\t'.join(colnames2) + '\n')
            np.savetxt(f, data[:, [0, 3, 4]], fmt='%i', delimiter='\t')

        finfo     = fileinfo.FileInfo(['data1.txt', 'data2.txt'],
                                      renameDuplicates=True)
        dtable, _ = importing.importData(finfo, vartable, proctable, cattable)

        cols      = dtable.dataColumns
        names     = sorted([c.name     for c in cols])
        orignames = sorted([c.origname for c in cols])

        assert dtable.variables == [0, 1, 2, 3]
        assert names     == ['1-0.0', '2-0.0', '2-0.0.1', '3-0.0']
        assert orignames == ['1-0.0', '2-0.0', '2-0.0',   '3-0.0']
        assert (dtable[:, names] == data[:, 1:]).all().all()


def test_importData_duplicate_columns_remove():

    data       = np.random.randint(1, 100, (10, 6))
    data[:, 0] = np.arange(1, 10 + 1)
    colnames   = ['eid'] + ['1-0.0', '1-0.0', '2-0.0', '3-0.0', '3-0.0']

    vartable, proctable, cattable = gen_tables([1])[:3]

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(colnames) + '\n')
            np.savetxt(f, data, fmt='%i', delimiter='\t')

        finfo     = fileinfo.FileInfo('data.txt',
                                      renameDuplicates=True,
                                      renameSuffix='.REMOVE')
        dtable, _ = importing.importData(finfo,
                                         vartable,
                                         proctable,
                                         cattable,
                                         excludeColnames=['.REMOVE'])

        cols = dtable.dataColumns

        assert dtable.variables           == [0, 1, 2, 3]
        assert [c.name     for c in cols] == ['1-0.0', '2-0.0', '3-0.0']
        assert [c.origname for c in cols] == ['1-0.0', '2-0.0', '3-0.0']
        assert (dtable[:, :] == data[:, [1, 3, 4]]).all().all()


def test_importData_duplicate_columns_multiple_files_remove():

    data       = np.random.randint(1, 100, (10, 8))
    data[:, 0] = np.arange(1, 10 + 1)
    colnames1  = ['eid'] + ['1-0.0', '2-0.0', '2-0.0']
    colnames2  = ['eid'] + ['2-0.0', '3-0.0', '3-0.0', '4-0.0']

    vartable, proctable, cattable = gen_tables([1, 2, 3])[:3]

    custom.registerBuiltIns()

    with tempdir():
        with open('data1.txt', 'wt') as f:
            f.write('\t'.join(colnames1) + '\n')
            np.savetxt(f, data[:, [0, 1, 2, 3]], fmt='%i', delimiter='\t')

        with open('data2.txt', 'wt') as f:
            f.write('\t'.join(colnames2) + '\n')
            np.savetxt(f, data[:, [0, 4, 5, 6, 7]], fmt='%i', delimiter='\t')

        finfo     = fileinfo.FileInfo(['data1.txt', 'data2.txt'],
                                      renameDuplicates=True,
                                      renameSuffix='.REMOVE')
        dtable, _ = importing.importData(finfo,
                                         vartable,
                                         proctable,
                                         cattable,
                                         excludeColnames=['.REMOVE'])

        cols      = dtable.dataColumns
        names     = sorted([c.name     for c in cols])
        orignames = sorted([c.origname for c in cols])

        assert dtable.variables  == [0, 1, 2, 3, 4]
        assert names             == ['1-0.0', '2-0.0', '3-0.0', '4-0.0']
        assert orignames         == ['1-0.0', '2-0.0', '3-0.0', '4-0.0']
        assert (dtable[:, names] == data[:, [1, 2, 5, 7]]).all().all()
