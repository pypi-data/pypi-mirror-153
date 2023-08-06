#!/usr/bin/env python
#
# coding.py - Loading files which contain descriptions for data coding values.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains the :func:`loadCodingFile` function, which can be used
to load descriptions of the values for a given data coding.


The data coding information for some data codings in the UKBiobank is stored
in ``funpack/data/coding/`` - these files are available from the UKBiobank
showcase at https://biobank.ctsu.ox.ac.uk/crystal/schema.cgi.
"""


import os.path as op

import pandas  as pd


def getCodingFilePath(dtable=None, vid=None, coding=None):
    """Return a path to the data coding file for the given ``vid``.

    Pass the path to :func:`loadCodingFile` to load it. The returned path
    is not guaranteed to exist.

    :arg dtable: The :class:`.DataTable`
    :arg vid:    The variable ID
    :return:     A path to the relevant data coding file.
    """

    codingdir = op.join(op.dirname(__file__), 'data', 'coding')

    if (dtable is not None) and (vid is not None):
        coding = dtable.vartable.loc[vid, 'DataCoding']

    elif coding is None:
        raise ValueError('Either a datatable+vid, or a data '
                         'coding, must be specified')

    return op.join(codingdir, 'coding{}.tsv'.format(int(coding)))


def loadCodingFile(fname):
    """Loads the given data coding description file.

    The descriptions are returned in a ``pandas.DataFrame``, with the coding
    values as the index, and a single column called ``meaning``, containing
    the descriptions for each value.

    :arg fname: Path to a data coding file
    :return:    A ``DataFrame`` containing descriptions
    """
    return pd.read_csv(fname, delimiter='\t', index_col=0)
