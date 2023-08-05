#!/usr/bin/env python
#
# test_config.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import os.path as op

from unittest import mock

import funpack.config as config
import funpack.custom as custom

from . import clear_plugins, tempdir

@clear_plugins
def test_parseArgs_fixPath():

    custom.registerBuiltIns()

    fullpath = op.normpath(
        op.join(op.dirname(__file__), '..',
                'configs', 'fmrib', 'variables_clean.tsv'))
    relpath  = op.join('fmrib', 'variables_clean.tsv')
    dotpath  = 'fmrib.variables_clean'

    argv = ['-vf', fullpath,
            '-vf', relpath,
            '-vf', dotpath, 'output',  'input']

    args = config.parseArgs(argv)[0]

    assert args.variable_file == [fullpath, fullpath, fullpath]

@clear_plugins
def test_num_jobs():

    custom.registerBuiltIns()

    with mock.patch('multiprocessing.cpu_count', return_value=99):
        assert config.parseArgs('-nj -1 out in'.split())[0].num_jobs == 99
        assert config.parseArgs('-nj -5 out in'.split())[0].num_jobs == 99

    assert config.parseArgs('-nj 0 out in'.split())[0].num_jobs == 1
    assert config.parseArgs('-nj 1 out in'.split())[0].num_jobs == 1
    assert config.parseArgs('-nj 5 out in'.split())[0].num_jobs == 5


@clear_plugins
def test_multiple_config_file():

    custom.registerBuiltIns()
    with tempdir():

        with open('one.cfg',   'wt') as f:
            f.write('variable\t1\n')
            f.write('variable_file\tvf\n')
            f.write('processing_file\tpf1\n')
        with open('two.cfg',   'wt') as f:
            f.write('variable\t2\n')
            f.write('datacoding_file\tdf\n')
            f.write('processing_file\tpf2\n')
        with open('three.cfg', 'wt') as f:
            f.write('variable\t3\n')
            f.write('processing_file\tpf3\n')
        argv = '-cfg one.cfg -cfg two.cfg -cfg three.cfg out in'.split()
        args = config.parseArgsWithConfigFile(argv)[0]
        assert args.variable        == [1, 2, 3]
        assert args.variable_file   == ['vf']
        assert args.datacoding_file == ['df']
        assert args.processing_file ==  'pf3'


@clear_plugins
def test_recursive_config_file():

    custom.registerBuiltIns()
    with tempdir():

        with open('one.cfg',   'wt') as f:
            f.write('variable\t1\n')
            f.write('variable_file\tvf\n')
            f.write('processing_file\tpf1\n')
            f.write('config_file\ttwo.cfg\n')
        with open('two.cfg',   'wt') as f:
            f.write('variable\t2\n')
            f.write('datacoding_file\tdf\n')
            f.write('processing_file\tpf2\n')
            f.write('config_file\tthree.cfg\n')
            f.write('config_file\tfour.cfg\n')
        with open('three.cfg', 'wt') as f:
            f.write('variable\t3\n')
            f.write('processing_file\tpf3\n')
        with open('four.cfg', 'wt') as f:
            f.write('variable\t4\n')
            f.write('category_file\tcf\n')
            f.write('processing_file\tpf4\n')
        argv = '-cfg one.cfg out in'.split()
        args = config.parseArgsWithConfigFile(argv)[0]
        assert args.variable        == [1, 2, 3, 4]
        assert args.variable_file   == ['vf']
        assert args.datacoding_file == ['df']
        assert args.processing_file ==  'pf4'
        assert args.category_file   ==  'cf'
