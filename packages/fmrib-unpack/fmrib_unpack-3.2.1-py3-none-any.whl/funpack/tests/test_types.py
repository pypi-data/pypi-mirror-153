#!/usr/bin/env python

import textwrap as tw

import numpy  as np
import pandas as pd

import pytest

from . import tempdir, patch_logging

import funpack.main   as main
import funpack.custom as custom
import funpack.config as config



def test_InternalType_trustTypes():
    _test_InternalType(True)

def test_InternalType_no_trustTypes():
    _test_InternalType(False)


@patch_logging
def _test_InternalType(trustTypes):


    data = tw.dedent("""
    eid\t1-0.0\t2-0.0\t3-0.0\t4-0.0\t5-0.0
    1\t1000\t2\t3\t4\t5
    2\t1\t2\t3\t4\t5
    3\t1\t2\t3\t4\t5
    4\t1\t2\t3\t4\t5
    5\t1\t2\t3\t4\t5
    """).strip()

    vartable = tw.dedent("""
    ID\tInternalType
    1\tint8
    2\tfloat64
    3\tuint32
    4\tfloat32
    5\tint16
    """).strip()

    with tempdir():

        with open('data.txt', 'wt') as f:
            f.write(data)
        with open('vartable.txt', 'wt') as f:
            f.write(vartable)

        custom.registerBuiltIns()
        args   = '-nb -vf vartable.txt out.txt data.txt'
        if trustTypes:
            args += ' -tt'
        args   = config.parseArgs(args.split())[0]
        dtable = main.doImport(args, None)[0]

        assert dtable[:, '1-0.0'].dtype == np.int8
        assert dtable[:, '2-0.0'].dtype == np.float64
        assert dtable[:, '3-0.0'].dtype == np.uint32
        assert dtable[:, '4-0.0'].dtype == np.float32
        assert dtable[:, '5-0.0'].dtype == np.int16

        # The low 8 bits of 1000 == -24
        # when interpreted as int8
        assert dtable[1, '1-0.0'] == -24


@patch_logging
def test_trustTypes():

    data = tw.dedent("""
    eid\t1-0.0
    1\t1
    2\t1
    3\tbadval
    """).strip()

    vartable = tw.dedent("""
    ID\tInternalType
    1\tfloat32
    """).strip()

    with tempdir():

        with open('data.txt', 'wt') as f:
            f.write(data)
        with open('vartable.txt', 'wt') as f:
            f.write(vartable)

        custom.registerBuiltIns()

        args = '-nb -tt -vf vartable.txt out.txt data.txt'
        args = config.parseArgs(args.split())[0]

        with pytest.raises(ValueError):
            dtable = main.doImport(args, None)[0]

        args   = '-nb -vf vartable.txt out.txt data.txt'
        args   = config.parseArgs(args.split())[0]
        dtable = main.doImport(args, None)[0]

        assert dtable[1, '1-0.0'] == 1
        assert dtable[2, '1-0.0'] == 1
        assert pd.isna(dtable[3, '1-0.0'])


@patch_logging
def test_largevals():

    # Some random values which cannot be
    # represented with float32 data type
    vals = np.array([10001249182,  48192124975, 14328901242])

    data = 'eid\t1-0.0\n'
    for i, v in enumerate(vals):
        data += '{}\t{}\n'.format(i, v)



    with tempdir():

        with open('data.txt', 'wt') as f:
            f.write(data)

        # If we specify the variable as an integer,
        # funpack will default to float32, and the
        # values will be misinterpreted
        vartable = 'ID\tType\n1\tinteger'
        with open('vartable.txt', 'wt') as f:
            f.write(vartable)

        custom.registerBuiltIns()

        args = '-nb -vf vartable.txt out.txt data.txt'
        args = config.parseArgs(args.split())[0]
        dtable = main.doImport(args, None)[0]

        assert not np.any(dtable[:, '1-0.0'] == vals)

        # But we can use InternalType to
        # specify a suitable storage type
        vartable = 'ID\tType\tInternalType\n1\tinteger\tfloat64'
        with open('vartable.txt', 'wt') as f:
            f.write(vartable)

        args   = '-nb -vf vartable.txt out.txt data.txt'
        args   = config.parseArgs(args.split())[0]
        dtable = main.doImport(args, None)[0]

        assert np.all(dtable[:, '1-0.0'] == vals)
