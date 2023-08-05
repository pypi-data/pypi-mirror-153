#!/usr/bin/env python
#
# test_main_index_visits.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import textwrap  as tw
import itertools as it
import os.path   as op
import              os
import              shlex

from unittest import mock

import numpy as np
import pytest

import pandas as pd

import funpack.main       as main
import funpack.custom     as custom
import funpack.importing  as importing
import funpack.loadtables as loadtables
import funpack.expression as expression
import funpack.processing as processing

from . import (patch_logging,
               patch_base_tables,
               clear_plugins,
               tempdir,
               gen_tables,
               gen_DataTable,
               gen_test_data,
               gen_DataTableFromDataFrame)


@patch_logging
def test_main_indexVisits():
    with tempdir():
        data = tw.dedent("""
        eid,1-0.0,1-1.0,2-0.0,2-1.0,3-0.0,3-1.0,3-0.1
        1,10,20,30,40,50,60,70
        2,11,21,31,41,51,61,71
        3,12,22,32,42,52,62,72
        4,13,23,33,43,53,63,73
        5,14,24,34,44,54,64,74
        6,15,25,35,45,55,65,75
        """).strip()

        exp = tw.dedent("""
        eid,visit,1.0,2-0.0,2-1.0,3.0,3.1
        1,0,10,30,40,50,70
        1,1,20,,,60,
        2,0,11,31,41,51,71
        2,1,21,,,61,
        3,0,12,32,42,52,72
        3,1,22,,,62,
        4,0,13,33,43,53,73
        4,1,23,,,63,
        5,0,14,34,44,54,74
        5,1,24,,,64,
        6,0,15,35,45,55,75
        6,1,25,,,65,
        """).strip()

        vt, _, _, _            = gen_tables([1, 2, 3])
        vt.at[1, 'Instancing'] = 2
        vt.at[2, 'Instancing'] = 1
        vt.at[3, 'Instancing'] = 2
        vt.to_csv('variables.tsv', sep='\t')

        with open('data.csv', 'wt') as f: f.write(data)
        with open('exp.csv',  'wt') as f: f.write(exp)

        main.main('-iv -vf variables.tsv out.tsv data.csv'.split())

        got = pd.read_csv('out.tsv', sep='\t', index_col=(0, 1))
        exp = pd.read_csv('exp.csv', sep=',',  index_col=(0, 1))

        print(got)
        print(exp)

        assert (got.index   == exp.index)  .all()
        assert (got.columns == exp.columns).all()
        for col in got.columns:
            assert (got[col].dropna() == exp[col].dropna()).all()
