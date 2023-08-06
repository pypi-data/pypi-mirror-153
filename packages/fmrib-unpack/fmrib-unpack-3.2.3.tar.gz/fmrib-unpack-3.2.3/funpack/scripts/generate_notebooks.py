#!/usr/bin/env python
#
# Convert funpack/scripts/demo/funpack_demonstration.md to
# funpack/scripts/demo/funpack_demonstration.ipynb, then execute it to
# generate funpack/tests/funpack_demonstration_with_outputs.ipynb,
# and doc/demo.rst
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import subprocess as sp
import os.path    as op
import base64     as b64
import               os
import               sys
import               json
import               shlex

import bash_kernel.install as bash_kernel_install

import funpack.scripts.demo  as     demo
import funpack.tests         as     tests
from   funpack.tests         import tempdir


METADATA = {
    'kernelspec' : {
        'display_name' : 'Bash',
        'language'     : 'bash',
        'name'         : 'bash'
    },
    'language_info' : {
        'codemirror_mode' : 'shell',
        'file_extension'  : '.sh',
        'mimetype'        : 'text/x-sh',
        'name'            : 'bash'
    }
}


def create_funpack_executable():
    with open('funpack', 'wt') as f:
        f.write('#!/usr/bin/env bash\n')
        f.write(f'{sys.executable} -m funpack "$@"\n')
    os.chmod('funpack', 0o755)


def encode(imagefile):
    with open(imagefile, 'rb') as f:
        data = f.read()
    return b64.b64encode(data).decode('ascii')


def patch_image(notebook, imagefile):
    filename = op.basename(imagefile)
    found    = False
    for cell in notebook['cells']:
        for lineidx, line in enumerate(cell['source']):
            if f'({filename})' in line:
                found = True
                break
        if found:
            break
    else:
        raise RuntimeError(f'Cannot find cell which refers to {filename}!')

    line = line.replace(f'({filename})', f'(attachment:{filename})')
    cell['source'][lineidx] = line

    cell['attachments'] = {filename : {'image/png' : encode(imagefile)}}


def markdown_to_notebook(demodir, mdfile, nbfile):
    sp.run(shlex.split(f'notedown "{mdfile}" -o "{nbfile}"'), check=True)

    with open(nbfile, 'rt') as f:
        notebook = json.loads(f.read())

    notebook['metadata'] = METADATA

    images = ['win.png', 'coding.png']
    for image in images:
        image = op.join(demodir, image)
        patch_image(notebook, image)

    with open(nbfile, 'wt') as f:
        f.write(json.dumps(notebook, indent=2))


def execute_notebook(nbfile, outfile):
    bash_kernel_install.main([])
    with tempdir():
        create_funpack_executable()
        cmd = f'jupyter-nbconvert {nbfile} --execute ' \
               '--ExecutePreprocessor.kernel_name=bash ' \
              f'--to=notebook --output={outfile}'
        env         = os.environ.copy()
        env['PATH'] = op.pathsep.join((os.getcwd(), env.get('PATH', '')))
        sp.run(shlex.split(cmd), check=True, env=env)


def truncate_long_output_cells(infile, outfile, maxlines=50):
    with open(infile, 'rt') as f:
        notebook = json.loads(f.read())

    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        if 'outputs' not in cell:
            continue
        for output in cell['outputs']:
            if len(output['text']) > maxlines:
                ntrunc = len(output['text']) - maxlines
                print('truncating cell', output['text'][0])
                output['text'] = output['text'][:50]
                output['text'].append('...\n')
                output['text'].append(f'[Long output - {ntrunc} '
                                      'more lines hidden]\n')
                output['text'].append('...\n')

    with open(outfile, 'wt') as f:
        f.write(json.dumps(notebook, indent=2))


def main():

    # get FUNPACK root dir from funpack/scripts
    basedir  = op.abspath(op.join(op.dirname(__file__), '..', '..'))
    demodir  = op.abspath(op.join(op.dirname(demo.__file__), 'demo'))
    testdir  = op.abspath(op.dirname(tests.__file__))
    mdfile   = op.join(demodir, 'funpack_demonstration.md')
    nbfile   = op.join(demodir, 'funpack_demonstration.ipynb')
    exfile   = op.join(testdir, 'funpack_demonstration_with_outputs.ipynb')
    docfile  = op.join(basedir, 'doc', 'demo.ipynb')

    print(f'Converting {mdfile} to {nbfile}')
    markdown_to_notebook(demodir, mdfile, nbfile)

    print(f'Executing {nbfile}, and saving to {exfile}...')
    execute_notebook(nbfile, exfile)

    print(f'Copying executed notebook into doc/ directory...')
    truncate_long_output_cells(exfile, docfile)


if __name__ == '__main__':
    main()
