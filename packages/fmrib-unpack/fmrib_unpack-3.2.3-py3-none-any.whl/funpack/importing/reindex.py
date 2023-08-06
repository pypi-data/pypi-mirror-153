#!/usr/bin/env python
#
# reindex.py - Re-indexing a data frame by visit.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains functions used by the :func:`.core.importData`
function, for re-arranging a data frame that is indexed by subject into
a data frame that is indexed by subject and visit.
"""


import copy
import logging
import collections

import pandas as pd

from .. import datatable


log = logging.getLogger(__name__)


def reindexByVisit(df, oldcols, newcols, oldnewmap, visits):
    """Re-arranges the data so that visits form part of the row
    indices, rather than being stored in separate columns for each variable.

    The :func:`generateReindexedColumns` function is used to create the
    ``newcols``, ``oldnewmap``, and ``visits`` arguments.

    The given dataframe is assumed to be indexed by a single-level
    ``pandas.Index`` This is replaced with a ``pandas.MultiIndex``, where
    the first level corresponds to the original index, and the second level
    to the visit number.

    :arg df:       ``pandas.DataFrame`` containing the data.

    :arg oldcols:  list of :class:`.Column` objects describing the existing
                   data.

    :arg newcols:  List of :class:`.Column` objects decsribing each column in
                   the new adjusted data.

    :arg oldnewmap Dict of ``{old Column : new Column}`` mappings, describing
                   how the old data maps to the new data.

    :returns:      adjusted ``pandas.DataFrame``
    """

    # Create the new two-tierd index
    # comprising existing row IDs
    # and visit numbers
    oldindex    = df.index
    newindex    = pd.MultiIndex.from_product(
        (oldindex, visits), names=(oldindex.name, 'visit'))

    # Create a new empty, but
    # fully labelled, dataframe
    olddf       = df
    newcolnames = [c.name for c in newcols if c.vid != 0]
    newdf       = pd.DataFrame(index=newindex, columns=newcolnames)

    # Loop through column of the
    # old dataframe, copying its
    # data into the corresponding
    # location in the new dataframe.
    for oldcol in oldcols:

        if oldcol.vid == 0:
            continue

        newcol    = oldnewmap[oldcol]
        reindexed = (oldcol != newcol)

        if reindexed: idx = ((slice(None), oldcol.visit), newcol.name)
        else:         idx = ((slice(None), 0),            newcol.name)

        newdf.loc[idx] = olddf.loc[:, oldcol.name].values

    log.debug('Re-indexed for %u visits - %u rows and %u columns '
              're-arranged to %u rows and %u columns', len(visits),
              len(olddf), len(oldcols), len(newdf), len(newcols))

    return newdf


def genReindexedColumns(cols, vartable, onlyRealVisits=True):
    """Figures out how to re-arrange the columns of a data set so that it is
    indexed by row ID and visit.  This function is called by :func:`loadFile`
    when the ``indexVisits`` option is used.

    The ``onlyRealVisits`` argument controls whether the re-indexing is only
    applied to variables which are labelled with `instancing 2
    <https://biobank.ctsu.ox.ac.uk/crystal/instance.cgi?id=2>`_ (Biobank
    assessment centre visit), or is solely based on the ``instance`` component
    of the column name (see the :func:`.parseColumnName` function for details).

    :arg cols:           list of :class:`.Column` objects dewscribing the
                         existing data.

    :arg vartable:       ``pandas.DataFrame`` containing the variable table

    :arg onlyRealVisits: Re-index all columns according to the ``instance``
                         component of their column names, not just columns
                         associated with variables that follow instancing
                         2.

    :returns:            ``None`` if the file does not contain any data with
                         multiple visits, or a ``tuple`` containing:

                           - list of :class:`.Column` objects describing
                             the re-indexed data set.
                           - Dict of ``{old Column : new Column}`` mappings,
                             describing how the old data maps to the new data.
                           - A ``set`` containing all visit codes in the data.
    """

    oldcols = cols
    vt      = vartable

    # List of Column objects for the
    # new adjusted dataframe. During
    # creation, we index them by
    # (vid, visit, instance), to make
    # the mapping of old columns onto
    # new ones easier
    newcols = collections.OrderedDict()

    # Dict of {old Column : new Column}
    # mappings, so we know how to copy
    # data from the old df into the new
    # df
    oldnewmap = {}

    # All visit codes in the data
    visits = set()

    # figure out which variables should
    # be deemed as having visits, and
    # thus subjected to the re-indexing
    # process.
    def hasVisits(vid):
        return (not onlyRealVisits) or (vt.loc[vid, 'Instancing'] == 2)

    # Generate a list of Column objects
    # describing the new data frame. Start
    # with the index column. Currently
    # only supporting single-column index
    # in the input.
    idxcol            = copy.copy([c for c in oldcols if c.vid == 0][0])
    visitcol          = copy.copy(idxcol)
    visitcol.name     = 'visit'
    visitcol.origname = 'visit'
    newcols[0, 0, 0]  = idxcol
    newcols[0, 1, 0]  = visitcol

    # Now regular (non-index) columns
    for oldcol in oldcols:

        if oldcol.vid == 0:
            continue

        vid      = oldcol.vid
        visit    = oldcol.visit
        instance = oldcol.instance
        hasv     = hasVisits(vid)

        # This variable has visits - all
        # old columns with the same vid
        # and instance will map on to
        # the same new column.
        if hasv:
            visits.add(visit)
            visit = 0

        newcol = newcols.get((vid, visit, instance), None)

        # We've already created a new
        # column which maps to this old
        # column (i.e. from a different
        # visit number).
        if newcol is not None:
            oldnewmap[oldcol] = newcol
            continue

        # if this VID has visits, the
        # new dataframe will contain
        # one column for each instance.
        if hasv:
            newcol = datatable.Column(
                oldcol.datafile,
                name='{}.{}'.format(vid, instance),
                index=None,
                vid=vid,
                visit=0,
                instance=instance)

        # if this VID doesn't have visits,
        # the new dataframe will contain
        # identical columns to the old one.
        else:
            newcol = copy.copy(oldcol)

        newcols[vid, visit, instance] = newcol
        oldnewmap[oldcol]             = newcol

    newcols = list(newcols.values())
    for i, col in enumerate(newcols):
        col.index = i

    if len(visits) == 0:
        return (None, None, None)

    return newcols, oldnewmap, visits
