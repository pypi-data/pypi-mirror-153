#!/usr/bin/env python
#
# test_metaproc.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import random
import textwrap as tw
from unittest import mock

import numpy as np

from .. import metaproc_functions as metaproc
from .. import hierarchy
from .. import custom

from . import clear_plugins, gen_DataTable, tempdir, patch_logging


@clear_plugins
@patch_logging
def test_codingDescriptionFromValue():

    custom.registerBuiltIns()

    with tempdir():
        descs = tw.dedent("""
        coding	meaning
        30	meaning 30
        40	meaning 40
        50	meaning 50
        20	meaning 20
        60	meaning 60
        10	meaning 10 hah
        """).strip()

        with open('coding123.txt', 'wt') as f:
            f.write(descs)

        dt = gen_DataTable([np.random.randint(1, 10, 10)])

        dt.vartable.loc[1, 'DataCoding'] = 123

        func = custom.get('metaproc', 'codingdesc')

        with mock.patch('funpack.coding.getCodingFilePath',
                        return_value='coding123.txt'):
            assert func(dt, 1, 30) == '30 - meaning 30'
            assert func(dt, 1, 10) == '10 - meaning 10 hah'


@clear_plugins
@patch_logging
def test_hierarchicalDescriptionFromX():

    custom.registerBuiltIns()

    with tempdir():
        data = tw.dedent("""
        coding\tmeaning\tnode_id\tparent_id
        a\ta desc\t5\t0
        b\tb desc\t1\t5
        c\tc desc\t3\t5
        d\td desc\t4\t3
        e\te desc\t2\t1
        """)

        with open('coding19.txt', 'wt') as f:
            f.write(data)

        dt = gen_DataTable([np.random.randint(1, 10, 10)])

        dt.vartable.loc[1, 'DataCoding'] = 123

        numfunc  = custom.get('metaproc', 'hierarchynumdesc')
        codefunc = custom.get('metaproc', 'hierarchycodedesc')

        with mock.patch('funpack.hierarchy.getHierarchyFilePath',
                        return_value='coding19.txt'):
            assert codefunc(dt, 1, 'a') == 'a - a desc'
            assert codefunc(dt, 1, 'c') == 'c - c desc'
            assert numfunc( dt, 1,  5)  == 'a - a desc'
            assert numfunc( dt, 1,  3)  == 'c - c desc'
