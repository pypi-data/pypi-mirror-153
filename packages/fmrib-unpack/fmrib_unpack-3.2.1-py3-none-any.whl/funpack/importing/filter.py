#!/usr/bin/env python
#
# filter.py - functions for filtering columns/rows.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
"""This module contains functions used by the :func:`.core.importData`
function to identify which columns should be imported, and to filter
rows from a data frame after it has been loaded.
"""


import functools as ft
import itertools as it
import              fnmatch
import              logging
import              collections

from typing import Sequence, Union

import pandas as pd

import funpack.expression as expression
import funpack.loadtables as loadtables


log = logging.getLogger(__name__)


REMOVE_DUPLICATE_COLUMN_IDENTIFIER = '.REMOVE_DUPLICATE'
"""Identifier which is appended to the names of duplicate columns that
are to be removed. Use of this identifier is not hard-coded anywhere -
this module is just a convenient location for its definition. See
the :func:`funpack.main.doImport` function.
"""


def _ispattern(s):
    """Returns ``True`` if ``s`` looks like a ``fnmatch``-style pattern,
    ``False`` otherwise.
    """
    return any([c in s for c in '*?['])


def restrictVariables(
        cattable          : pd.DataFrame,
        variables         : Sequence[int]             = None,
        categories        : Sequence[Union[str, int]] = None,
        excludeVariables  : Sequence[int]             = None,
        excludeCategories : Sequence[Union[str, int]] = None
) -> Union[None, Sequence[int]]:

    """Determines which variables should be loaded (and the order they should
    appear in the output), and which variables should be excluded, from the
    given sequences of ``variables``,  ``categories``, and ``excludeVariables``
    and ``excludeCategories``.

    :arg cattable:          The category table
    :arg variables:         List of variable IDs to import.
    :arg categories:        List of category names or IDs to import.
    :arg excludeVariables:  List of variable IDs to exclude.
    :arg excludeCategories: List of category names or IDs to exclude.

    :returns:               A tuple containing:

                             - a sequence of variables to load, or ``None`` if
                               all variables should be loaded.

                             - a sequence of variables to exclude, or ``None``
                               if no variables should be excluded.
    """

    # Build a list of all the variables we
    # want to load, from the variables and
    # categories that were passed in.
    if categories is not None:

        if variables is None:
            variables = []

        catvars   = loadtables.categoryVariables(cattable, categories)
        variables = variables + [c for c in catvars if c not in variables]

    exclude = []

    if excludeVariables is not None:
        exclude = list(excludeVariables)

    if excludeCategories is not None:
        catvars   = loadtables.categoryVariables(cattable, excludeCategories)
        exclude   = exclude + catvars

    if variables is not None:
        variables = [v for v in variables if v not in exclude]

    return variables, exclude


def columnsToLoad(fileinfo,
                  vartable,
                  variables,
                  exclude=None,
                  colnames=None,
                  excludeColnames=None):
    """Determines which columns should be loaded from ``datafiles``.

    Peeks at the first line of the data file (assumed to contain column names),
    then uses the variable table to determine which of them should be loaded.

    :arg fileinfo:        :class:`.FileInfo` object describing the input
                          file(s).

    :arg vartable:        Variable table

    :arg variables:       List of variables to load.

    :arg exclude:         List of variables to exclude.

    :arg colnames:        List of column names/glob-style wildcard patterns,
                          specifying columns to load.

    :arg excludeColnames: List of column name suffixes specifying columns to
                          exclude. This overrides ``colnames``.

    :returns:           A tuple containing:

                         - A dict of ``{ file : [Column] }`` mappings, the
                           :class:`.Column` objects to *load* from each input
                           file. The columns (including the index column) are
                           ordered as they appear in the file.

                         - A list containing the :class:`.Column` objects to
                           *ignore*.
    """

    if exclude         is None: exclude         = []
    if excludeColnames is None: excludeColnames = []

    # We apply these cleaning steps by
    # omitting the relevant columns.
    loadFuncNames = ['remove', 'keepVisits']

    # Peek at the columns that
    # are in the input files.
    allcols = [fileinfo.columns(df) for df in fileinfo.datafiles]
    ncols   = len(list(it.chain(*allcols)))

    # re-organise the columns - a list of
    # columns for each variable ID. We do
    # this because, for a given VID, we
    # want to pass all columns at once to
    # the cleaning function(s) below.
    byvid = collections.defaultdict(list)
    for col in it.chain(*allcols):
        byvid[col.vid].append(col)

    # retrieve all cleaning steps -
    # we are only going to apply the
    # cleaning steps that will
    # determine whether or not a column
    # should be loaded
    mask    = vartable['Clean'].notna()
    cleans  = vartable['Clean'][mask]
    ppvids  = vartable.index[   mask]

    # Loop through all columns in
    # the data, and build a list of
    # the ones we want to load. The
    # end result will be an ordered
    # dict of { file : [column] }
    # mappings, and a list of columns
    # to drop.
    drop = []
    load = collections.OrderedDict([(f, []) for f in fileinfo.datafiles])
    for vid, cols in byvid.items():

        # index column - load it!
        # (the fileinfo function gives
        # index columns a variable ID
        # of 0).
        if vid == 0:
            for col in cols:
                load[col.datafile].append(col)
            continue

        # exclude/excludeColnames take precedence
        # over all other column selection mechanisms
        if vid in exclude:
            drop.extend(cols)
            continue
        for suf in excludeColnames:
            for col in list(cols):
                if col.name.endswith(suf):
                    cols.remove(col)
                    drop.append(col)

        # Figure out whether each
        # column should be loaded.
        # We load all columns which
        # pass either the variables
        # test or the colnames test
        # (or, if neither of those
        # options have been given,
        # all columns)
        loadflags = [(variables is None) and (colnames is None) for c in cols]

        # variable list has been specified,
        # and this vid is not in it - don't
        # load.
        if variables is not None:
            loadflags = [(vid in variables) for c in cols]

        # column names/patterns specified -
        # filter the list of columns based
        # on whether they match any of the
        # patterns specified.
        if colnames is not None:

            # if there are any glob patterns, do
            # an exhaustive search (*very* slow)
            if any(_ispattern(c) for c in colnames):
                for i, col in enumerate(cols):
                    hits = [fnmatch.fnmatch(col.name, pat) for pat in colnames]
                    loadflags[i] = loadflags[i] or any(hits)

            # short cut - if there are no glob
            # patterns, we don't have to use fnmatch
            else:
                for i, c in enumerate(cols):
                    loadflags[i] = loadflags[i] or (c.name in colnames)

        for col, loadflag in list(zip(cols, loadflags)):
            if not loadflag:
                cols.remove(col)
                drop.append(col)

        if len(cols) == 0:
            continue

        # cleaning specified for this variable
        if vid in ppvids:

            # retrieve the cleaning functions
            # which affect whether or not a column
            # should get loaded. We remove these
            # functions from the variable table, as
            # they won't need to be called again.
            funcs = [cleans[vid].pop(n, None) for n in loadFuncNames]
            funcs = [f for f in funcs if f is not None]

            # call the functions, generate a new
            # set of columns for this variable
            newcols = cols
            for f in funcs:
                newcols = f.run(vartable, vid, newcols)

            drop.extend(list(set.difference(set(cols), set(newcols))))

            cols = newcols

        for col in cols:
            load[col.datafile].append(col)

    # Final step - the column lists for each
    # file are not necessarily ordered by
    # their position in the file. Re-order
    # them so they are.
    for fname, cols in list(load.items()):
        load[fname].sort(key=lambda c: c.index)

    log.debug('Identified %i / %i columns to be loaded',
              sum([len(c) for c in load.values()]), ncols)

    return load, drop


def filterSubjects(data,
                   cols,
                   subjects=None,
                   subjectExprs=None,
                   exclude=None):
    """Removes rows (subjects) from the data based on ``subjects`` to
    include, conditional ``subjectExprs``, and subjects to ``exclude``.

    :arg data:         A ``pandas.DataFrame`` instance.

    :arg allcols:      List of :class:`.Column` objects describing every column
                       in the data set.

    :arg subjects:     List of subjects to include.

    :arg subjectExprs: List of subject inclusion expressions

    :arg exclude:      List of subjects to exclude

    :returns:          A ``pandas.DataFrame``, potentially with rows removed.
    """

    if all((subjects     is None,
            subjectExprs is None,
            exclude      is None)):
        return data

    mask = None

    # ones to include, zeros to drop
    if subjects is not None:
        mask = data.index.isin(subjects)

    if subjectExprs is not None and len(subjectExprs) >= 1:
        exprmask = evaluateSubjectExpressions(data, cols, subjectExprs)
        # include rows listed in subjects
        # and which pass any expression
        if mask is not None: mask = mask & exprmask
        else:                mask = exprmask

    # exclude list overrides all of the above
    if exclude is not None:
        exclmask = data.index.isin(exclude)
        if mask is None: mask           = ~exclmask
        else:            mask[exclmask] = 0

    if mask is not None: return data.loc[mask, :]
    else:                return data


def evaluateSubjectExpressions(data, allcols, subjectExprs):
    """Remove subjects (rows) from the data according to ``subjectExprs``.

    :arg data:         A ``pandas.DataFrame`` instance.

    :arg allcols:      List of :class:`.Column` objects describing every column
                       in the data set.

    :arg subjectExprs: List of strings containing expressions which identify
                       subjects to be included. Subjects for which *any*
                       expression evaluates to ``True`` will be included.

    :returns:          1D boolean ``numpy`` array containing ``True`` for
                       subjects to be included and ``False`` for subjects to
                       be excluded. Or ``None``, indicating that the
                       expressions were not evaluated (and all rows passed).
    """

    # build a {vid : [column]} mapping
    # to make life easy for the
    # evaluateSubjectExpression function
    colsbyvid = collections.defaultdict(list)
    for col in allcols:
        colsbyvid[col.vid].append(col)

    # evaluate each expression - we get
    # a numpy array for each of them
    exprmasks = []
    for i, expr in enumerate(subjectExprs):
        exprmask = evaluateSubjectExpression(data, expr, colsbyvid)
        if exprmask is not None:
            exprmasks.append(exprmask)

    # Any result which was not combined using
    # any() or all() defaults to being combined
    # with any(). For example, if "v123 >= 2"
    # is applied to columns 123-0.0, 123-1.0,
    # and 123-2.0, the final result will be
    # a 1D boolean array containing True where
    # any of the three columns were >= 2.
    for i, em in enumerate(exprmasks):
        if len(em.shape) == 2:
            exprmasks[i] = em.any(axis=1)

    # Finally, all expressions are combined in
    # the same manner - i.e. rows which passed
    # *any* of the expressions are included
    if   len(exprmasks) >  1: return ft.reduce(lambda a, b: a | b, exprmasks)
    elif len(exprmasks) == 1: return exprmasks[0]
    else:                     return None


def evaluateSubjectExpression(data, expr, cols):
    """Evaluates the given variable expression for each row in the data.

    :arg data: A ``pandas.DataFrame`` instance.

    :arg expr: String containing a variable expression

    :arg cols: Dict of ``{vid : [Column]}`` mappings

    :returns:  A boolean ``numpy`` array containing the result of evaluating
               the expression at each row, or ``None`` indicating that the
               expression was not evaluated (and every row passed).
    """
    expr = expression.Expression(expr)
    vids = expr.variables

    # Build a {vid : [colname]} dict to pass
    # to the expression evaluate method
    exprcols = {}
    for vid in vids:
        vidcols = [c.name for c in cols[vid]]
        if len(vidcols) > 0:
            exprcols[vid] = vidcols

    if len(exprcols) == 0:
        log.debug('Ignoring expression (%s) - no associated '
                  'columns are present', str(expr))
        return None

    if any(evid not in exprcols for evid in expr.variables):
        log.warning('Cannot evaluate expression (%s) - one or '
                    'more variables are not present', str(expr))
        return None

    log.debug('Evaluating expression (%s) on columns %s',
              str(expr), list(it.chain(*exprcols.values())))

    return expr.evaluate(data, exprcols)
