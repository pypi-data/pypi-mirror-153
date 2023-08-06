#!/usr/bin/env python
#
# test_util.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import multiprocessing as mp
from unittest import mock

import pytest

import funpack.util as util

from . import tempdir, patch_logging


def test_parseMatlabRange():
    tests = [
        ('1',      [1]),
        ('1:10',   list(range(1, 11))),
        ('1:2:10', [1, 3, 5, 7, 9]),
        ('10:-1:1', list(range(10, 0, -1))),
        ('10:-2:0', [10, 8, 6, 4, 2, 0]),
    ]

    for rng, exp in tests:
        assert util.parseMatlabRange(rng) == exp

    with pytest.raises(ValueError): util.parseMatlabRange('1:')
    with pytest.raises(ValueError): util.parseMatlabRange('1:1:')
    with pytest.raises(ValueError): util.parseMatlabRange('1:1:1:')
    with pytest.raises(ValueError): util.parseMatlabRange('1:1:1:1')
    with pytest.raises(ValueError): util.parseMatlabRange('abcde')
    with pytest.raises(ValueError): util.parseMatlabRange('a:b')
    with pytest.raises(ValueError): util.parseMatlabRange('a:b:c')


def test_parseColumnName():

    tests = [

        ('0-0.0',       ( 0,   0,  0)),
        ('1-1.1',       ( 1,   1,  1)),
        ('10-10.10',    (10,  10, 10)),
        ('1--1.1',      ( 1,  -1,  1)),
        ('10--10.10',   (10, -10, 10)),
        ('1-1.ABC',     ( 1,   1, 'ABC')),
        ('1-1.ABC.E',   ( 1,   1, 'ABC.E')),
        ('1-1.ABC E',   ( 1,   1, 'ABC E')),
        ('f.1.1.1',     ( 1,   1,  1)),
        ('f.10.10.10',  (10,  10, 10)),
        ('f.1..1.1',    ( 1,  -1,  1)),
        ('f.10..10.10', (10, -10, 10)),
        ('1.1',         ( 1,   0,  1)),
        ('1.ABC',       ( 1,   0, 'ABC')),
        ('1.ABC.E',     ( 1,   0, 'ABC.E')),
        ('1.ABC E',     ( 1,   0, 'ABC E')),
    ]

    for col, exp in tests:
        assert util.parseColumnName(col) == exp

    with pytest.raises(ValueError): util.parseColumnName('eid')
    with pytest.raises(ValueError): util.parseColumnName('f.eid')
    with pytest.raises(ValueError): util.parseColumnName('abc')
    with pytest.raises(ValueError): util.parseColumnName('10')
    with pytest.raises(ValueError): util.parseColumnName('10-')
    with pytest.raises(ValueError): util.parseColumnName('10-1')
    with pytest.raises(ValueError): util.parseColumnName('10-1-2')
    with pytest.raises(ValueError): util.parseColumnName('f.a')
    with pytest.raises(ValueError): util.parseColumnName('f.a.b')
    with pytest.raises(ValueError): util.parseColumnName('f.a.b.c')
    with pytest.raises(ValueError): util.parseColumnName('f.10.')
    with pytest.raises(ValueError): util.parseColumnName('f.10.10.')
    with pytest.raises(ValueError): util.parseColumnName('f.10.10.10.')
    with pytest.raises(ValueError): util.parseColumnName('f.10.10.10.10')
    with pytest.raises(ValueError): util.parseColumnName('f..10')
    with pytest.raises(ValueError): util.parseColumnName('f.10.10..10')


def test_generateColumnName():

    tests = [

        (( 0,   0,  0), '0-0.0'),
        (( 1,   1,  1), '1-1.1'),
        ((10,  10, 10), '10-10.10'),
        (( 1,  -1,  1), '1--1.1'),
        ((10, -10, 10), '10--10.10'),
    ]

    for var, exp in tests:
        assert util.generateColumnName(*var) == exp


@patch_logging
def test_timed():
    with util.timed('abc'):
        pass
    with util.timed('abc'):
        pass
    with util.timed('abc', fmt='abc %s %s'):
        pass
    with util.timed(fmt='abc %s %s'):
        pass


@patch_logging
def test_wc():
    text = '1\n2\n3\n4\n5\n'

    with tempdir():
        with open('file.txt', 'wt') as f:
            f.write(text)

        assert util.wc('file.txt') == 5

        with mock.patch('shutil.which', return_value=None):
            assert util.wc('file.txt') == 5


@patch_logging
def test_cat():

    f1  = '1\n2\n3\n'
    f2  = '4\n5\n6\n'
    f3  = '7\n8\n9\n'
    exp = f1 + f2 + f3

    with tempdir():
        with open('f1.txt', 'wt') as f: f.write(f1)
        with open('f2.txt', 'wt') as f: f.write(f2)
        with open('f3.txt', 'wt') as f: f.write(f3)

        util.cat(['f1.txt', 'f2.txt', 'f3.txt'], 'out1.txt')

        with mock.patch('shutil.which', return_value=None):
            util.cat(['f1.txt', 'f2.txt', 'f3.txt'], 'out2.txt')

        assert open('out1.txt').read() == exp
        assert open('out2.txt').read() == exp


def _checkproc(i):
    return util.inMainProcess()


def test_inMainProcess():
    pool = mp.Pool(8)
    assert util.inMainProcess()
    assert not any(pool.map(_checkproc, range(16)))
