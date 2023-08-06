#!/usr/bin/env python


import random
import textwrap as tw
import os.path  as op
import contextlib as ctxlib

from unittest import mock

import numpy as np
import pandas as pd

import funpack.hierarchy as hierarchy

from . import (tempdir, gen_DataTable)


def test_getHierarchyFilePath():

    dt = gen_DataTable([np.random.randint(1, 10, 10)])

    dt.vartable.loc[1, 'DataCoding'] = 123

    exp = op.join(op.dirname(hierarchy.__file__),
                  'data', 'hierarchy', 'coding123.tsv')
    assert hierarchy.getHierarchyFilePath(dt, 1) == exp


@ctxlib.contextmanager
def patchDataType(dtype):
    with mock.patch('funpack.hierarchy.dataCodingType', return_value=dtype):
        yield


def test_loadHierarchyFile():

    hier = tw.dedent("""
    coding	meaning	node_id	parent_id
    30	meaning 30	3	1
    40	meaning 40	4	1
    50	meaning 50	5	4
    20	meaning 20	2	0
    60	meaning 60	6	2
    10	meaning 10	1	0
    """).strip()

    with tempdir(), patchDataType(int):

        with open('coding123.tsv', 'wt') as f:
            f.write(hier)

        h = hierarchy.loadHierarchyFile('coding123.tsv')

        assert h.parents(10) == []
        assert h.parents(20) == []
        assert h.parents(30) == [10]
        assert h.parents(40) == [10]
        assert h.parents(50) == [40, 10]
        assert h.parents(60) == [20]



def test_codeToNumeric():

    icd10code = hierarchy.HIERARCHY_DATA_NAMES['icd10']
    icd10hier = hierarchy.getHierarchyFilePath(coding=icd10code)
    icd10hier = hierarchy.loadHierarchyFile(icd10hier)
    codes     = list(random.sample(icd10hier.codings, 20)) + ['badcode']
    exp       = [icd10hier.index(c) for c in codes[:-1]] + [np.nan]

    conv = [hierarchy.codeToNumeric(c, coding=icd10code) for c in codes]

    exp  = np.array(exp)
    conv = np.array(conv)

    expna  = np.isnan(exp)
    convna = np.isnan(conv)

    assert np.all(     expna  ==       convna)
    assert np.all(exp[~expna] == conv[~convna])

    ncodes = [(code, ncode)
              for code, ncode
              in zip(codes, conv)
              if not pd.isna(ncode)]

    codes, ncodes = zip(*ncodes)
    codes = [c.lower() for c in codes]

    assert codes == [hierarchy.numericToCode(c, coding=icd10code).lower()
                     for c in ncodes]


def test_Hierarchy():
    with tempdir():
        data = tw.dedent("""
        coding\tmeaning\tnode_id\tparent_id
        a\ta desc\t5\t0
        b\tb desc\t1\t5
        c\tc desc\t3\t5
        d\td desc\t4\t3
        e\te desc\t2\t1
        """)

        with open('coding345.tsv', 'wt') as f:
            f.write(data)

        with patchDataType(str):
            h = hierarchy.loadHierarchyFile('coding345.tsv')

        assert h.index('a') == 5
        assert h.index('b') == 1
        assert h.index('c') == 3
        assert h.index('d') == 4
        assert h.index('e') == 2
        assert h.coding(1)  == 'b'
        assert h.coding(2)  == 'e'
        assert h.coding(3)  == 'c'
        assert h.coding(4)  == 'd'
        assert h.coding(5)  == 'a'

        assert h.parents(  'a') == []
        assert h.parents(  'b') == ['a']
        assert h.parents(  'c') == ['a']
        assert h.parents(  'd') == ['c', 'a']
        assert h.parents(  'e') == ['b', 'a']
        assert h.parentIDs( 5)  == []
        assert h.parentIDs( 1)  == [5]
        assert h.parentIDs( 3)  == [5]
        assert h.parentIDs( 4)  == [3, 5]
        assert h.parentIDs( 2)  == [1, 5]

        assert h.description('a') == 'a desc'
        assert h.description('b') == 'b desc'
        assert h.description('c') == 'c desc'
        assert h.description('d') == 'd desc'
        assert h.description('e') == 'e desc'

        h.set('a', 'meta', 'aa')
        h.set('b', 'meta', 'bb')
        h.set('c', 'meta', 'cc')
        h.set('d', 'meta', 'dd')
        h.set('e', 'meta', 'ee')

        assert h.get('a', 'meta') == 'aa'
        assert h.get('b', 'meta') == 'bb'
        assert h.get('c', 'meta') == 'cc'
        assert h.get('d', 'meta') == 'dd'
        assert h.get('e', 'meta') == 'ee'


def test_Hierarchy_non_sequential_ids():
    with tempdir():
        data = tw.dedent("""
        coding\tmeaning\tnode_id\tparent_id
        100\t100 desc\t550\t0
        200\t200 desc\t150\t550
        300\t300 desc\t350\t550
        400\t400 desc\t450\t350
        500\t500 desc\t250\t150
        """)

        with open('coding456.tsv', 'wt') as f:
            f.write(data)

        with patchDataType(str):
            h = hierarchy.loadHierarchyFile('coding456.tsv')

        assert h.index('100') == 550
        assert h.index('200') == 150
        assert h.index('300') == 350
        assert h.index('400') == 450
        assert h.index('500') == 250
        assert h.coding(150)  == '200'
        assert h.coding(250)  == '500'
        assert h.coding(350)  == '300'
        assert h.coding(450)  == '400'
        assert h.coding(550)  == '100'

        assert h.parents('100') == []
        assert h.parents('200') == ['100']
        assert h.parents('300') == ['100']
        assert h.parents('400') == ['300', '100']
        assert h.parents('500') == ['200', '100']
        assert h.parentIDs(550) == []
        assert h.parentIDs(150) == [550]
        assert h.parentIDs(350) == [550]
        assert h.parentIDs(450) == [350, 550]
        assert h.parentIDs(250) == [150, 550]

        assert h.description('100') == '100 desc'
        assert h.description('200') == '200 desc'
        assert h.description('300') == '300 desc'
        assert h.description('400') == '400 desc'
        assert h.description('500') == '500 desc'

        h.set('100', 'meta', 'aa')
        h.set('200', 'meta', 'bb')
        h.set('300', 'meta', 'cc')
        h.set('400', 'meta', 'dd')
        h.set('500', 'meta', 'ee')

        assert h.get('100', 'meta') == 'aa'
        assert h.get('200', 'meta') == 'bb'
        assert h.get('300', 'meta') == 'cc'
        assert h.get('400', 'meta') == 'dd'
        assert h.get('500', 'meta') == 'ee'
