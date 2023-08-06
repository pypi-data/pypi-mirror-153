#!/usr/bin/env python
#
# test_exporting.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import             warnings
import             os
import textwrap as tw
import os.path  as op
import multiprocessing as mp
from unittest import mock

import pytest

from collections import OrderedDict

import pandas as pd
import numpy  as np
import           h5py

import funpack.importing      as importing
import funpack.exporting      as exporting
import funpack.exporting_hdf5 as exporting_hdf5
import funpack.exporting_tsv  as exporting_tsv
import funpack.datatable      as datatable
import funpack.fileinfo       as fileinfo
import funpack.custom         as custom
import funpack.util           as util

from . import (gen_DataTable,
               clear_plugins,
               patch_base_tables,
               tempdir,
               gen_test_data,
               gen_tables,
               gen_DataTableFromDataFrame)


def test_exportData():

    custom.registerBuiltIns()

    testdata = np.random.randint(1, 10, (10, 10)).astype(np.float32)

    def check(gotfile, expected):
        with open(gotfile, 'rt') as f:
            got = f.read().strip()
            return got == expected

    with tempdir():

        dtable = gen_DataTable(testdata)
        exporting.exportData(dtable, 'data.tsv', 'tsv')
        exp = ['\t'.join(['eid'] +
                         ['{}-0.0'.format(i) for i in range(1, 11)])] + \
              ['\t'.join([str(i + 1)] + [str(c) for c in r])
               for i, r in enumerate(testdata.T)]
        exp = '\n'.join(exp)
        assert check('data.tsv', exp)

        td = np.copy(testdata)
        td[5, 5] = np.nan
        dtable = gen_DataTable(td)
        exporting.exportData(dtable,
                             'data.tsv',
                             'tsv',
                             sep='*',
                             missingValues='boo')
        exp = ['*'.join(['eid'] +
                         ['{}-0.0'.format(i)  for i in range(1, 11)])] + \
              ['*'.join([str(i + 1)] +
                        ['boo' if np.isnan(c) else str(c) for c in r])
               for i, r in enumerate(td.T)]
        exp = '\n'.join(exp)
        assert check('data.tsv', exp)


def test_exportData_subjid():

    custom.registerBuiltIns()

    with tempdir():
        gen_test_data(3, 3, 'data.tsv', start_subj=10)

        variables = list(range(0, 4))
        vartable, proctable, cattable, _ = gen_tables(variables)
        colnames  = ['eid'] + ['{}-0.0'.format(v) for v in variables[1:]]
        colobjs   = [datatable.Column(None, c, i, v, 0, 0)
                     for i, (c, v) in enumerate(zip(colnames, variables))]
        data      = pd.read_csv( 'data.tsv', delimiter='\t', index_col=0)

        dtable = datatable.DataTable(
            data, colobjs, vartable, proctable, cattable)

        exporting.exportData(dtable, 'export.tsv', 'tsv')

        got = pd.read_csv('export.tsv', delimiter='\t', index_col=0)

        assert np.all(got.index == [10, 11, 12])



def test_exportData_TSV_subject_ordering():

    custom.registerBuiltIns()

    with tempdir():
        data   = np.random.randint(1, 10, (5, 20))
        dtable = gen_DataTable(data)
        subjs  = np.arange(20, 0, -1)
        dtable = dtable.subtable(rows=subjs)

        exporting.exportData(dtable, 'data.tsv', 'tsv')
        got = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        assert np.all(got.index == subjs)

        exporting.exportData(dtable,
                             'data.tsv',
                             'tsv',
                             numRows=2)
        got = pd.read_csv('data.tsv', delimiter='\t', index_col=0)
        assert np.all(got.index == subjs)


def test_exportData_numRows():

    custom.registerBuiltIns()

    with tempdir():
        data   = np.random.randint(1, 10, (5, 20))
        dtable = gen_DataTable(data)

        exporting.exportData(dtable, 'nochunks.tsv', 'tsv')
        exporting.exportData(dtable, 'chunks.tsv', 'tsv', numRows=2)

        with open('nochunks.tsv', 'rt') as f: nochunks = f.read()
        with open('chunks.tsv',   'rt') as f: chunks   = f.read()

        assert nochunks == chunks


def test_exportData_dropNaRows():

    custom.registerBuiltIns()

    with tempdir():
        data   = np.random.random((10, 10))
        data[:, [2, 4, 7]] = np.nan
        dtable = gen_DataTable(data)

        exporting.exportData(dtable, 'data.tsv', 'tsv',  dropNaRows=True)
        exporting.exportData(dtable, 'data.h5',  'hdf5', dropNaRows=True)

        got1 = pd.read_csv('data.tsv', sep='\t', index_col=0)
        got2 = pd.read_hdf('data.h5')
        exp  = data[:, [0, 1, 3, 5, 6, 8, 9]].T

        for got in [got1, got2]:
            assert list(got.index) == [1, 2, 4, 6, 7, 9, 10]
            assert np.all(np.isclose(exp, got.values))


def test_defaultDateTimeFormat():

    custom.registerBuiltIns()

    with tempdir():
        gen_test_data(3, 3, 'data.tsv', ctypes={1 : 'date', 2 : 'datetime'})

        data = pd.read_csv('data.tsv',
                           delimiter='\t',
                           parse_dates=['1-0.0', '2-0.0'],
                           infer_datetime_format=True,
                           index_col=0)
        dt = gen_DataTableFromDataFrame(data)

        dt.vartable.loc[1, 'Type'] = util.CTYPES.date
        dt.vartable.loc[2, 'Type'] = util.CTYPES.time

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            datecol        = dt[:, '1-0.0']
            datecol[2]     = np.nan
            dt[:, '1-0.0'] = datecol

        def datefmt(d):
            try:    return d.strftime('%Y-%m-%d')
            except: return np.nan
        def timefmt(t):
            try:    return t.strftime('%Y-%m-%dT%H:%M:%S%z')
            except: return np.nan

        expdate = data['1-0.0'].apply(datefmt)
        exptime = data['2-0.0'].apply(timefmt)
        expvar  = data['3-0.0']

        gotdate = exporting.defaultDateTimeFormat(
            dt, dt.columns(1)[0], data['1-0.0'])
        gottime = exporting.defaultDateTimeFormat(
            dt, dt.columns(2)[0], data['2-0.0'])
        gotvar  = exporting.defaultDateTimeFormat(
            dt, dt.columns(3)[0], data['3-0.0'])

        expdna = expdate.isna()
        exptna = exptime.isna()

        assert np.all(expdate.isna() == expdna)
        assert np.all(exptime.isna() == exptna)

        assert np.all(expdate[~expdna] == gotdate[~expdna])
        assert np.all(exptime[~exptna] == gottime[~exptna])
        assert np.all(expvar           == gotvar)


def test_exportHDF5():

    custom.registerBuiltIns()

    with tempdir():
        gen_test_data(5, 10, 'data.tsv', ctypes={1 : 'date', 2 : 'datetime'})

        data = pd.read_csv('data.tsv',
                           delimiter='\t',
                           parse_dates=['1-0.0', '2-0.0'],
                           infer_datetime_format=True,
                           index_col=0)
        dt = gen_DataTableFromDataFrame(data)

        for col in dt.dataColumns:
            exporting.formatColumn(col,
                                   dt,
                                   'default',
                                   'default',
                                   {})

        exporting_hdf5.exportHDF5(dt,
                                  'out_funpack.h5',
                                  key='h5key',
                                  style='funpack')
        exporting_hdf5.exportHDF5(dt,
                                  'out_pandas.h5',
                                  key='h5key',
                                  style='pandas')

        colnames = [c.name for c in dt.dataColumns]

        exp    = dt[:, :]
        gotpd  = pd.read_hdf('out_pandas.h5')
        gotukb = h5py.File('out_funpack.h5', 'r')
        assert gotpd.index.name     == 'eid'
        assert np.all(gotpd.columns == colnames)

        for i, c in enumerate(exp.columns):
            assert np.all(gotpd[colnames[i]] == exp[c])

        gotidx = gotukb['h5key/eid']

        assert np.all(exp.index[:] == gotidx)

        h5ver = int(h5py.__version__.split('.')[0])

        for i, col in enumerate(dt.dataColumns):
            coldata = gotukb['h5key/{}'.format(colnames[i])]

            if col.name in ('1-0.0', '2-0.0'):

                # h5py 3.x and newer will return variable
                # length UTF8 strings as bytes objects,
                # but h5py 2.x will return str objects.
                if h5ver >= 3:
                    coldata = list(coldata.asstr())

                expcol = exporting.defaultDateTimeFormat(
                    dt, col, exp[col.name])
            else:
                expcol = exp[col.name]

            assert np.all(np.asarray(coldata) == expcol)


def test_exportData_HDF_subject_ordering():

    custom.registerBuiltIns()

    with tempdir():
        data   = np.random.randint(1, 10, (5, 20))
        dtable = gen_DataTable(data)
        subjs  = np.arange(20, 0, -1)
        dtable = dtable.subtable(rows=subjs)

        # pandas style + no chunking
        exporting.exportData(dtable,
                             'data.h5',
                             fileFormat='hdf5')
        got  = pd.read_hdf('data.h5')
        assert np.all(got.index == subjs)

        # pandas style + chunking
        exporting.exportData(dtable,
                             'data.h5',
                             fileFormat='hdf5',
                             numRows=2)
        got  = pd.read_hdf('data.h5')
        assert np.all(got.index == subjs)

        # funpack style
        exporting.exportData(dtable,
                             'data.h5',
                             style='funpack',
                             fileFormat='hdf5')

        got = exporting_hdf5.importFunpackStyle(
            'data.h5', 'eid', key='funpack')

        assert np.all(got.index == subjs)



def test_compound():

    data = tw.dedent("""
    "eid","1-0.0","2-0.0"
    1,"1,2,3",8
    2,"4,5,6",8
    3,"7,8,9",8
    """).strip()

    exp = tw.dedent("""
    eid\t1-0.0\t2-0.0
    1\t1.0,2.0,3.0\t8.0
    2\t4.0,5.0,6.0\t8.0
    3\t7.0,8.0,9.0\t8.0
    """).strip()


    def parseCompound(v):
        return np.fromstring(v, sep=',')

    with tempdir():

        with open('data.txt', 'wt') as f:
            f.write(data)

        vartable, proctable, cattable, _ = gen_tables(
            [1, 2], vtypes={1:'compound'})
        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo, vartable, proctable, cattable)

        dt[:, '1-0.0'] = dt[:, '1-0.0'].apply(parseCompound)

        for col in dt.dataColumns:
            exporting.formatColumn(col,
                                   dt,
                                   'default',
                                   'default',
                                   {1 : 'compound'})

        exporting.exportData(dt,
                             'out.txt',
                             fileFormat='tsv')


        with open('out.txt', 'rt') as f:
            got = f.read().strip()

        assert got == exp


def test_exporting_id_column():
    data = tw.dedent("""
    my_id,col1
    1,11
    2,12
    3,13
    """).strip()

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write(data)

        vartable, proctable, cattable, _ = gen_tables([1], datafiles=['data.txt'])
        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(finfo, vartable, proctable, cattable)

        exporting.exportData(dt,
                             'out.txt',
                             fileFormat='tsv')
        got = pd.read_csv('out.txt', delimiter='\t', index_col=0)
        assert got.index.name == 'my_id'


def test_exporting_no_data():

    data = tw.dedent("""
    eid,1-0.0,2-0.0
    1,11,21
    2,12,22
    3,13,23
    4,14,24
    5,15,25
    """)

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write(data)

        vartable, proctable, cattable, _ = gen_tables([1])
        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(
            finfo, vartable, proctable, cattable, variables=[3])

        with pytest.raises(RuntimeError):
            exporting.exportData(dt,
                                 'out.txt',
                                 fileFormat='tsv')
        assert not op.exists('out.txt')


def test_exportTSV_parallel():

    ncols  = 100
    nsubjs = 50000

    data       = np.random.randint(1, 100, (nsubjs, ncols + 1))
    data[:, 0] = np.arange(1, nsubjs + 1)
    colnames   = ['eid'] + ['{}-0.0'.format(i) for i in range(1, ncols + 1)]

    custom.registerBuiltIns()

    with tempdir():
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(colnames) + '\n')
            np.savetxt(f, data, fmt='%i', delimiter='\t')

        vartable, proctable, cattable, _ = gen_tables(range(1, ncols + 1))
        finfo = fileinfo.FileInfo('data.txt')
        dt, _ = importing.importData(
            finfo, vartable, proctable, cattable)

        # in one go, single process
        exporting_tsv.exportTSV(dt,
                                'out1.tsv',
                                numRows=100000)

        # chunked, single process
        exporting_tsv.exportTSV(dt,
                                'out2.tsv',
                                numRows=8767)

        # chunked, multiprocess
        with mp.Pool(8) as pool:
            with mock.patch.object(dt, 'pool', return_value=pool):
                exporting_tsv.exportTSV(dt,
                                        'out3.tsv',
                                        numRows=5675)

        exp  = dt[:, :]
        got1 = pd.read_csv('out1.tsv', sep='\t', index_col=0)
        got2 = pd.read_csv('out2.tsv', sep='\t', index_col=0)
        got3 = pd.read_csv('out3.tsv', sep='\t', index_col=0)

        def eq(df):
            assert np.all(df.eq(exp))
            assert np.all(df.columns == exp.columns)
            assert np.all(df.index   == exp.index)

        eq(got1)
        eq(got2)
        eq(got3)


def test_exportCSV_escapeNewlines():

    data = tw.dedent("""
    eid,1-0.0,2-0.0
    1,"a b c
    d e f",abc
    2,one two three,"four five
    six seven"
    3,"x y	z","a b

    cde"
    """).strip()

    exp = tw.dedent(r"""
    eid,1-0.0,2-0.0
    1,a b c\nd e f,abc
    2,one two three,four five\nsix seven
    3,x y\tz,a b\n\ncde
    """).strip()

    with tempdir():

        with open('in.csv', 'wt') as f:
            f.write(data)

        vartable, proctable, cattable, _ = gen_tables(
            [1, 2], vtypes={1 : 'text', 2 : 'text'})
        finfo = fileinfo.FileInfo('in.csv')
        dt, _ = importing.importData(
            finfo, vartable, proctable, cattable)

        exporting_tsv.exportCSV(dt, 'out.csv', sep=',', escapeNewlines=True)

        with open('out.csv', 'rt') as f:
            got = f.read()

        assert got.strip() == exp
