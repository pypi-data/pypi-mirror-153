#!/usr/bin/env python
#
# metaproc_functions.py - Functions for manipulating column metadata.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains ``metaproc`` functions - functions for manipulating
column metadata.

Some :class:`.Column` instances have a ``metadata`` attribute, containing some
additional information about the column. The functions in this module can be
used to modify these metadata values. Currently, column metadata is only used
to generate a description of each column (via the ``--description_file``
command-line option).

All ``metaproc`` functions must accept three arguments:

 - The :class:`.DataTable`

 - The variable ID associated with the column. This may be ``None``, if the
   column has been newly added, and is not associated with any other variable.

 - The metadata value.
"""


import pandas as pd

from . import util
from . import custom
from . import coding
from . import hierarchy


@custom.metaproc('codingdesc')
def codingDescriptionFromValue(dtable, vid, val):
    """Generates a description for a value from a specific data coding. """
    fname = coding.getCodingFilePath(dtable, vid)
    descs = coding.loadCodingFile(fname)

    # Reverse any categorical recoding
    # that may have been applied, so we
    # can get at the original value.
    # We make the assumption here that
    # metaproc functions are called
    # after categorical recoding.
    raw = dtable.vartable.at[vid, 'RawLevels']
    new = dtable.vartable.at[vid, 'NewLevels']

    if not pd.isna(new) and val in new:
        recoding = dict(zip(new, raw))
        val      = recoding[val]

    desc  = descs['meaning'][val]
    return '{} - {}'.format(val, desc)


@custom.metaproc('hierarchynumdesc')
def hierarchicalDescriptionFromNumeric(dtable, vid, val):
    """Generates a description for a numeric hierarchical code. """
    val  = hierarchy.numericToCode(val, dtable=dtable, vid=vid)
    hier = hierarchy.getHierarchyFilePath(dtable, vid)
    hier = hierarchy.loadHierarchyFile(hier)
    desc = hier.description(val)
    return '{} - {}'.format(val, desc)


@custom.metaproc('hierarchycodedesc')
def hierarchicalDescriptionFromCode(dtable, vid, val):
    """Generates a description for a hierarchical code. """
    hier = hierarchy.getHierarchyFilePath(dtable=dtable, vid=vid)
    hier = hierarchy.loadHierarchyFile(hier)
    desc = hier.description(val)
    return '{} - {}'.format(val, desc)
