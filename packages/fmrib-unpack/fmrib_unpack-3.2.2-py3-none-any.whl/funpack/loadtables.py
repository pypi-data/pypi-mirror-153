#!/usr/bin/env python
#
# loadtables.py - Functions which load the variable, data coding, processing,
#                 and category tables used by funpack.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides functions and logic to load the variable, data coding,
type, processing, and category tables used by funpack.

The variable table is a ``pandas.DataFrame`` which contains metadata about all
UK Biobank variables in the input data files, along with cleaning rules. The
data coding and type tables contain the same information about all UK Biobank
data codings and types - these are merged into the variable table after
being loaded. All of these tables are loaded by the :func:`loadVariableTable`
function.

The processing table contains an ordered list of processing functions to be
applied to the input data.

The category table contains collections of variable groupings; it is used to
allow the user to select these groups by name, rather than having to
use variable IDs.

.. autosummary::
   :nosignatures:

   loadTables
   loadVariableTable
   addNewVariable
   loadProcessingTable
   loadCategoryTable
   categoryVariables
   columnTypes
"""


import itertools as it
import functools as ft
import os.path   as op
import              re
import              logging
import              warnings
import              collections

from typing import Tuple, Sequence, Union, Dict, List, Type, Any, Callable
from typing_extensions import Literal

import numpy  as np
import pandas as pd

import funpack.util       as util
import funpack.fileinfo   as finfo
import funpack.datatable  as datatable
import funpack.processing as processing
import funpack.expression as expression


log = logging.getLogger(__name__)


def convert_type(val : str) -> util.CTYPES:
    """Convert a string containing a UK BioBank type into a numerical
    identifier for that type - see :attr:`funpack.util.CTYPES`.
    """
    valmap = {
        'sequence' :
        util.CTYPES.sequence,
        'integer' :
        util.CTYPES.integer,
        'continuous' :
        util.CTYPES.continuous,
        'categorical (single)' :
        util.CTYPES.categorical_single,
        'categorical (single non-numeric)' :
        util.CTYPES.categorical_single_non_numeric,
        'categorical (multiple)' :
        util.CTYPES.categorical_multiple,
        'categorical (multiple non-numeric)' :
        util.CTYPES.categorical_multiple_non_numeric,
        'time' : util.CTYPES.time,
        'date' :
        util.CTYPES.date,
        'text' :
        util.CTYPES.text,
        'compound' :
        util.CTYPES.compound,
        'unknown' :
        util.CTYPES.unknown,
    }
    return valmap.get(val.lower(), util.CTYPES.unknown)


def convert_dtype(val : str) -> Union[np.dtype, Literal[np.nan]]:
    """Convert a string containing a ``numpy.dtype`` (e.g. ``'float32'``)
    into a ``dtype`` object.
    """

    if val == '':
        return np.nan

    dtype = getattr(np, val, None)

    if dtype not in np.ScalarType:
        raise ValueError('Invalid numpy dtype: {}'.format(dtype))

    return dtype


def convert_comma_sep_text(val : str) -> Union[List[str], Literal[np.nan]]:
    """Convert a string containing comma-separated text into a list. """
    if val.strip() == '':
        return np.nan
    words = val.split(',')
    return [w.strip() for w in words]


def convert_comma_sep_numbers(val : str) -> Union[np.ndarray, Literal[np.nan]]:
    """Convert a string containing comma-separated numbers into a ``numpy``
    array.
    """
    if val.strip() == '':
        return np.nan
    return np.fromstring(val, sep=',', dtype=np.float)


def convert_ParentValues(
        val : str) -> Union[List[expression.Expression], Literal[np.nan]]:
    """Convert a string containing a sequence of comma-separated
    ``ParentValue`` expressions into a sequence of :class:`.Expression`
    objects.
    """
    if val.strip() == '':
        return np.nan
    return [expression.Expression(e) for e in val.split(',')]


def convert_Process_Variable(val : str) -> Tuple[str, List[int]]:
    """Convert a string containing a process variable specification - one of:

      - One or more comma-separated MATLAB-style ``start:stop:step`` ranges,
        indicating that the process is to be applied to the specified variables
        simultaneously.

      - ``'independent,'``, followed by one or more comma-separated
        MATLAB-style ``start:stop:step`` ranges, indicating that the process
        is to be applied to the specified variables independently.

      - ``'all'``, indicating that the process is to be applied to all
        variables simultaneously

      - ``'all_independent'``, indicating that the process is to be applied
        to all variables independently

      - ``'all_except,'``, followed by one or more comma-separated MATLAB-style
        ranges, indicating that the process is to be applied to all variables
        simultaneously, except for the specified variables.

      - ``'all_independent_except,'``, followed by one or more comma-separated
        MATLAB-style ranges, indicating that the process is to be applied to
        all variables independently, except for the specified variables.

    :returns: A tuple containing:

               - The process variable type - one of ``'all'``,
                 ``'all_independent'``, ``'all_except'``,
                 ``'all_independent_except'``, ``'independent'``, or
                 ``'vids'``

               - A list of variable IDs (empty if the process variable type
                 is ``'all'`` or ``'all_independent'``).
    """
    tokens = convert_comma_sep_text(val)
    if len(tokens) == 1 and \
       tokens[0] in ('all', 'all_independent',
                     'all_except', 'all_independent_except'):
        return np.array((tokens[0], []), dtype=object)

    if tokens[0] in ('independent', 'all_except', 'all_independent_except'):
        ptype  = tokens[0]
        tokens = tokens[1:]
    else:
        ptype = 'vids'

    vids = list(it.chain(*[util.parseMatlabRange(t) for t in tokens]))

    return np.array((ptype, vids), dtype=object)


def convert_Process(
        ptype : str,
        val   : str
) -> Dict[str, processing.Process]:
    """Convert a string containing a sequence of comma-separated ``Process`` or
    ``Clean`` expressions into an ``OrderedDict`` of :class:`.Process`
    objects (with the process names used as dictionary keys).
    """
    if val.strip() == '':
        return np.nan

    procs = processing.parseProcesses(val, ptype)

    return collections.OrderedDict([(p.name, p)  for p in procs])


def convert_category_variables(val : str) -> List[int]:
    """Convert a string containing a sequence of comma-separated variable IDs
    or ranges into a list of variable IDs. Variables may be specified as
    integer IDs, or via a MATLAB-style ``start:step:stop`` range. See
    :func:`.util.parseMatlabRange`.
    """

    ranges    = convert_comma_sep_text(val)
    variables = list(it.chain(*[util.parseMatlabRange(r) for r in ranges]))

    return variables


VARTABLE_COLUMNS = [
    'ID',
    'Type',
    'InternalType',
    'Description',
    'DataCoding',
    'Instancing',
    'NAValues',
    'RawLevels',
    'NewLevels',
    'ParentValues',
    'ChildValues',
    'Clean']
"""The columns that must be in a variable table file. """


DCTABLE_COLUMNS = [
    'ID',
    'NAValues',
    'RawLevels',
    'NewLevels']
"""The columns that must be in a datacoding table file. """


TYPETABLE_COLUMNS = [
    'Type',
    'Clean']
"""The columns that must be in a type table file. """


PROCTABLE_COLUMNS = [
    'Variable',
    'Process']
"""The columns that must be in a processing table file. """


CATTABLE_COLUMNS = [
    'ID',
    'Category',
    'Variables']
"""The columns that must be in a category table file. """


VARTABLE_DTYPES = {
    'ID'           : np.uint32,
    'Description'  : object,

    # We can't use an integer for the data
    # coding, because not all variables
    # have a data coding, and pandas uses
    # np.nan to represent missing data.
    'DataCoding'   : np.float32,
    'Instancing'   : np.float32,
    'NAValues'     : object,
    'RawLevels'    : object,
    'NewLevels'    : object,
    'ParentValues' : object,
    'ChildValues'  : object,
    'Clean'        : object,

}
"""Types to use for some columns in the variable table. """


VARTABLE_CONVERTERS = {
    'Type'         : convert_type,
    'InternalType' : convert_dtype,
    'ParentValues' : convert_ParentValues,
    'Clean'        : ft.partial(convert_Process, 'cleaner'),
}
"""Custom converter functinos to use for some columns in the variable
table.
"""


DCTABLE_DTYPES = {
    'ID'         : np.uint32,
    'NAValues'   : object,
    'RawLevels'  : object,
    'NewLevels'  : object,
}
"""Types to use for some columns in the data coding table. """



TYPETABLE_DTYPES = {
    'Type'  : object,
    'Clean' : object,
}
"""Types to use for some columns in the types table. """


TYPETABLE_CONVERTERS = {
    'Type'  : convert_type,
    'Clean' : ft.partial(convert_Process, 'cleaner'),
}
"""Custom converter functinos to use for some columns in the type trable. """



PROCTABLE_CONVERTERS = {
    'Variable' : convert_Process_Variable,
    'Process'  : ft.partial(convert_Process, 'processor'),
}
"""Custom converter functinos to use for some columns in the processing
table.
"""


CATTABLE_DTYPES = {
    'ID' : np.int32,
}
"""Types to use for some columns in the category table. """


CATTABLE_CONVERTERS = {
    'Variables' : convert_category_variables
}
"""Custom converter functinos to use for some columns in the category
table.
"""


IMPLICIT_CATEGORIES = {
    'unknown'       : -1,
    'uncategorised' : -2,
}
"""This dict contains some categories which are automatically/implicitly
added to the category table by the :func:`loadTables` function (via a
call to :func:`addImplicitCategories`).
"""


def loadTables(
        fileinfo : finfo.FileInfo,
        varfiles : Sequence[str] = None,
        dcfiles  : Sequence[str] = None,
        typefile : str           = None,
        procfile : str           = None,
        catfile  : str           = None,
        **kw
) -> Tuple[pd.DataFrame,
           pd.DataFrame,
           pd.DataFrame,
           List[datatable.Column],
           List[datatable.Column]]:
    """Loads the data tables used to run ``funpack``.

    :arg fileinfo:  :class:`.FileInfo` object describing the input data files.
    :arg varfiles:  Path to one or more partial variable table files
    :arg dcfiles:   Path to one or more partial data coding table files
    :arg typefile:  Path to the type table file
    :arg procfile:  Path to the processing table file
    :arg catfile:   Path to the category table file

    All other arguments are passed throughh to the :func:`loadVariableTable`
    and :func:`loadProcessingTable` functions.

    :returns:      A tuple containing:

                    - The variable table
                    - The processing table
                    - The category table
                    - List of :class:`.Column` objects representing columns
                      which were in the data file(s), but not in the variable
                      table.
                    - List of :class:`.Column` objects representing columns
                      which are uncategorised.
    """

    vartable, unk, _ = loadVariableTable(fileinfo,
                                         varfiles,
                                         dcfiles,
                                         typefile,
                                         **kw)
    proctable        = loadProcessingTable(procfile, **kw)
    cattable         = loadCategoryTable(catfile)
    unc              = identifyUncategorisedVariables(fileinfo, cattable)

    # uncategorised should not contain unknown
    unc = [c for c in unc if c not in unk]

    # Add categorise for unknown/
    # uncategorised variables
    addImplicitCategories(cattable, unk, unc)

    return vartable, proctable, cattable, unk, unc


def loadVariableTable(
        fileinfo    : finfo.FileInfo,
        varfiles    : Sequence[str]              = None,
        dcfiles     : Sequence[str]              = None,
        typefile    : str                        = None,
        noBuiltins  : bool                       = False,
        naValues    : Dict[int, str]             = None,
        childValues : Dict[int, Tuple[str, str]] = None,
        recoding    : Dict[int, Tuple[str, str]] = None,
        clean       : Dict[int, str]             = None,
        typeClean   : Dict[util.CTYPES, str]     = None,
        globalClean : str                        = None,
        dropAbsent  : bool                       = True,
        **kwargs  # pylint: disable=unused-argument
) -> Tuple[pd.DataFrame,
           Sequence[datatable.Column],
           Sequence[datatable.Column]]:
    """Given variable table and datacoding table file names, builds and returns
    the variable table.

    :arg fileinfo:    :class:`.FileInfo` object describing the input data
                      files.

    :arg varfiles:    Path(s) to one or more variable files

    :arg dcfiles:     Path(s) to one or more data coding files

    :arg typefile:    Path to the type file

    :arg noBuiltins:  If provided, the built-in variable and datacoding base
                      tables are not loaded.

    :arg naValues:    Dictionary of ``{vid : values}`` mappings, specifying
                      values which should be replaced with NA. The values
                      are expected to be strings of comma-separated values.

    :arg childValues: Dictionary of ``{vid : (exprs, values)}`` mappings,
                      specifying parent value expressions, and corresponding
                      child values. The expressions and values
                      are expected to be strings of comma-separated values
                      of the same length.

    :arg recoding:    Dictionary of ``{vid : (rawlevel, newlevel)}``
                      mappings. The raw and enw levels are expected to be
                      strings of comma-separated values of the same length.

    :arg clean:       Dictionary of ``{vid : expr}`` mappings containing
                      cleaning functions to apply - this will override
                      any cleaning specified in the variable file, and
                      any cleaning specified in ``typeClean``. The expressions
                      are expected to be strings.

    :arg typeClean:   Dictionary of ``{type : expr}`` mappings containing
                      cleaning functions to apply to all variables of a
                      specific type - this will override any cleaning
                      specified in the type file. The expressions
                      are expected to be strings.

    :arg globalClean: Expression containing cleaning functions to
                      apply to every variable - this will be performed after
                      variable-specific cleaning in the variable table,
                      or specified via ``clean`` or ``typeClean``. The
                      expressions are expected to be strings.

    :arg dropAbsent:  If ``True`` (the default), remove all variables from the
                      variable table which are not present in the data
                      file(s).

    All other keyword arguments are ignored.

    :returns: A tuple containing:

                - A ``pandas.DataFrame`` containing the variable table

                - A sequence of :class:`.Column` objects representing variables
                  which were present in the data files, but not in the variable
                  table, but were added to the variable table.

                - A sequence of :class:`.Column` objects representing variables
                  which were present in the data files and in the variable
                  table, but which did not have any cleaning rules specified.
    """

    if noBuiltins: varbase, dcbase = None, None
    else:          varbase, dcbase = loadTableBases()

    vartable = mergeTableFiles(varbase,
                               varfiles,
                               'variable',
                               VARTABLE_DTYPES,
                               VARTABLE_CONVERTERS,
                               VARTABLE_COLUMNS)
    dctable  = mergeTableFiles(dcbase,
                               dcfiles,
                               'data coding',
                               DCTABLE_DTYPES,
                               {},
                               DCTABLE_COLUMNS)
    tytable  = mergeTableFiles(None,
                               [typefile],
                               'type',
                               TYPETABLE_DTYPES,
                               TYPETABLE_CONVERTERS,
                               TYPETABLE_COLUMNS)

    # Make sure data types are aligned,
    # otherwise we may run into problems
    # when merging them together.
    vartable = vartable.astype(
        {c : t for c, t in VARTABLE_DTYPES .items() if c != 'ID'})
    dctable  = dctable .astype(
        {c : t for c, t in DCTABLE_DTYPES  .items() if c != 'ID'})
    tytable  = tytable .astype(
        {c : t for c, t in TYPETABLE_DTYPES.items() if c != 'Type'})

    vartable.index = vartable.index.astype(VARTABLE_DTYPES[ 'ID'])
    dctable .index = dctable .index.astype(DCTABLE_DTYPES[  'ID'])
    tytable .index = tytable .index.astype(TYPETABLE_DTYPES['Type'])

    # Build a list of all columns in the input
    # data files, with the index column(s)
    # from each file dropped (index columns
    # are assigned a VID of 0)
    cols = []
    for df in fileinfo.datafiles:
        dfcols = fileinfo.columns(df)
        cols.extend([c for c in dfcols if c.vid != 0])

    # Make sure the variable table
    # contains an entry for every
    # variable in the input data.
    unknownVars = sanitiseVariableTable(vartable, cols, dropAbsent)

    # Merge data coding specific NAValues,
    # RawLevels, and NewLevels from the data
    # coding table into the variable table.
    mergeDataCodingTable(vartable, dctable)

    # Merge provided naValues, recodings,
    # and childValues into the variable
    # table (overriding whatever was specified
    # in the datacoding/variable tables)
    if naValues is not None:
        mergeIntoVariableTable(
            vartable,
            'NAValues',
            naValues)

    if recoding is not None:
        mergeIntoVariableTable(
            vartable,
            ['RawLevels', 'NewLevels'],
            recoding)

    if childValues is not None:
        childValues = {vid : (convert_ParentValues(expr), values)
                       for vid, (expr, values) in childValues.items()}
        mergeIntoVariableTable(
            vartable,
            ['ParentValues', 'ChildValues'],
            childValues)

    # navalues, raw/new levels and child values
    # are all still comma-separated strings -
    # convert them to types appropriate to the
    # datafield/variable
    def convert(rowvalues, column):
        val = rowvalues[column]

        if pd.isna(val):
            return np.nan

        val   = convert_comma_sep_text(val)
        ctype = rowvalues['Type']
        dtype = util.DATA_TYPES.get(ctype, None)

        if ctype in (util.CTYPES.date, util.CTYPES.time):
            return pd.to_datetime(val).values
        else:
            return np.array(val, dtype=dtype)

    # Make sure the series type stays as "object" - if
    # no rules are specified on any vid, the convert
    # function will return all nans, and pandas will
    # coerce the series type to float64, which may
    # interfere with subsequent rule assignments (as
    # these series may contain numpy arrays or
    # list-likes)
    if len(vartable) > 0:
        for col in ('NAValues', 'RawLevels', 'NewLevels', 'ChildValues'):
            newseries     = vartable.apply(convert, axis=1, args=(col,))
            vartable[col] = newseries.astype(object)

    # Before merging the cleaning functions
    # in, we generate a list of variables
    # which are "uncleaned", i.e. have not
    # had any cleaning specified, as this
    # may indicate that a variable has been
    # overlooked.
    #
    # If a variable has indirectly had NA
    # value insertion or recoding applied
    # via its data coding, it is not included
    # in this list.
    if clean is not None: ucmask = ~vartable.index.isin(clean.keys())
    else:                 ucmask =  vartable.index.notna()

    ucmask      = (ucmask                          &
                   vartable['NAValues']    .isna() &
                   vartable['RawLevels']   .isna() &
                   vartable['ParentValues'].isna() &
                   vartable['Clean']       .isna())
    ucmask      = ucmask[ucmask]
    uncleanVars = [c for c in cols
                   if (c.vid in ucmask.index and
                       c not in unknownVars)]

    # Merge clean options into variable table
    mergeCleanFunctions(vartable, tytable, clean, typeClean, globalClean)

    # Check where we can that the
    # vartable contains valid rules
    def checkLengths(col1, col2, row):
        val1  = row[col1]
        val2  = row[col2]
        isna1 = pd.isna(val1)
        isna2 = pd.isna(val2)

        # ugh. if the value is a sequence, isna
        # will return a sequence of bools
        if not isinstance(isna1, bool): isna1 = False
        if not isinstance(isna2, bool): isna2 = False

        if isna1 and isna2:
            return
        if isna1 or isna2 or (len(val1) != len(val2)):
            raise ValueError('Columns don\'t match [len({}) != '
                             'len({})]: {}'.format(val1, val2, row.name))

    checkRecoding     = ft.partial(checkLengths, 'RawLevels',    'NewLevels')
    checkParentValues = ft.partial(checkLengths, 'ParentValues', 'ChildValues')

    vartable.apply(checkRecoding,     axis=1)
    vartable.apply(checkParentValues, axis=1)

    return vartable, unknownVars, uncleanVars


def loadTableBases() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Loads the UK Biobank variable and data coding schema files.

    This function is called by :func:`loadVariableTable`. It loads the UK
    Biobank variable and data coding schema files (available from the UK
    Biobank data showcase web site), and returns the information contained
    within as two ``pandas.Dataframe`` objects. These dataframes are then
    used as bases for the ``funpack`` variable table.

    Information in the base tables is loaded from the following files:

     - ``field.txt``:    A list of all UKB variables
     - ``encoding.txt``: A list of all UKB data codings
     - ``type.txt``:     A list of ``vid : type`` mappings for certain
                         variables, where ``type`` is the name of a
                         ``numpy`` data type (e.g. ``float32``).

    :returns: A tuple containing:

               - a ``pandas.DataFrame`` to be used as the base for the
                 variable table
               - a ``pandas.DataFrame`` to be used as the base for the
                 datacoding table
    """

    # Here we load these files, both obtained
    # from the UK Biobank showcase website:
    #
    #  - field.txt    - describes all UK biobank variables
    #  - encoding.txt - describes all data codings
    #
    # And we also load type.txt, which contains
    # the internal type to use for some variables

    # This dict contains all possible combinations
    # of (value_type, base_type) from field.txt
    typecodes = {
        (11,  0)  : util.CTYPES.integer,
        (31,  0)  : util.CTYPES.continuous,
        (21,  11) : util.CTYPES.categorical_single,
        (21,  41) : util.CTYPES.categorical_single_non_numeric,
        (22,  11) : util.CTYPES.categorical_multiple,
        (22,  41) : util.CTYPES.categorical_multiple_non_numeric,
        (61,  0)  : util.CTYPES.time,
        (51,  0)  : util.CTYPES.date,
        (41,  0)  : util.CTYPES.text,
        (101, 0)  : util.CTYPES.compound,
    }

    # We need pandas >=0.24 to support enums here
    def settype(valtype, basetype):
        return typecodes[valtype, basetype]

    datadir   = op.join(op.dirname(__file__), 'data')
    fields    = op.join(datadir, 'field.txt')
    encodings = op.join(datadir, 'encoding.txt')
    types     = op.join(datadir, 'type.txt')

    fields    = pd.read_csv(fields,    delimiter='\t')
    encodings = pd.read_csv(encodings, delimiter='\t')
    types     = pd.read_csv(types,     delimiter='\t',
                            index_col=0,
                            converters={'Type' : convert_dtype})

    dcbase  = pd.DataFrame({'ID' : encodings['encoding_id']}).set_index('ID')
    varbase = pd.DataFrame({
        'ID'           : fields['field_id'].astype(np.uint64),
        'Type'         : fields['value_type'].combine(fields['base_type'],
                                                      settype),
        'Description'  : fields['title'],
        'DataCoding'   : fields['encoding_id'],
        'Instancing'   : fields['instance_id'],
    }).set_index('ID')

    types.rename({'Type' : 'InternalType'}, axis=1, inplace=True)
    varbase = pd.concat((varbase, types), axis=1, join='outer')

    return varbase, dcbase


def mergeTableFiles(
        base       : pd.DataFrame,
        fnames     : List[str],
        what       : str,
        dtypes     : Dict[str, Type],
        converters : Dict[str, Callable],
        columns    : List[str]
) -> pd.DataFrame:
    """Load and merge one or more table files.

    This function is called by :func:`loadVariableTable` to load the variable,
    data coding, and type table files.

    The variable and datacoding tables can be loaded from multiple files, with
    each file containing part of the full table. All provided files are merged
    into one table. The final table for a given set of files is the outer join
    on the index column (assumed to be the first column in each file), where
    non-na values in overlapping columns from later files will overwrite the
    values in earlier files.

    :arg base:       Table containing base information - used for the variable
                     and datacoding tables (see :func:`_loadTableBases`).

    :arg fnames:     List of files to load. If ``None``, the ``base`` table
                     is returned (or an empty table if a ``base`` is not
                     given).

    :arg what:       Name of the table files being loaded - used solely for log
                     messages

    :arg dtypes:     Dict containing ``{column : datatype}`` mappings

    :arg converters: Dict containing ``{column : convertfunc}`` mappings

    :arg columns:    Expected column names
    """

    idcol   = columns[0]
    columns = columns[1:]

    if fnames is None:
        fnames = []

    fnames = [f for f in fnames if f is not None]

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=pd.errors.ParserWarning)

        for f in fnames:

            log.debug('Loading %s table from %s', what, f)

            table = pd.read_csv(f,
                                sep='\t',
                                index_col=0,
                                dtype=dtypes,
                                converters=converters)

            if base is None:
                base = table
                continue

            # Merge each file with an outer
            # join, so we retain all IDs and
            # columns defined across the
            # entire set of files.
            merged = base.merge(table,
                                how='outer',
                                on=idcol,
                                sort=True,
                                suffixes=('_x', '_y'))

            # Now we merge overlapping columns -
            # non-na values in later files take
            # precedence.
            for c in [c[:-2] for c in merged.columns if c.endswith('_x')]:
                bname                = c + '_x'
                tname                = c + '_y'
                merged[c]            = merged[bname]
                notna                = merged[tname].notna()
                merged.loc[notna, c] = merged.loc[notna, tname]
                merged               = merged.drop(columns=[bname, tname])
            base = merged

    # no base, and no files
    if base is None:
        base = pd.DataFrame()

    # error if we have any
    # unrecognised columns
    for col in base.columns:
        if col not in columns:
            raise ValueError('Unrecognised column in table file {} - '
                             'should be {}, but file contained {}.'.format(
                                 fnames, columns, base.columns))

    # in-fill any columns that
    # were not provided
    for col in columns:
        if col not in base.columns:
            base[col] = pd.Series(dtype=np.float64)

    return base


def sanitiseVariableTable(
        vartable   : pd.DataFrame,
        cols       : Sequence[datatable.Column],
        dropAbsent : bool
) -> List[datatable.Column]:
    """Ensures that the variable table contains an entry for every
    variable in the input data.

    Called by :func:`loadVariableTable`.

    :arg vartable:   ``pandas.DataFrame`` containing the variable table.

    :arg cols:       Sequence of :class:`.Column` objects representing
                     the columns in the input data.

    :arg dropAbsent: If ``True``, entries in the table for variables which are
                     not in ``cols`` will be removed.

    :return:         A list of unknown :class:`.Column` objects, i.e.
                     representing variables which were not in the variable
                     table.
    """

    unknownVars = []

    # Make sure a placeholder entry is
    # present for any variables which are
    # not in the variable table, but which
    # are in the data file(s).
    for col in cols:

        vid  = col.vid
        name = col.name

        if vid in vartable.index:
            continue

        unknownVars.append(col)
        addNewVariable(vartable, vid, name)

    # And the inverse - we can drop any
    # variables from the variable table
    # that are not in the data.
    if dropAbsent:
        vids = [c.vid for c in cols]
        vartable.drop([v for v in vartable.index if v not in vids],
                      inplace=True)
    return unknownVars


def mergeIntoVariableTable(
        vartable : pd.DataFrame,
        cols     : Sequence[str],
        mapping  : Union[str, Dict[int, Any]]):
    """Merge data from ``mapping`` into the variable table.

    Called by :func:`loadVariableTable`.

    :arg vartable: The variable table

    :arg cols:     Names of columns in the variable table

    :arg mapping:  Dict of ``{vid : values}`` mappings containing the
                   data to copy in.
    """

    onecol = isinstance(cols, str)
    if onecol:
        cols = [cols]

    # Ignore any variables that
    # are not in variable table
    vids   = list(mapping.keys())
    vin    = pd.Series(vids).isin(vartable.index)
    vids   = [v for i, v in enumerate(vids) if vin[i]]

    for vid in vids:
        vals = mapping[vid]

        if onecol:
            vals = [vals]

        for col, val in zip(cols, vals):
            vartable.at[vid, col] = val


def mergeDataCodingTable(
        vartable : pd.DataFrame,
        dctable  : pd.DataFrame):
    """Merges information from the data coding table into the variable
    table.

    Called by :func:`loadVariableTable`.

    :arg vartable: The variable table.
    :arg dctable:  The data coding table.
    """

    with_datacoding = vartable['DataCoding'].notna()

    for field in ['NAValues', 'RawLevels', 'NewLevels']:
        mask    = vartable[field].isna() & with_datacoding
        newvals = vartable.loc[mask].merge(dctable,
                                           left_on='DataCoding',
                                           right_index=True,
                                           suffixes=('_v', '_dc'),
                                           copy=False)['{}_dc'.format(field)]
        vartable.loc[mask, field] = newvals


def mergeCleanFunctions(
        vartable    : pd.DataFrame,
        tytable     : pd.DataFrame,
        clean       : Dict[int, str],
        typeClean   : Dict[str, str],
        globalClean : str):
    """Merges custom clean functions into the variable table.

    Called by :func:`loadVariableTable`.

    :arg vartable:    The variable table.

    :arg tytable:     The type table

    :arg clean:       Dictionary of ``{vid : expr}`` mappings containing
                      cleaning functions to apply - this will override
                      any cleaning specified in the variable file, and
                      any cleaning specified in ``typeClean``.

    :arg typeClean:   Dictionary of ``{type : expr}`` mappings containing
                      cleaning functions to apply to all variables of a
                      specific type - this will override any cleaning
                      specified in the type file.

    :arg globalClean: Expression containing cleaning functions to
                      apply to every variable - this will be performed after
                      variable-specific cleaning in the variable table,
                      or specified via ``clean`` or ``typeClean``.
    """

    # Merge type-specific Clean
    # from the type table into
    # the variable table.
    for vid in vartable.index:

        if vid == 0:
            continue

        vtype = vartable.loc[vid, 'Type']
        pp    = vartable.loc[vid, 'Clean']

        # Override with typeClean if necessary
        if typeClean is not None and vtype in typeClean:
            tpp = convert_Process('cleaner', typeClean[vtype])
        elif vtype in tytable.index:
            tpp = collections.OrderedDict((tytable.loc[vtype, 'Clean']))
        else:
            continue

        # type cleaning is applied after
        # variable-specific cleaning
        if pd.isnull(pp): vartable.loc[[vid], 'Clean'] = [tpp]
        else:             vartable.loc[ vid,  'Clean'].update(tpp)

    # Override cleaning with expressions
    # that have been passed on the command line
    if clean is not None:
        clean = {vid : convert_Process('cleaner', expr)
                 for vid, expr in clean.items()}
        mergeIntoVariableTable(vartable, 'Clean', clean)

    # Add global cleaning to all variables
    if globalClean is not None:

        for vid in vartable.index:

            if vid == 0:
                continue

            pp  = vartable.loc[vid, 'Clean']
            gpp = convert_Process('cleaner', globalClean)

            # global cleaning is applied
            # after all other cleaning
            if pd.isnull(pp): vartable.loc[[vid], 'Clean'] = [gpp]
            else:             vartable.loc[ vid,  'Clean'].update(gpp)


def addNewVariable(
        vartable   : pd.DataFrame,
        vid        : int,
        name       : str,
        dtype      : np.dtype = None,
        instancing : int      = None):
    """Add a new row to the variable table.

    The ``instancing`` argument defines the meaning of the
    :attr:`.Column.visit` field for columns associated with this variable.
    The default value is ``2``, meaning that this variable may be associated
    with columns corresponding to measurements acquired at different UK
    BioBank assessments and imaging visits.  See
    https://biobank.ctsu.ox.ac.uk/crystal/schema.cgi?id=9 and
    https://biobank.ctsu.ox.ac.uk/crystal/schema.cgi?id=10 for more details.

    .. note:: If an entry for the specified ``vid`` already exists in
              ``vartable``, the ``name``, ``dtype`` and ``instancing``
              arguments are ignored and the existing information in
              ``vartable`` will take precedence.

    :arg vartable:   The variable table

    :arg vid:        Integer variable ID

    :arg name:       Variable name - used as the description

    :arg dtype:      ``numpy`` data type. If ``None``, the variable type
                     is set to :attr:`.util.CTYPES.unknown`.

    :arg instancing: Instancing code for the new variable - defaults to ``2``
    """

    # If an entry already exists
    # in the variable table, it
    # takes precedence
    if vid in vartable.index:
        dtype      = vartable.at[vid, 'Type']
        name       = vartable.at[vid, 'Description']
        instancing = vartable.at[vid, 'Instancing']

    else:
        # set dtype to something which
        # will cause the conditionals
        # to fall through
        if dtype is None: dtype = object
        else:             dtype = dtype.type

        # Assume that new variables
        # are associated with visits
        if instancing is None:
            instancing = 2

        if   issubclass(dtype, np.integer): dtype = util.CTYPES.integer
        elif issubclass(dtype, np.float):   dtype = util.CTYPES.continuous
        else:                               dtype = util.CTYPES.unknown

    vartable.loc[vid, 'Description'] = name
    vartable.loc[vid, 'Type']        = dtype
    vartable.loc[vid, 'Instancing']  = instancing


def loadProcessingTable(
        procfile       : str                             = None,
        skipProcessing : bool                            = False,
        prependProcess : Sequence[Tuple[List[int], str]] = None,
        appendProcess  : Sequence[Tuple[List[int], str]] = None,
        **kwargs  # pylint: disable=unused-argument
) -> pd.DataFrame:
    """Loads the processing table from the given file.

    :arg procfile:       Path to the processing table file.

    :arg skipProcessing: If ``True``, the processing table is not loaded from
                         ``procfile``. The ``prependProcess`` and
                         ``appendProcess`` arguments are still applied.

    :arg prependProcess: Sequence of ``(varids, procstr)`` mappings specifying
                         processes to prepend to the beginning of the
                         processing table.

    :arg appendProcess:  Sequence of ``(varids, procstr)`` mappings specifying
                         processes to append to the end of the processing
                         table.

    All other keyword arguments are ignored.
    """

    if prependProcess is None: prependProcess = []
    if appendProcess  is None: appendProcess  = []

    if (procfile is not None) and (not skipProcessing):
        log.debug('Loading processing table from %s', procfile)
        proctable = pd.read_csv(procfile,
                                sep='\t',
                                index_col=False,
                                skip_blank_lines=True,
                                comment='#',
                                converters=PROCTABLE_CONVERTERS)

    else:
        proctable = pd.DataFrame(columns=PROCTABLE_COLUMNS)

    # prepend/append custom
    # processes to the table
    proctable.index += len(prependProcess)
    for i, (vids, procs) in enumerate(prependProcess):
        vids  = convert_Process_Variable(vids)
        procs = convert_Process('processor', procs)
        proctable.at[i, 'Variable'] = np.array(vids, dtype=object)
        proctable.at[i, 'Process']  = procs

    for i, (vids, procs) in enumerate(appendProcess, len(proctable.index)):
        vids  = convert_Process_Variable(vids)
        procs = convert_Process('processor', procs)
        proctable.at[i, 'Variable'] = np.array(vids, dtype=object)
        proctable.at[i, 'Process']  = procs

    proctable.sort_index(inplace=True)

    return proctable


def loadCategoryTable(catfile : str = None) -> pd.DataFrame:
    """Loads the category table from the given file.

    :arg catfile: Path to the category file.
    """
    if catfile is not None:
        log.debug('Loading category table from %s', catfile)
        cattable = pd.read_csv(catfile,
                               sep='\t',
                               index_col=0,
                               dtype=CATTABLE_DTYPES,
                               converters=CATTABLE_CONVERTERS)
    else:
        cattable            = pd.DataFrame(columns=CATTABLE_COLUMNS[1:])
        cattable.index.name = CATTABLE_COLUMNS[0]


    return cattable


def categoryVariables(
        cattable   : pd.DataFrame,
        categories : Sequence[Union[int, str]]
) -> List[int]:
    """Returns a list of variable IDs from ``cattable`` which correspond to
    the strings in ``categories``.

    :arg cattable:   The category table.
    :arg categories: Sequence of integer category IDs or label sub-strings
                     specifying the categories to return.
    :returns:        A list of variable IDs.
    """

    allvars = []

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for cat in categories:

            catpat  = re.compile('({})'.format(cat), re.IGNORECASE)
            idmask  = cattable.index.isin([cat])
            lblmask = cattable['Category'].str.contains(catpat)
            catvars = cattable.loc[idmask | lblmask, 'Variables']

            if len(catvars) == 0:
                continue

            for c in catvars.iloc[0]:
                if c not in allvars:
                    allvars.append(c)

    return allvars


def variableCategories(
        cattable : pd.DataFrame,
        vids     : Sequence[int]
) -> Dict[int, List[str]]:
    """Identify the categories for each variable in vids.

    :arg cattable: The category table
    :arg vids:     Sequence of variable/datafield IDs
    :returns:      A dict of ``{vid : [category]}`` mappings
    """

    categories = collections.defaultdict(list)

    for v in vids:
        for i in cattable.index:
            if v in cattable.loc[i, 'Variables']:
                categories[v].append(cattable.loc[i, 'Category'])

    return categories


def addImplicitCategories(
        cattable : pd.DataFrame,
        unknown  : Sequence[datatable.Column],
        uncat    : Sequence[datatable.Column]):
    """Adds some implicit/automatic categories to the category table.

    The following implicit categories are added:

     - ``unknown``:       Variables which are not present in the variable
                          table - this comprises non-UKB variables, or new UKB
                          variables which are not described by the internal
                          FUNPACK variable information in ``funpack/data/``.

     - ``uncategorised``: Variables which are not present in any other
                          category.

    :arg cattable: The category table.
    :arg unknown:  Sequence of :class:`.Column` objects representing
                   variables to add to an "unknown" category.
    :arg uncat:    Sequence of :class:`.Column` objects representing
                   variables to add to an "uncategorised" category.
    """

    for cols, label in zip((unknown, uncat), ('unknown', 'uncategorised')):

        if cols is None:
            continue

        vids = list(sorted({c.vid for c in cols}))

        # label already in table?
        umask = cattable['Category'] == label

        if np.any(umask):
            idx  = np.where(umask)[0][0]
            idx  = cattable.index[idx]
            vids = cattable.loc[idx, 'Variables'] + vids
        else:
            idx = IMPLICIT_CATEGORIES[label]

        cattable.loc[idx, 'Category']  = label
        cattable.loc[idx, 'Variables'] = list(vids)


def columnTypes(
        vartable : pd.DataFrame,
        columns  : Sequence[datatable.Column]
) -> Tuple[List[util.CTYPES], Dict[str, np.dtype]]:
    """Retrieves the type of each column in ``cols`` as listed in ``vartable``.
    Also identifies a suitable internal data type to use for each column where
    possible.

    :arg vartable: The variable table.

    :arg columnss: List of :class:`.Column` objects.

    :returns:      A tuple containing:

                    - A list containing the type for each column in ``cols`` -
                      an identifier from the :attr:`.util.CTYPES` enum.
                      Columns corresponding to a variable which is not in
                      the variable table is given a type of ``None``.

                    - A dict of ``{ column_name : dtype }`` mappings containing
                      a suitable internal data type to use for some columns.
    """

    vttypes = []
    dtypes  = {}

    for col in columns:

        vid  = col.vid
        name = col.name

        if vid not in vartable.index:
            vttypes.append(None)
            continue

        vttype = vartable.loc[vid, 'Type']
        dtype  = vartable.loc[vid, 'InternalType']

        if pd.isna([dtype])[0]:
            dtype = util.DATA_TYPES.get(vttype, None)

        vttypes.append(vttype)
        if dtype is not None:
            dtypes[name] = dtype

    return vttypes, dtypes


def identifyUncategorisedVariables(
        fileinfo : finfo.FileInfo,
        cattable : pd.DataFrame
) -> List[datatable.Column]:
    """Called by :func:`loadTables`. Identifies all variables which are in the
    data file(s), but which are uncategorised (not present in any categories
    in the category table).

    Such variables might have been overlooked, so the user may need to be
    warned about them.

    :arg fileinfo:  :class:`.FileInfo` object.
    :arg cattable:  Category table
    :returns:       A list of :class:`.Column` objects associated with
                    variables that are uncategorised.
    """

    def isCategorised(col):
        def inCategory(catvars):
            return col.vid in catvars
        return cattable['Variables'].apply(inCategory).any()

    uncategorised = []
    for datafile in fileinfo.datafiles:
        cols = fileinfo.columns(datafile)
        cols = [c for c in cols if (c.vid != 0) and (not isCategorised(c))]
        uncategorised.extend(cols)

    return uncategorised
