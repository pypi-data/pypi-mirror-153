#!/usr/bin/env python
#
# test_importing_reindex.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import io
import textwrap as tw

import pandas as pd

from funpack.importing import reindex
from funpack.importing import core
from funpack           import fileinfo

from . import gen_tables, gen_columns, tempdir


def test_genReindexedColumns():

    vartable = gen_tables([1, 2, 3])[0]
    cols     = gen_columns(['eid',
                            (1, 0, 0), (1, 1, 0),
                            (2, 0, 0), (2, 1, 0),
                            (2, 0, 1), (2, 1, 1),
                            (3, 0, 0), (3, 1, 0), (3, 2, 0)])

    vartable.loc[:, 'Instancing'] = 1
    got1 = reindex.genReindexedColumns(cols, vartable)
    got2 = reindex.genReindexedColumns(cols, vartable, onlyRealVisits=False)
    vartable.loc[:, 'Instancing'] = 2
    got3 = reindex.genReindexedColumns(cols, vartable)
    vartable.loc[2, 'Instancing'] = 1
    got4 = reindex.genReindexedColumns(cols, vartable)

    assert got1 == (None, None, None)

    exp2cols = gen_columns(['eid', 'visit',
                            (1, None, 0),
                            (2, None, 0),
                            (2, None, 1),
                            (3, None, 0)])
    exp2map = [2, 2, 3, 3, 4, 4, 5, 5, 5]
    exp2map = {cols[i + 1] : exp2cols[ci] for i, ci in enumerate(exp2map)}
    assert got2[0] == exp2cols
    assert got2[1] == exp2map
    assert got2[2] == {0, 1, 2}

    assert got3[0] == exp2cols
    assert got3[1] == exp2map
    assert got3[2] == {0, 1, 2}

    exp4cols = gen_columns(['eid', 'visit',
                            (1, None, 0),
                            (2, 0, 0),
                            (2, 1, 0),
                            (2, 0, 1),
                            (2, 1, 1),
                            (3, None, 0)])
    exp4map = [2, 2, 3, 4, 5, 6, 7, 7, 7]
    exp4map = {cols[i + 1] : exp4cols[ci] for i, ci in enumerate(exp4map)}

    assert got4[0] == exp4cols
    assert got4[1] == exp4map
    assert got4[2] == {0, 1, 2}


def test_reindexByVisit():
    data = tw.dedent("""
    eid,1-0.0,1-1.0,2-0.0,2-1.0,3-0.0,3-1.0,3-0.1
    1,10,20,30,40,50,60,70
    2,11,21,31,41,51,61,71
    3,12,22,32,42,52,62,72
    4,13,23,33,43,53,63,73
    5,14,24,34,44,54,64,74
    6,15,25,35,45,55,65,75
    """).strip()
    vartable = gen_tables([1, 2, 3])[0]
    oldcols  = gen_columns(['eid',
                            (1, 0, 0), (1, 1, 0),
                            (2, 0, 0), (2, 1, 0),
                            (3, 0, 0), (3, 1, 0),
                            (3, 0, 1)])

    olddf   = pd.read_csv(io.StringIO(data), sep=',', index_col=0)
    newcols = reindex.genReindexedColumns(oldcols, vartable)
    newdf   = reindex.reindexByVisit(olddf, oldcols, *newcols)

    for c in oldcols[1:]:
        newname = '{}.{}'.format(c.vid, c.instance)
        slc     = ((slice(None), c.visit), newname)
        oldvals = newdf.loc[slc]
        newvals = olddf.loc[:, c.name]

        assert (oldvals.index.get_level_values(0) == newvals.index).all()

        assert (oldvals.values == newvals.values).all()


def test_importData_indexVisits():
    data = tw.dedent("""
    eid,1-0.0,1-1.0,2-0.0,2-1.0,3-0.0,3-1.0,3-0.1
    1,10,20,30,40,50,60,70
    2,11,21,31,41,51,61,71
    3,12,22,32,42,52,62,72
    4,13,23,33,43,53,63,73
    5,14,24,34,44,54,64,74
    6,15,25,35,45,55,65,75
    """).strip()
    vt, pt, ct = gen_tables([1, 2, 3])[:3]
    oldcols = gen_columns(['eid',
                           (1, 0, 0), (1, 1, 0),
                           (2, 0, 0), (2, 1, 0),
                           (3, 0, 0), (3, 1, 0),
                           (3, 0, 1)])
    newcols, oldnewmap = reindex.genReindexedColumns(oldcols, vt)[:2]
    for c in newcols:
        c.datafile = 'data.csv'

    with tempdir():
        with open('data.csv', 'wt') as f:
            f.write(data)

        finfo = fileinfo.FileInfo('data.csv')
        olddf = pd.read_csv('data.csv', sep=',', index_col=0)
        dt = core.importData(finfo,
                             vt, pt, ct,
                             indexVisits=True)[0]

        assert dt.allColumns == newcols

        for oldcol, newcol in oldnewmap.items():
            old = olddf.loc[:,                           oldcol.name]
            new = dt[       (slice(None), oldcol.visit), newcol.name]
            assert (old.values == new.values).all()
