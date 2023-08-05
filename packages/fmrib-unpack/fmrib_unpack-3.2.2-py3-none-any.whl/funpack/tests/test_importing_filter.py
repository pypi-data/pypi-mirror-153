#!/usr/bin/env python
#
# test_importing_removeSubjects.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import textwrap as tw
import pytest

import pandas as pd
import numpy as np

import funpack.importing.filter as filter

from funpack.datatable import Column
import funpack.fileinfo       as fileinfo
from . import (gen_DataTable, gen_DataTableFromDataFrame,
               tempdir, gen_tables, gen_test_data)


def test_columnsToLoad():

    data = tw.dedent("""
    eid,1-0.0,2-0.0,3-0.0
    1,10,20,30
    2,11,21,31
    3,12,22,32
    4,13,23,33
    """).strip()

    vartable = gen_tables(range(1, 10))[0]

    with tempdir():

        with open('data.txt', 'wt') as f:
            f.write(data)

        finfo = fileinfo.FileInfo('data.txt')
        cols  = finfo.columns('data.txt')

        gc, gd = filter.columnsToLoad(finfo, vartable, None)
        assert gc['data.txt'] == cols
        assert gd             == []

        gc, gd = filter.columnsToLoad(finfo, vartable, [1, 2, 3])
        assert gc['data.txt'] == cols[:4]
        assert gd             == []

        gc, gd = filter.columnsToLoad(finfo, vartable, None, exclude=[2, 3])
        assert gc['data.txt'] == cols[:2]
        assert gd             == cols[2:]

        gc, gd = filter.columnsToLoad(finfo, vartable, [1, 2, 3], exclude=[2, 3])
        assert gc['data.txt'] == cols[:2]
        assert gd             == cols[2:]


def test_filterSubjects():

    data       = np.random.randint(1, 10, (500, 11))
    index      = np.arange(1, 501)
    data[:, 0] = index
    colnames   = ['eid'] + ['{}-0.0'.format(i+1) for i in range(10)]
    cols       = [Column(None, n, i, i) for i, n in enumerate(colnames)]
    df         = pd.DataFrame(data, columns=colnames).set_index('eid')
    data       = data[:, 1:]

    #   - exclude:  list of subjects to *exclude*
    #   - include:  list of subjects to *include*
    #   - exprs:    list of expressions specifying *inclusion*

    # pass through
    got = filter.filterSubjects(df, cols)
    assert np.all(got.index == np.arange(1, 501))
    assert np.all(got == df)

    # include
    got = filter.filterSubjects(df, cols, subjects=np.arange(1, 20))
    assert np.all(got.index == np.arange(1, 20))
    assert np.all(got == df.loc[np.arange(1, 20), :])

    # exclude
    got = filter.filterSubjects(df, cols, exclude=[1, 2, 3])
    assert np.all(got.index == np.arange(4, 501))
    assert np.all(got == df.loc[np.arange(4, 501), :])

    # expr
    mask = data[:, 0] > 5
    got = filter.filterSubjects(df, cols, subjectExprs=['v1 > 5'])
    assert np.all(got.index == (np.where(mask)[0] + 1))
    assert np.all(got == data[mask, :])

    # include + exclude
    got = filter.filterSubjects(
        df, cols, subjects=np.arange(1, 20), exclude=[1, 2, 3])
    assert np.all(got.index == np.arange(4, 20))
    assert np.all(got == df.loc[np.arange(4, 20), :])

    # include + expr
    mask       = data[:, 0] > 5
    mask[100:] = 0
    got = filter.filterSubjects(
        df, cols, subjects=np.arange(1, 101), subjectExprs=['v1 > 5'])
    assert np.all(got.index == (np.where(mask)[0] + 1))
    assert np.all(got == data[mask, :])

    # expr + exclude
    mask     = data[:, 0] > 5
    mask[:3] = 0
    got = filter.filterSubjects(
        df, cols, subjectExprs=['v1 > 5'], exclude=[1, 2, 3])
    assert np.all(got.index == (np.where(mask)[0] + 1))
    assert np.all(got == data[mask, :])

    # include + expr + exclude
    mask          = data[:, 0] > 5
    mask[300:]    = 0
    mask[75:200]  = 0
    got = filter.filterSubjects(
        df, cols,
        subjects=np.arange(1, 301),
        exclude=np.arange(76, 201),
        subjectExprs=['v1 > 5'])
    assert np.all(got.index == (np.where(mask)[0] + 1))
    assert np.all(got == data[mask, :])

    # multiple expressions
    got = filter.filterSubjects(
        df, cols, subjectExprs=['v1 > 5', 'v2 == 9'])
    mask = (data[:, 0] > 5) | (data[:, 1] == 9)
    assert np.all(got.index == np.where(mask)[0] + 1)
    assert np.all(got == data[mask, :])


def test_filterSubjects_multiple_columns():

    def gendata():
        colnames   = ['eid', '1-0.0', '1-1.0', '1-2.0', '2-0.0', '2-1.0']
        variables  = [0,      1,       1,       1,       2,       2]
        cols       = [Column(None, n, i, v) for i, (n, v) in
                      enumerate(zip(colnames, variables))]
        data       = np.random.randint(1, 10, (6, 500))
        data[0, :] = np.arange(1, 501)
        df         = pd.DataFrame({c : d for c, d in zip(colnames, data)})
        df         = df.set_index('eid')
        data       = data[1:, :].T
        return df, cols, data

    def all(s): return s.all(axis=1)
    def any(s): return s.any(axis=1)

    # combine vars with ncolumn
    # mismatch - should be ORed
    # within var, then combined
    df, cols, data = gendata()
    exprs = ['v1 > 2 && v2 < 7']
    exp   = any(data[:, :3] > 2) & any(data[:, 3:] < 7)
    got   = filter.filterSubjects(df, cols, subjectExprs=exprs)
    assert (got.index == (np.where(exp)[0] + 1)).all()

    # combine columns within var
    df, cols, data = gendata()
    exprs = ['all(v1 > 2) && any(v2 < 7)']
    exp = all(data[:, :3] > 2) & any(data[:, 3:] < 7)
    got = filter.filterSubjects(df, cols, subjectExprs=exprs)
    assert (got.index == (np.where(exp)[0] + 1)).all()

    # no combining columns - should
    # default to any
    df, cols, data = gendata()
    exprs = ['v1 > 6']
    exp = any(data[:, :3] > 6)
    got = filter.filterSubjects(df, cols, subjectExprs=exprs)
    assert (got.index == (np.where(exp)[0] + 1)).all()

    # multipler expressions - ORed together
    df, cols, data = gendata()
    exprs = ['v1 > 6', 'v2 < 4']
    exp = any(data[:, :3] > 6) | any(data[:, 3:] < 4)
    got = filter.filterSubjects(df, cols, subjectExprs=exprs)
    assert (got.index == (np.where(exp)[0] + 1)).all()


def test_filter_subjects_column_not_present():
    data       = np.random.randint(1, 10, (500, 11))
    index      = np.arange(1, 501)
    data[:, 0] = index
    colnames   = ['eid'] + ['{}-0.0'.format(i+1) for i in range(10)]
    cols       = [Column(None, n, i, i) for i, n in enumerate(colnames)]
    df         = pd.DataFrame(data, columns=colnames).set_index('eid')

    # expression is skipped if any variable is not present
    got1       = filter.filterSubjects(df, cols, subjectExprs=['v11 > 0'])
    got2       = filter.filterSubjects(df, cols, subjectExprs=['v9  < 0 || '
                                                               'v11 > 0'])

    assert (got1 == df).all().all()
    assert (got2 == df).all().all()
