#!/usr/bin/env python
#
# cleaning_functions.py - Cleaning functions.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains definitions of cleaning functions - functions
which may be specified in the ``Clean`` column of the variable table,
and which are appiled during the data import stage.

The following cleaning functions are available:

.. autosummary::
   :nosignatures:

   remove
   keepVisits
   fillVisits
   fillMissing
   flattenHierarchical
   parseSpirometryData
   makeNa


All cleaning functions (with two exceptions - :func:`remove` and
:func:`keepVisits`, explained below) will be passed the following as their
first positional arguments, followed by any arguments specified in the
variable table:

 - The :class:`.DataTable` object, containing references to the data, variable,
   and processing table.
 - The integer ID of the variable to process

These functions are expected to perform in-place pre-processing on the data.


The :func:`remove` and :func:`keepVisits` functions are called before the data
is loaded, as they are used to determine which columns should be loaded
in. They therefore have a different function signature to the other cleaning
functions, which are called after the data has been loaded. These functions
are passed the following positional arguments, followed by arguments specified
in the variable table:

 - The variable table, containing metadata about all known variables

 - The integer ID of the variable to be checked

 - A list of :class:`.Column` objects denoting all columns
   associated with this variable that are present in the data

These functions are expected to return a modified list containing the columns
that should be loaded.
"""


import logging

import numpy            as np
import pandas           as pd
import pandas.api.types as pdtypes

from . import util
from . import icd10
from . import custom
from . import hierarchy
from . import expression


log = logging.getLogger(__name__)


@custom.cleaner()
def remove(vartable, vid, columns):
    """remove()
    Remove (do not load) all columns associated with ``vid``.

    :arg vartable: Variable table
    :arg vid:      Integer variable ID.
    :arg columns:  List of all :class:`.Column` objects associated with
                   ``vid``.
    :returns:      An empty list.
    """
    return []


@custom.cleaner()
def keepVisits(vartable, vid, columns, *tokeep):
    """keepVisits(visit[, visit, ...])
    Only load columns for ``vid`` which correspond to the specified visits.

    This test is only applied to variables which have an *instancing* equal to
    2:

    https://biobank.ctsu.ox.ac.uk/crystal/instance.cgi?id=2

    Such variables are not associated with a specific visit, so it makes no
    sense to apply this test to them. See the
    :func:`.loadtables.addNewVariable` function for more information on
    variable instancing.

    :arg vartable: Variable table

    :arg vid:      Integer variable ID.

    :arg columns:  List of all :class:`.Column` objects that are associated
                   with ``vid``.

    :arg tokeep:   Visit IDs (integers), or ``'first'``, or ``'last'``,
                   indicating that the first or last visit should be loaded.

    :returns:      List of columns that should be loaded.
    """

    # variables which don't follow instancing
    # 2 do not have columns that correspond
    # to specific visits.
    instancing = vartable.loc[vid, 'Instancing']
    if instancing != 2:
        return columns

    keep      = []
    minVisit  = min([c.visit for c in columns])
    maxVisit  = max([c.visit for c in columns])

    for col in columns:

        test = [col.visit]

        if col.visit == minVisit: test.append('first')
        if col.visit == maxVisit: test.append('last')

        if col not in keep and any([v in tokeep for v in test]):
            keep.append(col)

    return keep


@custom.cleaner()
def fillVisits(dtable, vid, method='mode'):
    """fillVisits([method=(mode|mean)])
    Fill missing visits from available visits.

    For a variable with multiple visits, fills missing values from the visits
    that do contain data. The ``method`` argument can be set to one of:

      - ``'mode'`` (the default) - fill missing visits with the most
        frequently occurring value in the available visits
      - ``'mean'`` - fill missing visits with the mean of the values in the
        available visits
    """

    if method not in ('mode', 'mean'):
        raise ValueError('Unknown method: {}'.format(method))

    instances = dtable.instances(vid)

    for instance in instances:
        columns = [c.name for c in dtable.columns(vid, instance=instance)]
        view    = dtable[:, columns]

        if   method == 'mode': repvals = view.mode('columns')[0]
        elif method == 'mean': repvals = view.mean('columns')

        log.debug('Filling NA values in columns %s across visits', columns)

        for col in columns:
            dtable[:, col] = dtable[:, col].fillna(repvals)


@custom.cleaner()
def fillMissing(dtable, vid, value):
    """fillMissing(fill_value)
    Fill missing values with a constant.

    Fills all missing values in columns for the given variable with
    ``fill_value``.
    """
    columns = [c.name for c in dtable.columns(vid)]
    log.debug('Filling NA values in columns %s with %i', columns, value)
    for col in columns:
        dtable[:, col] = dtable[:, col].fillna(value)


@custom.cleaner()
def flattenHierarchical(dtable,
                        vid,
                        level=None,
                        name=None,
                        numeric=False,
                        convertNumeric=False):
    """flattenHierarchical([level][, name][, numeric][, convertNumeric])
    Replace leaf values with parent values in hierarchical variables.

    For hierarchical variables such as the ICD10 disease categorisations,
    this function replaces leaf values with a parent value.

    The ``level`` argument allows the depth of the parent value to be selected
    - ``0`` (the default) replaces a value with the top-level (i.e. its most
    distant) parent value, ``1`` the second-level parent value, etc.

    If, for a particular value, the ``level`` argument is greater than the
    number of ancestors of the value, the value is unchanged.

    By default, ``flattenHierarchical`` expects to be given coding values.  For
    example, for `data field 41202
    <https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=41202>`_ (ICD10
    diagnoses), coding ``A009`` (Cholera, unspecified) would be replaced with
    ``Chapter I`` (Certain infectious and parasitic diseases).

    The ``numeric`` argument tells the function to expect numeric node IDs (as
    output by :func:`codeToNumeric`), rather than coding labels. This allows
    ``flattenHierarchical`` to be used in conjunction with ``codeToNumeric``,
    e.g.::

        -cl 41202 "codeToNumeric,flattenHierarchical(numeric=True)"

    Continuing the above example, the ``codeToNumeric`` function would replace
    ``A009`` with its node ID ``2890``, and
    ``flattenHierarchical(numeric=True)`` would replace ``2890`` with ``10``
    (the node ID for ``Chapter I``).

    The ``convertNumeric`` argument is a shortcut for the above scenario -
    using this implies ``numeric=True``, and will cause the ``codeToNumeric``
    routine to be called automatically. The following example is equivalent
    to the above::

        -cl 41202 "flattenHierarchical(convertNumeric=True)"

    The ``name`` option is unnecessary in most cases, but may be used to
    specify an encoding scheme to use. Currently, ``'icd9'``, ``'icd10'``,
    ``'opsc3'`` and ``'opsc4'`` are accepted.
    """

    if convertNumeric:
        numeric = True
        codeToNumeric(dtable, vid, name)

    if level is None:
        level = 0

    columns = [c.name for c in dtable.columns(vid)]
    vhier   = hierarchy.getHierarchyFilePath(dtable, vid, name)
    vhier   = hierarchy.loadHierarchyFile(vhier)

    # Hierarchy.parents returns a list of all
    # parents of a node - we want to return
    # the one at the requested level/depth
    def index_parent(parents, val):

        if pdtypes.is_number(parents) and pd.isna(parents):
            return val

        # the list returned by Hierarchy.parents
        # is ordered from closest to most distant
        # parent, so we index from the end.
        idx = len(parents) - 1 - level

        # If the specified level is out of
        # bounds, we return the original value
        if idx < 0: return val
        else:       return parents[idx]

    log.debug('Flattening hierarchical data in columns %s (level %i)',
              columns, level)

    if numeric: lookupFunc = vhier.parentIDs
    else:       lookupFunc = vhier.parents

    for col in columns:
        data           = dtable[:, col]
        parents        = data.map(lookupFunc, na_action='ignore')
        parents        = parents.combine(data, index_parent)
        dtable[:, col] = parents


@custom.cleaner()
def codeToNumeric(dtable, vid, name=None):
    """codeToNumeric()
    Convert hierarchical coding labels to numeric equivalents (node IDs).

    Given a hierarchical variable which contains alpha-numeric codings, this
    function will replace the codings with numeric equivalents (node IDs).

    For example, UKB data field 41202 (ICD10 diagnoses) uses `data coding 19
    <https://biobank.ctsu.ox.ac.uk/crystal/coding.cgi?id=19>`_, which uses
    alpha-numeric codings to denote medical diagnoses.

    For data field 41202, ``codeToNumeric`` would replace coding ``D730``
    with the corresponding node ID ``22180``.

    The ``name`` option is unnecessary in most cases, but may be used to
    specify an encoding scheme to use. Currently, ``'icd9'``, ``'icd10'``,
    ``'opsc3'`` and ``'opsc4'`` are accepted.
    """

    hier = hierarchy.getHierarchyFilePath(dtable, vid, name=name)
    hier = hierarchy.loadHierarchyFile(hier)

    def convert(code):
        return hierarchy.codeToNumeric(code, hier=hier)

    cols  = [c.name for c in dtable.columns(vid)]
    codes = dtable[:, cols]

    log.debug('Converting hierarchy codes to numeric for '
              'variable %i [%u columns]', vid, len(cols))

    for col in cols:
        dtable[:, col] = codes[col].map(convert)

    if name is None:
        coding = dtable.vartable.loc[vid, 'DataCoding']
        ncmap  = {c : n for n, c in hierarchy.HIERARCHY_DATA_NAMES.items()}
        name   = ncmap.get(coding, None)

    if name == 'icd10':
        for col in cols:
            icd10.storeCodes(codes[col].tolist())


@custom.cleaner()
def parseSpirometryData(dtable, vid):
    """parseSpirometryData()
    Parse spirometry (lung volume measurement) data.

    Parses values which contain spirometry (lung volume measurement) test
    data.

    Columns for UK Biobank data fields `3066
    <https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=3066>`_ and `10697
    <https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=10697>`_ contain
    comma-separated time series data. This function converts the text values
    into ``numpy`` arrays, and potentially re-orders instances of the variable
    within each visit - subjects potentially underwent a series of tests, with
    each test stored as a separate instance within one visit. However, the
    instance order does not necessarily correspond to the test order.
    """
    visits = dtable.visits(vid)

    # applied to each row
    def fixOrder(vals):

        def parseBlow(val):
            # the first entry is "blowN",
            # where N is the blow number
            try:
                tkn = val[:10].split(',', maxsplit=1)[0]
                return int(tkn[4:])
            except Exception:
                return np.nan
        bnumvals = [(parseBlow(v), v) for v in vals]
        bnumvals = sorted(bnumvals)
        return pd.Series([bv[1] for bv in bnumvals],
                          index=vals.index)

    def parseValue(val):
        # first entry is "blowN", second
        # entry is number of samples.
        # Ignore them both, turn the
        # remainder into a numpy array
        try:
            val = val.split(',', maxsplit=2)[2]
            return np.fromstring(val, sep=',')
        except Exception:
            return np.nan

    for visit in visits:
        cols = dtable.columns(vid, visit=visit)
        cols = [c.name for c in cols]

        data = dtable[:, cols]
        data = data.apply(fixOrder,   axis=1)
        for col in cols:
            data.loc[:, col] = data.loc[:, col].apply(parseValue)

        dtable[:, cols] = data


@custom.cleaner()
def makeNa(dtable, vid, expr):
    """makeNa(expression)
    Replace values which pass the expression with NA.

    All values in the columns of the variable for which ``func`` evaluates to
    ``True`` are replaced with ``nan``.

    The ``expression`` must be of the form ``'<operator> <value>'``, where
    ``<operator>`` is one of ``==``, ``!=``, ``<``, ``<=``, ``>``, ``>=``, or
    ``contains`` (only applicable to non-numeric variables). For example,
    ``makeNa('> 25')`` would cause all values greater than 25 to be replaced
    with ``nan``.
    """

    expr = expression.Expression('v{} {}'.format(vid, expr))
    cols = dtable.columns(vid)

    for col in cols:
        col               = col.name
        mask              = expr.evaluate(dtable[:], {vid : col})
        dtable[mask, col] = np.nan
