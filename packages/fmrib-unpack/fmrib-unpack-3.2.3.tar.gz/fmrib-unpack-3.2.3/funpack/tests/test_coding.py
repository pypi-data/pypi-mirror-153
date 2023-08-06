#!/usr/bin/env python
#
# test_coding.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import textwrap as tw
import os.path  as op

import numpy as np

import funpack.coding as coding

from . import (tempdir, gen_DataTable)


def test_getCodingFilePath():

    dt = gen_DataTable([np.random.randint(1, 10, 10)])
    dt.vartable.loc[1, 'DataCoding'] = 4
    exp = op.join(op.dirname(coding.__file__), 'data', 'coding', 'coding4.tsv')

    assert coding.getCodingFilePath(dt, 1)    == exp
    assert coding.getCodingFilePath(coding=4) == exp


def test_loadCodingFile():
    descs = tw.dedent("""
    coding	meaning
    30	meaning 30
    40	meaning 40
    50	meaning 50
    20	meaning 20
    60	meaning 60
    10	meaning 10
    """).strip()

    with tempdir():
        with open('descs.txt', 'wt') as f:
            f.write(descs)
        d = coding.loadCodingFile('descs.txt')
        assert d.loc[30, 'meaning'] == 'meaning 30'
