#!/usr/bin/env python

import shutil
import os.path as op

from setuptools import setup, find_packages, Command

basedir = op.dirname(__file__)


with open(op.join(basedir, 'requirements.txt'), 'rt') as f:
    install_requires = [line.strip() for line in f.readlines()]
    install_requires = [line for line in install_requires if line != '']


with open(op.join(basedir, 'requirements-demo.txt'), 'rt') as f:
    demo_requires = [line.strip() for line in f.readlines()]
    demo_requires = [line for line in demo_requires if line != '']


with open(op.join(basedir, 'requirements-test.txt'), 'rt') as f:
    test_requires = [line.strip() for line in f.readlines()]
    test_requires = [line for line in demo_requires if line != '']


extras_require = {
    'demo' : demo_requires,
    'test' : test_requires
}


version = {}
with open(op.join(basedir, 'funpack', '__init__.py')) as f:
    for line in f:
        if line.startswith('__version__ = '):
            exec(line, version)
            break
version = version['__version__']


with open(op.join(basedir, 'README.rst'), 'rt') as f:
    readme = f.read()


class doc(Command):
    """Build the API documentation. """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        docdir  = op.join(op.dirname(__file__), 'doc')
        destdir = op.join(docdir, 'html')

        if op.exists(destdir):
            shutil.rmtree(destdir)

        import funpack.scripts.generate_notebooks as gennb
        import sphinx.cmd.build as sphinx_build
        gennb.main()
        sphinx_build.main([docdir, destdir])

setup(
    name='fmrib-unpack',
    version=version,
    description='The FMRIB UKBiobank Normalisation, Parsing '
                'And Cleaning Kit',
    long_description=readme,
    url='https://git.fmrib.ox.ac.uk/fsl/funpack',
    author='Paul McCarthy',
    author_email='pauldmccarthy@gmail.com',
    license='Apache License Version 2.0',

    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

    install_requires=install_requires,
    extras_require=extras_require,
    packages=find_packages(),
    include_package_data=True,

    cmdclass={'doc' : doc},

    entry_points={
        'console_scripts' : [
            'fmrib_unpack      = funpack.main:main',
            'fmrib_unpack_demo = funpack.scripts.demo:main',
        ]
    }
)
