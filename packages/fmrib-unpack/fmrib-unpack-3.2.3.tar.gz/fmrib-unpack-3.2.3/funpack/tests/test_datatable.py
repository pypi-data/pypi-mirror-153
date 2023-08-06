#!/usr/bin/env python
#
# test_datatable.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import multiprocessing as mp

import numpy as np
import pandas as pd

import funpack.datatable as datatable

from . import gen_DataTable, gen_tables, gen_columns, tempdir


def _parallel_task(dtable, factor):
    for col in dtable.dataColumns:
        flag = 'mul {}'.format(factor)
        dtable[:, col.name] = dtable[:, col.name] * factor
        dtable.addFlag(col, flag)

        if factor % 2: col.metadata = flag
        else:          col.metadata = None
    return dtable


def test_subtable_merge_columns():

    data      = np.random.randint(1, 10, (10, 4))
    dtable    = gen_DataTable(data)
    cols      = dtable.dataColumns
    subtables = [dtable.subtable([c]) for c in cols]
    factors   = np.arange(1, len(subtables) + 1)

    for col, fac in zip(cols, factors):
        dtable.addFlag(col, 'origflag')
        col.metadata = 'origmeta'

    with mp.Pool(8) as pool:
        subtables = pool.starmap(_parallel_task, zip(subtables, factors))

    for st in subtables:
        dtable.merge(st)

    for i, (col, fac) in enumerate(zip(dtable.dataColumns, factors)):
        expflag = 'mul {}'.format(fac)
        expdata = data[i, :] * fac

        assert np.all(dtable[:, col.name] == expdata)
        assert dtable.getFlags(col) == set(('origflag', expflag))
        if fac % 2: assert col.metadata == expflag
        else:       assert col.metadata == 'origmeta'


def test_DataTable_columns():
    with tempdir():
        data = np.random.randint(1, 100, (100, 5))
        data[:, 0] = np.arange(1, 101)
        cols = gen_columns(('eid', (1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0)))

        df = pd.DataFrame(data, columns=[c.name for c in cols]).set_index('eid')
        vt, pt, ct = gen_tables((1, 2, 3, 4))[:3]
        dt = datatable.DataTable(df, cols, vt, pt, ct)

        assert dt.allColumns   == cols
        assert dt.indexColumns == [cols[0]]
        assert dt.dataColumns  == cols[1:]

        data = np.random.randint(1, 100, (100, 6))
        data[:, 0] = np.repeat(np.arange(1, 51), 2)
        data[:, 1] = np.tile(np.array([0, 1]), 50)
        cols = gen_columns(('eid', 'visit', (1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0)))

        df = pd.DataFrame(data, columns=[c.name for c in cols]).set_index(['eid', 'visit'])
        dt = datatable.DataTable(df, cols, vt, pt, ct)
        assert dt.allColumns   == cols
        assert dt.indexColumns == cols[:2]
        assert dt.dataColumns  == cols[2:]
