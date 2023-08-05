#!/usr/bin/env python
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import os
import sys
import shutil
import tempfile
import os.path as op

import notebook.notebookapp as notebookapp
import bash_kernel.install  as bash_kernel_install


def create_funpack_entrypoint(path):
    with open(path, 'wt') as f:
        interpreter = sys.executable
        f.write('#!/usr/bin/env bash\n')
        f.write(f'{interpreter} -m funpack "$@"\n')
    os.chmod(path, 0o755)


def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    thisdir = op.abspath(op.dirname(__file__))
    nbdir   = op.join(thisdir, 'demo')
    bash_kernel_install.main([])

    with tempfile.TemporaryDirectory() as tmpdir:

        create_funpack_entrypoint(op.join(tmpdir, 'fmrib_unpack'))
        os.environ['PATH'] = op.pathsep.join((
            os.environ['PATH'], tmpdir))

        tmpdir = op.join(tmpdir, 'demo')
        shutil.copytree(nbdir, tmpdir)
        notebookapp.main(['--notebook-dir', tmpdir] + argv)


if __name__ == '__main__':
    main()
