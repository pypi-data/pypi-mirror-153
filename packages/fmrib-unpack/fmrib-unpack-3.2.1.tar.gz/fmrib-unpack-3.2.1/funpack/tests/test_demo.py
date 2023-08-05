#!/usr/bin/env python
#
# test_demo.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import time
import json
import glob
import shutil
import sys
import os
import signal
import os.path as op
import itertools as it
import subprocess as sp
import multiprocessing as mp

from unittest import mock

import jinja2 as j2
import numpy as np

import notebook.notebookapp as notebookapp
import funpack.scripts.demo as ukbdemo


from . import tempdir


def test_demo():

    def nbfunc():
        # add some extra args for running within docker
        if op.exists('/.dockerenv'): args = ['--allow-root', '--ip=0.0.0.0']
        else:                        args = None

        with mock.patch('sys.argv', ['fmrib_unpack_demo']):
            ukbdemo.main(args)

    nbproc = mp.Process(target=nbfunc)
    nbproc.start()
    time.sleep(3)

    servers = notebookapp.list_running_servers()

    assert sum([s['pid'] == nbproc.pid for s in servers]) == 1
    for s in servers:
        if s['pid'] == nbproc.pid:
            notebookapp.shutdown_server(s)
            break

    os.kill(nbproc.pid, signal.SIGKILL)
    nbproc.join(0.5)
    assert not nbproc.is_alive()


def create_funpack_entrypoint(path):
    with open(path, 'wt') as f:
        f.write('#!/usr/bin/env bash\n')
        f.write('{} -m funpack "$@"\n'.format(sys.executable))
    os.chmod(path, 0o755)


def test_demo_commands():

    def eval_cmd(cmd, out, env):

        # TODO extract all funpack calls, and turn
        #      them into funpack.main function calls.
        result = sp.run(['bash', cmd], stdout=sp.PIPE, env=env)

        with open(out, 'rt') as f:
            out = f.read()
        assert result.returncode              == 0
        assert result.stdout.decode().strip() == out.strip()

    # Issues with pytest-cov 3.0.0 / coveragepy 6.2
    # cause coverage to spit out error information
    # in subprocess-called invocations. Disabling for
    # the time being.
    env = os.environ.copy()
    for k in list(env.keys()):
        if 'COVERAGE' in k or k.startswith('COV_'):
            env.pop(k)

    with tempdir() as td:
        td = op.realpath(td)
        gen_demo_tests(rundir=td)
        create_funpack_entrypoint(op.join(td, 'funpack'))
        create_funpack_entrypoint(op.join(td, 'fmrib_unpack'))

        env['PATH'] = op.pathsep.join((td, env['PATH']))

        demodir = op.join(op.dirname(__file__), '..', 'scripts', 'demo')

        for fname in glob.glob(op.join(demodir, '*.*')):
            shutil.copy(fname, td)

        commands = list(sorted(glob.glob('*_command.txt')))
        outputs  = list(sorted(glob.glob('*_output.txt')))

        for i, (cmd, out) in enumerate(zip(commands, outputs)):

            print('Command', i)
            print(open(cmd).read())
            print()

            eval_cmd(cmd, out, env)


def gen_demo_tests(outdir=None, rundir=None):

    if outdir is None: outdir = os.getcwd()
    if rundir is None: rundir = os.getcwd()

    demofile = op.join(op.dirname(__file__),
                       'funpack_demonstration_with_outputs.ipynb')
    with open(demofile, 'rt') as f:
        content = f.read()

    content = j2.Template(content)
    content = content.render(dir_prefix=rundir, op=op)
    nb      = json.loads(content)
    cells   = nb['cells']

    fname_prefix_format = '{{:0{}d}}'.format(
        int(np.ceil(np.log10(len(cells)))))

    i = 1
    for cell in cells:

        if cell['cell_type'] != 'code':
            continue

        source = cell['source']
        output = cell['outputs']

        # exclude some specific commands
        excludes = ['pygmentize',
                    'ls -l $ukbdir/configs/fmrib']

        if any([exc in line
                for exc, line
                in it.product(excludes, source)]):
            continue

        alloutput = []
        for o in output:
            if o['name'] == 'stdout':
                alloutput += o['text']
        output = alloutput

        cmd_file = '{}_command.txt'.format(
            fname_prefix_format.format(i))
        out_file = '{}_output.txt'.format(
            fname_prefix_format.format(i))

        # Todo abs paths in unknown var file output

        with open(op.join(outdir, cmd_file), 'wt') as f:
            f.write('#!/usr/bin/env bash\n')
            f.write('export PYTHONPATH="{}"\n'.format(
                op.join(op.dirname(__file__), '..', '..')))
            for line in source:
                # The demo uses an alias funpack='fmrib_unpack -q -ow'
                if line.startswith('funpack '):
                    line = line.replace('funpack ', 'funpack -q -ow ')
                    line = '{} -m '.format(sys.executable) + line
                f.write(line)
        with open(op.join(outdir, out_file), 'wt') as f:
            for line in output:
                f.write(line)

        i += 1
