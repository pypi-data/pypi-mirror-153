#!/usr/bin/env python
#
# hierarchy.py - Functions and data structures for working with hierarchical
#                variables.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains functions and data structures for working with
hierarchical variables.


The :func:`loadHierarchyFile` function will read hierarchy information for
one variable from a text file, and return a :class:`Hierarchy` object.


The :class:`Hierarchy` class allows the hierarchy information about a variable
to be queried.


The hierarchy information for all hierarchical variables in the UKBiobank is
stored in ``funpack/data/hierarchy/`` - these files are available from the
UKBiobank showcase at https://biobank.ctsu.ox.ac.uk/crystal/schema.cgi.
"""


import os.path     as op
import functools   as ft
import dataclasses as dc

import pandas      as pd
import numpy       as np

from typing import Any


HIERARCHY_DATA_NAMES = {
    'icd10' : 19,
    'icd9'  : 87,
    'opcs4' : 240,
    'opcs3' : 259,
}
"""This dictionary contains some UK Biobank hierarchical data codings which
can be looked up by name with the :func:`getHierarchyFilePath` function.
"""


class CircularError(Exception):
    """Error raised by the :meth:`Hierarchy.parents` method in the event
    that a circular relationship is detected in a hierarchy.
    """


@ft.lru_cache()
def loadEncodingTable():
    """Loads the encoding.txt file built into funpack, which contains
    information about all UK Biobank encodings.
    """
    datadir   = op.join(op.dirname(__file__), 'data')
    encodings = op.join(datadir, 'encoding.txt')
    encodings = pd.read_csv(encodings, sep='\t', index_col='encoding_id')
    return encodings


def dataCodingType(coding):
    """Returns a data type suitable for representing values in the given
    encoding.
    """
    encodings = loadEncodingTable()
    typecode  = encodings.loc[coding, 'coded_as']

    # the coded_as column conains a numeric ID
    # for each encoding, denoting its type. The
    # codes are the same as those used in
    # field.txt (see loadtables.loadTableBases).
    dtypes = {
        11 : int,
        21 : int,
        31 : float,
        41 : str,
        51 : str
    }
    return dtypes.get(typecode, str)


def getHierarchyFilePath(dtable=None,
                         vid=None,
                         name=None,
                         coding=None):
    """Return a path to the file containing hierarchy information for the
    specified variable/name. Pass the path to the :func:`loadHierarchyFile`
    function to load it.

    Hierarchy files can be looked up with one of the following methods, in
    order of precedence:

     1. By specifying a data coding (``coding``). This takes precedence.
     2. By specifying a ``name`` which is present in the
        :attr:`HIERARCHY_DATA_NAMES`.
     3. By passing a :class:`.DataTable` (``dtable``) and variable ID (``vid``)

    Te recognised data type names for use with the second method are listed in
    the :attr:`HIERARCHY_DATA_NAMES` dictionary.

    A :exc:`ValueError` is raised if the variable is unknown, or does not
    have a listed data coding.

    The returned path is not guaranteed to exist.

    :arg dtable: The :class:`.DataTable`
    :arg vid:    Variable ID
    :arg name:   Data coding name
    :arg coding: Data coding ID
    :returns:    A path to the relevant hierarchical coding file.
    """

    if coding is None:
        if name is not None:
            coding = HIERARCHY_DATA_NAMES[name.lower()]
        elif (dtable is not None) and (vid is not None):
            try:
                coding = int(dtable.vartable.loc[vid, 'DataCoding'])
            except Exception:
                raise ValueError('Variable {} is unknown or does not '
                                 'have a data coding'.format(vid))
    if coding is None:
        raise ValueError('A coding, name, or dtable+vid must be specified')

    hierdir = op.join(op.dirname(__file__), 'data', 'hierarchy')
    return op.join(hierdir, 'coding{}.tsv'.format(int(coding)))


@ft.lru_cache()
def loadHierarchyFile(fname):
    """Reads the hierarchy information for a variable from the given file.

    ``fname`` is assumed to refer to a tab-separated file containing
    the following columns:

      - ``coding``:    A variable value (not necessarily unique)
      - ``meaning``:   Description
      - ``node_id``:   Unique numeric identifier for each node
      - ``parent_id``: Identifier of each node's parent

    It is assumed that all codings have a unique ``node_id``. Top-level parent
    nodes (nodes with no parent of their own) often have an ID of 0, although
    this is not assumed.

    :arg fname: File containing hierarchy information for one variable
    :returns:   A :class:`Hierarchy` object.
    """

    # get the encoding ID fromn "coding<id>.tsv",
    # and look up a suitable data type
    encoding  = int(op.basename(fname)[6:-4])
    dtype     = {'coding' : dataCodingType(encoding)}

    # load the hierarchy encoding file, ensuring
    # that the coding values are converted
    data      = pd.read_csv(fname, sep='\t', index_col=False, dtype=dtype)
    codings   = data['coding']   .values
    meanings  = data['meaning']  .values
    nodeIds   = data['node_id']  .values
    parentIds = data['parent_id'].values
    return Hierarchy(nodeIds, parentIds, codings, meanings)


def codeToNumeric(code,
                  name=None,
                  dtable=None,
                  vid=None,
                  coding=None,
                  hier=None):
    """Converts a hierarchical code into a numeric version. See the
    :func:`getHierarchyFilePath` for information on the arguments.

    Some hierarchical codings in the UKB do not have unique coding values for
    parent/non-leaf nodes. If this function is passed such a value, ``np.nan``
    is returned.

    :arg code:   Code to convert
    :arg name:   Data coding name
    :arg dtable: The :class:`.DataTable`
    :arg vid:    Variable ID
    :arg coding: Data coding ID
    :arg hier:   A :class:`Hierarchy` instance which, if provided, will
                 be used instead of loading one from file using the other
                 arguments.
    """
    # We use the node IDs defined in
    # the hierarchy file as the
    # numeric version of each coding.
    if hier is None:
        hier = getHierarchyFilePath(dtable, vid, name, coding)
        hier = loadHierarchyFile(hier)

    try:
        return int(hier.index(code))
    except KeyError:
        return np.nan


def numericToCode(code, name=None, dtable=None, vid=None, coding=None):
    """Converts a numeric hierarchical code into its original version

    :arg code:   Code to convert
    :arg name:   Data coding name
    :arg dtable: The :class:`.DataTable`
    :arg vid:    Variable ID
    :arg coding: Data coding ID
    """
    hier = getHierarchyFilePath(dtable, vid, name, coding)
    hier = loadHierarchyFile(hier)

    try:
        return hier.coding(int(code))
    except KeyError:
        return 'NaN'


@dc.dataclass
class Node:
    """Represnts a node in a hierarchical encoding. Used by the
    :class:`Hierarchy` class.
    """
    node_id:   int
    parent_id: int
    coding:    Any
    attrs:     dict


class Hierarchy:
    """The ``Hierarchy`` class allows information in a hierarchical variable to
    be queried. The :meth:`parents` method will return all parents in the
    hierarchy for a given value (a.k.a. *coding*), and the :meth:`description`
    method will return the description for a value.

    Additional metadata can be added and retrieved for codings via the
    :meth:`set` and :meth:`get` methods.
    """


    def __init__(self, nodes, parents, codings, descs):
        """Create a ``Hierarchy`` object.

        :arg nodes:   Node IDs. Assumed to be unique.
        :arg parents: Parent IDs for each node.
        :arg codings: Value/coding for each node.
        :arg descs:   Description for each node.
        """

        # Mappings from node ID and from
        # coding value to Node objects.
        # Mappings for unique codings
        # only are retained - non-unique
        # mappings are culled afterwards.
        self.__by_id     = {}
        self.__by_coding = {}
        counts           = {}

        for i, node_id in enumerate(nodes):
            coding    = codings[i]
            parent_id = parents[i]
            attrs     = {'description' : descs[i]}
            node      = Node(node_id, parent_id, coding, attrs)

            self.__by_id[    node_id] = node
            self.__by_coding[coding]  = node
            counts[          coding]  = counts.get(coding, 0) + 1

        for coding, count in counts.items():
            if count > 1:
                self.__by_coding.pop(coding)


    @property
    def codings(self):
        """Return a list of all unique codings in the hierarchy. """
        return list(self.__by_coding.keys())


    def index(self, coding):
        """Return the node ID for the given ``coding``. A ``KeyError``
        is raised for non-uniqwue or invalid codings.
        """
        return self.__by_coding[coding].node_id


    def coding(self, nodeID):
        """Return the coding for the given ``nodeID``. """
        return self.__by_id[nodeID].coding


    def parents(self, coding):
        """Return codings for all parents of the given coding.  A ``KeyError``
        is raised for non-uniqwue or invalid codings.
        """
        pids    = self.parentIDs(self.__by_coding[coding].node_id)
        codings = [self.__by_id[p].coding for p in pids]
        return codings


    def parentIDs(self, nodeID):
        """Return IDs of  all parents of the given node. """

        node       = self.__by_id[nodeID]
        parent     = node
        parent_ids = []
        seen       = set()

        while True:

            parent = self.__by_id.get(parent.parent_id, None)

            # we're at the top of the tree
            if parent is None:
                break

            # circular relationship in tree - should never
            # happen, means the coding file is corrupt
            if parent.node_id in seen:
                raise CircularError(f'{parent.node_id} / {parent.coding}')

            seen      .add(   parent.node_id)
            parent_ids.append(parent.node_id)

        return parent_ids


    def description(self, coding):
        """Return the description for the given coding. """
        return self.get(coding, 'description')


    def get(self, coding, attr):
        """Get the given attribute for the given coding. Returns a ``KeyError``
        for non-unique / invalid codings, or non-existent attributes.
        """
        return self.__by_coding[coding].attrs[attr]


    def set(self, coding, attr, value):
        """Set an attribute for the given coding. Returns a ``KeyError``
        for non-unique / invalid codings.
        """
        self.__by_coding[coding].attrs[attr] = value
