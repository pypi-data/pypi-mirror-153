#!/usr/bin/env python
#
# config.py - Parses command line arguments and configuration files.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains functions for parsing ``funpack`` command line
arguments and configuration files. A ``funpack`` configuration file
is simply a plain-text file which contains command-line options,
sans-hyphens.
"""


import os.path         as op
import functools       as ft
import itertools       as it
import multiprocessing as mp
import                    sys
import                    shlex
import                    logging
import                    argparse
import                    collections
import numpy           as np

import funpack
import funpack.util           as util
import funpack.custom         as custom
import funpack.importing      as importing
import funpack.exporting_hdf5 as exporting_hdf5


log = logging.getLogger(__name__)


VERSION                    = funpack.__version__
DEFAULT_MERGE_AXIS         = importing.MERGE_AXIS
DEFAULT_MERGE_STRATEGY     = importing.MERGE_STRATEGY
AVAILABLE_MERGE_AXES       = importing.MERGE_AXIS_OPTIONS
AVAILABLE_MERGE_STRATEGIES = importing.MERGE_STRATEGY_OPTIONS
DEFAULT_HDF5_KEY           = exporting_hdf5.HDF5_KEY
DEFAULT_HDF5_STYLE         = exporting_hdf5.HDF5_STYLE
AVAILABLE_HDF5_STYLES      = exporting_hdf5.HDF5_STYLES
CLI_ARGUMENTS              = collections.OrderedDict((

    ('Input/output files', [
        ((       'outfile',),          {}),
        ((       'infile',),           {'nargs'   : '+'}),
        (('e',   'encoding'),          {'action'  : 'append'}),
        (('l',   'loader'),            {'nargs'   : 2,
                                        'metavar' : ('FILE', 'LOADER'),
                                        'action'  : 'append'}),
        (('i',   'index'),             {'nargs'   : 2,
                                        'metavar' : ('FILE', 'INDEX'),
                                        'action'  : 'append'}),
        (('ma',  'merge_axis'),        {'choices' : AVAILABLE_MERGE_AXES,
                                        'default' : DEFAULT_MERGE_AXIS}),
        (('ms',  'merge_strategy'),    {'choices' : AVAILABLE_MERGE_STRATEGIES,
                                        'default' : DEFAULT_MERGE_STRATEGY}),
        (('rm',  'remove_duplicates'), {'action' : 'store_true'}),
        (('rd',  'rename_duplicates'), {'action' : 'store_true'}),
        (('cfg', 'config_file'),       {'action'  : 'append'}),
        (('vf',  'variable_file'),     {'action'  : 'append'}),
        (('df',  'datacoding_file'),   {'action'  : 'append'}),
        (('tf',  'type_file'),         {}),
        (('pf',  'processing_file'),   {}),
        (('cf',  'category_file'),     {})]),

    ('Import options', [
        (('s',  'subject'),          {'action' : 'append'}),
        (('v',  'variable'),         {'action' : 'append'}),
        (('co', 'column'),           {'action' : 'append'}),
        (('c',  'category'),         {'action' : 'append'}),
        (('vi', 'visit'),            {'action' : 'append'}),
        (('ex', 'exclude'),          {'action' : 'append'}),
        (('ev', 'exclude_variable'), {'action' : 'append'}),
        (('ec', 'exclude_category'), {'action' : 'append'}),
        (('iv', 'index_visits'),     {'action' : 'store_true'}),
        (('tt', 'trust_types'),      {'action' : 'store_true'})]),

    ('Cleaning options', [
        (('sn',  'skip_insertna'),      {'action'  : 'store_true'}),
        (('scv', 'skip_childvalues'),   {'action'  : 'store_true'}),
        (('scf', 'skip_clean_funcs'),   {'action'  : 'store_true'}),
        (('sr',  'skip_recoding'),      {'action'  : 'store_true'}),
        (('nv',  'na_values'),          {'nargs'   : 2,
                                         'action'  : 'append',
                                         'metavar' : ('VID', 'NAVALUES')}),
        (('re',  'recoding'),           {'nargs'   : 3,
                                         'action'  : 'append',
                                         'metavar' : ('VID',
                                                      'RAWLEVELS',
                                                      'NEWLEVELS')}),
        (('cv',  'child_values'),       {'nargs'   : 3,
                                         'action'  : 'append',
                                         'metavar' : ('VID',
                                                      'EXPRS',
                                                      'VALUES')}),
        (('cl',  'clean'),              {'nargs'   : 2,
                                         'action'  : 'append',
                                         'metavar' : ('VID', 'EXPR')}),
        (('tc',  'type_clean'),         {'nargs'   : 2,
                                         'action'  : 'append',
                                         'metavar' : ('TYPE', 'EXPR')}),
        (('gc',  'global_clean'),       {'metavar' : 'EXPR'})]),

    ('Processing options', [
        (('sp',  'skip_processing'), {'action'  : 'store_true'}),
        (('ppr', 'prepend_process'), {'action'  : 'append',
                                      'nargs'   : 2,
                                      'metavar' : ('VARS', 'PROCS')}),
        (('apr', 'append_process'),  {'action'  : 'append',
                                      'nargs'   : 2,
                                      'metavar' : ('VARS', 'PROCS')})]),

    ('Export options', [
        (('io',  'ids_only'),              {'action'  : 'store_true'}),
        (('f',   'format'),                {}),
        (('edf', 'date_format'),           {'default' : 'default'}),
        (('etf', 'time_format'),           {'default' : 'default'}),
        (('evf', 'var_format'),            {'nargs'   : 2,
                                            'metavar' : ('VID', 'FORMATTER'),
                                            'action'  : 'append'}),
        (('esn', 'suppress_non_numerics'), {'action'  : 'store_true'}),
        (('nr',  'num_rows'),              {'type'    : int})]),

    ('TSV/CSV export options', [
        (('ts',  'tsv_sep'),            {}),
        (('en',  'escape_newlines'),    {'action'  : 'store_true'}),
        (('tm',  'tsv_missing_values'), {'default' : ''})]),

    ('HDF5 export options', [
        (('hk', 'hdf5_key'),   {'default' : DEFAULT_HDF5_KEY}),
        (('hs', 'hdf5_style'), {'default' : DEFAULT_HDF5_STYLE,
                                'choices' : AVAILABLE_HDF5_STYLES})]),

    ('Auxillary output file options', [
        (('wl',  'write_log'),          {'action' : 'store_true'}),
        (('wnn', 'write_non_numerics'), {'action' : 'store_true'}),
        (('wu',  'write_unknown_vars'), {'action' : 'store_true'}),
        (('wim', 'write_icd10_map'),    {'action' : 'store_true'}),
        (('wde', 'write_description'),  {'action' : 'store_true'}),
        (('ws',  'write_summary'),      {'action' : 'store_true'}),
        (('lf',  'log_file'),           {}),
        (('nnf', 'non_numerics_file'),  {}),
        (('uf',  'unknown_vars_file'),  {}),
        (('imf', 'icd10_map_file'),     {}),
        (('def', 'description_file'),   {}),
        (('sf',  'summary_file'),       {})]),

    ('Miscellaneous options', [
        (('V',  'version'),      {'action'  : 'version',
                                  'version' :
                                  '%(prog)s {}'.format(VERSION)}),
        (('dn', 'drop_na_rows'), {'action' : 'store_true'}),
        (('d',  'dry_run'),      {'action' : 'store_true'}),
        (('nb', 'no_builtins'),  {'action' : 'store_true'}),
        (('nj', 'num_jobs'),     {'type'    : int,
                                  'default' : 1}),
        (('p',  'plugin_file'),  {'action'  : 'append',
                                  'metavar' : 'FILE'}),
        (('ow', 'overwrite'),    {'action'  : 'store_true'}),
        (('n',  'noisy'),        {'action'  : 'count'}),
        (('q',  'quiet'),        {'action'  : 'store_true'})])))


CLI_DESCRIPTIONS = {

    'Inputs' :
    'The --variable_file and --datacoding_file options can be used multiple\n'
    'times - all provided files will be merged into a single table using the\n'
    'variable/data coding IDs.',

    'Export options' :
    'Non-numeric columns are exported to the main output file by default,\n'
    'but you can control this behaviour using one of the following options:\n'
    '\n'
    ' - The --suppress_non_numerics option tells FUNPACK to only save\n'
    '   numeric columns to the main output file.\n'
    ' - The --write_non_numerics option (described in the "Auxillary output\n'
    '   file options" section) tells FUNPACK to save non-numeric columns to\n'
    '   a separate output file.\n'
    '\n'
    'Note that the --suppress_non_numerics option is independent from the\n'
    '--write_non_numerics option - if you want to save non-numeric columns\n'
    'to a separate file, instead of to the main file, you must use both\n'
    'options together.',

    'Auxillary output file options' :
    'If the --write_log option is used, a default name, based on the main\n'
    'output file name, will be given to the log file. Alternatively, the\n'
    '--log_file option can be used with a specific name to use for the log\n'
    'file. This logic also applies to the other auxillary output files.\n'
    '\n'
    'The --unknown_vars_file allows a file to be saved containing\n'
    'information about columns which were in the input data, but were either\n'
    'not in the variable table, or were uncategorised and did not have any\n'
    'cleaning/processing rules specified. It contains four columns - the\n'
    'column name, the originating input file, the reason the column is being\n'
    'included (either unknown or uncategorised), and whether the column was\n'
    'exported.',
}


CLI_ARGUMENT_HELP = {

    # Input options
    'outfile' : 'Location to store output data.',
    'infile'  : 'File(s) containing input data.',

    'encoding' :
    'Character encoding. A single encoding can be specified, or this option '
    'can be used multiple times, one for each input file.',

    'loader' :
    'Use custom loader for file. Can be used multiple times.',

    'index' :
    'Position of index column for file (starting from 0). Can be used '
    'multiple times. Defaults to 0. Specify multi-column indexes as '
    'comma-separated lists.',

    'merge_axis' :
    'Axis to concatenate multiple input files along (default: "{}"). '
    'Options are "subjects"/"rows"/"0" or "variables"/"columns"/'
    '"1".'.format(DEFAULT_MERGE_AXIS),

    'merge_strategy' :
    'Strategy for merging multiple input files (default: "{}"). '
    'Options are "naive", "intersection"/"inner", or "union"/'
    '"outer".'.format(DEFAULT_MERGE_STRATEGY),

    'remove_duplicates' :
    'Remove duplicate columns, only retaining the first.',

    'rename_duplicates' :
    'Rename any duplicate columns so that all columns have a unique name.',

    'config_file' :
    'File containing default command line arguments. Can be used multiple '
    'times.',

    'variable_file' :
    'File(s) containing rules for handling variables',

    'datacoding_file' :
    'File(s) containing rules for handling data codings.',

    'type_file' :
    'File containing rules for handling types.',

    'processing_file' :
    'File containing variable processing rules.',

    'category_file' :
    'File containing variable categories.',

    'trust_types' :
    'Assume that columns in the input data with a known numeric type do not '
    'contain any bad/unparseable values. Using this flag will improve import '
    'performance, but will cause funpack to crash if the input file(s) do '
    'contain bad values.',

    'subject' :
    'Subject ID, range, comma-separated list, or file containing a list of '
    'subject IDs, or variable expression, denoting subjects to include. Can '
    'be used multiple times.',

    'variable' :
    'Variable ID, range, comma-separated list, or file containing a list of '
    'variable IDs, to import. Can be used multiple times.',

    'column' :
    'Name of column to import, or file containing a list of column names. Can '
    'also be a glob-style wildcard pattern - columns with a name matching the '
    'pattern will be imported. Can be used multiple times.',

    'category' :
    'Category ID or label to import. Can be used multiple times.',

    'visit' :
    'Import this visit. Can be used multiple times. Allowable values are '
    '\'first\', \'last\', or a visit number.',

    'exclude' :
    'Subject ID, range, comma-separated list, or file containing a list of '
    'subject IDs specifying subjects to exclude. Can be used multiple times.',

    'exclude_variable' :
    'Variable ID, range, comma-separated list, or file containing a list of '
    'variable IDs, to exclude. Takes precedence over the --variable and '
    '--category options. Can be used multiple times.',

    'exclude_category' :
    'Category ID or label to exclude. Takes precedence over the --variable '
    'and --category options. Can be used multiple times.',

    'index_visits' :
    'If set, the data is re-arranged so that visits form part of the row '
    'indices, rather than being stored in separate columns for each variable. '
    'Only applied to variables which are labelled with instancing 2 (Biobank '
    'assessment centre visit).',

    # Clean options
    'skip_insertna' :
    'Skip NA insertion.',
    'skip_childvalues' :
    'Skip child value replacement.',
    'skip_clean_funcs' :
    'Skip cleaning functions defined in variable table.',
    'skip_recoding' :
    'Skip raw->new level recoding.',

    'na_values' :
    'Replace these values with NA (overrides any NA values specified in '
    'variable table). Can be used multiple times. Values must be specified as '
    'a comma-separated list.',

    'recoding' :
    'Recode categorical variables (overrides any raw/new level recodings '
    'specified in variable table). Can be used multiple times. Raw and new '
    'level values must be specified as comma-separated lists.',

    'child_values' :
    'Replace NA with the given values where the given expressions evaluate '
    'to true (overrides any parent/child values specified in variable table). '
    'Can be used multiple times. Parent value expressions and corresponding '
    'child values must be specified as comma-separated lists.',

    'clean' :
    'Apply cleaning function(s) to variable (overrides any cleaning '
    'specified in variable table).',

    'type_clean' :
    'Apply clean function(s) to all variables of the specified type '
    '(overrides any cleaning specified in type table).',

    'global_clean' :
    'Apply cleaning function(s) to every variable (after variable-'
    'specific cleaning specified in variable table or via --clean).',

    # Processing options
    'skip_processing' :
    'Skip processing functions defined in processing table (but not '
    'those specified via --prepend_process and --append_process).',
    'prepend_process' :
    'Apply processing function(s) before processing defined in processing '
    'table.',
    'append_process' :
    'Apply processing function(s) after processing defined in processing '
    'table.',

    # Export options
    'ids_only' :
    'Do not output any data - instead, output a plain-text file which just '
    'contains the subject IDs, one per line. When this option is used, all '
    'cleaning and processing routines will be skipped, and no other output '
    'files (with the exception of a log file) will be produced.',
    'format' :
    'Output file format (default: inferred from the output file suffix - one '
    'of "tsv", "csv", or "h5").',
    'date_format' :
    'Formatter to use for date variables (default: "default").',
    'time_format' :
    'Formatter to use for time variables (default: "default").',
    'var_format' :
    'Apply custom formatter to the specified variable.',
    'num_rows' :
    'Number of rows to write at a time. Ignored if --num_jobs is set to 1.',
    'suppress_non_numerics' :
    'Do not save non-numeric columns to the main output file.',

    # TSV/CSV export options
    'escape_newlines' :
    'Escape any newline characters in all non-numeric columns, replacing them '
    'with a literal "\n" (with the same logic applied to any other escape '
    'characters).',
    'tsv_sep' :
    'Column separator string to use in output file (default: "," for csv, '
    '"\\t" for tsv).',
    'tsv_missing_values' :
    'String to use for missing values in output file (default: empty '
    'string).' ,

    # HDF5 export options
    'hdf5_key'    :
    'Key/name to use for the HDF5 group (default: '
    '"{}").'.format(DEFAULT_HDF5_KEY),
    'hdf5_style'  :
    'HDF5 style to save as (default: "{}").'.format(DEFAULT_HDF5_STYLE),

    # aux file options
    'write_log' : 'Save log messages to file.',
    'write_non_numerics' : 'Save non-numeric columns to file.',
    'write_unknown_vars' :
    'Save list of unknown/uncategorised variables/columns to file.',
    'write_icd10_map' :
    'Save converted ICD10 code mappings to file',
    'write_description'  :
    'Save descriptions of each column to file',
    'write_summary' :
    'Save summary of cleaning applied to each column to file',

    'log_file' : 'Save log messages to file.',
    'non_numerics_file' : 'Save non-numeric columns to file.',
    'unknown_vars_file' :
    'Save list of unknown/uncategorised variables/columns to file.',
    'icd10_map_file' :
    'Save converted ICD10 code mappings to file',
    'description_file' :
    'Save descriptions of each column to file',
    'summary_file' :
    'Save summary of cleaning applied to each column to file',

    # Miscellaneous options
    'version'      : 'Print version and exit.',
    'dry_run'      : 'Print a summary of what would happen and exit.',
    'drop_na_rows' : 'Drop rows which do not contain data for any column. '
                     'will take place on both import and export.',
    'no_builtins'  : 'Do not use the built in variable or data coding tables.',
    'num_jobs'     : 'Maximum number of jobs to run in parallel. Set to 1 '
                     '(the default) to disable parallelisation.  Set to -1 '
                     'to use all available cores ({} on this '
                     'platform).'.format(mp.cpu_count()),
    'plugin_file'  : 'Path to file containing custom funpack plugins. Can be '
                     'used multiple times.',
    'overwrite'    : 'Overwrite output file if it already exists',
    'noisy'        : 'Print debug statements. Can be used up to three times.',
    'quiet'        : 'Be quiet.',
}


def makeEpilog():
    """Generates an epilog for the command line help.

    The epilog contains an overview of available plugin functions.
    """

    def genTable(pluginType):
        plugins = custom.listPlugins(pluginType)
        descs   = []

        # The first two lines of all plugin function
        # docstrings are assumed to be:
        #   - function signature
        #   - one line description
        for p in plugins:
            try:
                desc = custom.get(pluginType, p).__doc__.split('\n')
                sig  = desc[0]
                desc = desc[1]
                descs.append((sig, desc))
            except Exception:
                descs.append(('n\a', None))

        maxpluginlen = max([len(p) for p in plugins])

        lines = []
        fmt   = '  - {{:{}s}}  {{}}'.format(maxpluginlen)

        for p, d in zip(plugins, descs):
            sig, desc = d
            lines.append(fmt.format(p, sig))
            if desc is not None:
                lines.append('{}  {}'.format(' ' * maxpluginlen, desc))

        return '\n'.join(lines)

    epilog = 'Available cleaning routines:'   + '\n'   + \
             genTable('cleaner')              + '\n\n' + \
             'Available processing routines:' + '\n'   + \
             genTable('processor')            + '\n'

    return epilog


@ft.lru_cache()
def makeParser(include=None, exclude=None):
    """Creates and returns an ``argparse.ArgumentParser`` for parsing
    ``funpack`` command line arguments.

    :arg include: Configure the parser so it only includes the specified
                  arguments.

    :arg exclude: Configure the parser so it excludes the specified
                  arguments - this overrides ``include``.
    """

    parser = argparse.ArgumentParser(
        'funpack',
        allow_abbrev=False,
        epilog=makeEpilog(),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    helps  = CLI_ARGUMENT_HELP
    descs  = CLI_DESCRIPTIONS

    for group, args in CLI_ARGUMENTS.items():

        desc  = descs.get(group, None)
        group = parser.add_argument_group(group, description=desc)

        for arg, kwargs in args:

            name = arg[-1]

            if exclude is not None and name     in exclude: continue
            if include is not None and name not in include: continue

            if len(arg) == 2:
                arg = ('-{}'.format(arg[0]), '--{}'.format(arg[1]))

            group.add_argument(*arg, help=helps[name], **kwargs)

    return parser


def sanitiseArgs(argv):
    """Sanitises command-line arguments to work around a bug in ``argparse``.

    The ``argparse`` module does not work with non-numeric optional argument
    values that begin with a hyphen, as it thinks that they are argument names
    (see https://bugs.python.org/issue9334).

    This function searches for relevant optional argument names, and prepends
    a space to their values to make sure that ``argparse`` doesn't fall over.

    :arg argv: Command-line arguments
    :returns:  Sanitised command-line arguments
    """
    argv       = list(argv)
    toSanitise = [( '-nv',           [1]),
                  ('--na_values',    [1]),
                  ( '-re',           [1, 2]),
                  ('--recoding',     [1, 2]),
                  ( '-cv',           [2]),
                  ('--child_values', [2])]

    for arg, idxs in toSanitise:

        try:               argidx = argv.index(arg)
        except ValueError: continue

        for i in idxs:

            i   = i + 1 + argidx
            val = argv[i]

            if val.startswith('-'):
                argv[i] = ' ' + val

    return argv


def loadConfigFile(cfgfile, namespace=None):
    """Loads arguments from the given configuration file, returning an
    ``argparse.Namespace`` object.

    :arg cfgfile:   Path to configuration file
    :arg namespace: Existing ``argparse.Namespace`` object to merge
                    arguments into.
    """

    argv = []

    # If the specified config file does
    # not exist, assume it is a reference
    # to a built-in config file
    if not op.exists(cfgfile):
        if not cfgfile.endswith('.cfg'):
            cfgfile = cfgfile + '.cfg'
        moddir   = op.dirname(op.abspath(__file__))
        cfgfile = op.join(moddir, 'configs', cfgfile)

    log.debug('Loading arguments from configuration file %s', cfgfile)

    with open(cfgfile, 'rt') as f:
        lines = [line.strip() for line in f.readlines()]
        lines = [line         for line in lines if line != '']
        lines = [line         for line in lines if not line.startswith('#')]

    for line in lines:
        words        = list(shlex.split(line))
        name, values = words[0], words[1:]

        argv.append('--{}'.format(name))
        argv.extend(values)

    argv      = sanitiseArgs(argv)
    parser    = makeParser(exclude=('outfile', 'infile'))
    namespace = parser.parse_args(argv, namespace)

    # a config file may "include" other
    # config files - we parse them recursively,
    # and merge the arguments in load order.
    cfgfiles = namespace.config_file
    if cfgfiles is not None and len(cfgfiles) > 0:
        for cf in cfgfiles:
            namespace.config_file = None
            namespace             = loadConfigFile(cf, namespace)

    return namespace


def parseArgsWithConfigFile(argv=None):
    """Checks the command line arguments to see if one or more configuration
    files has been specified. If so, loads the arguments in the configuration
    file(s), and then parses the rest of the command line arguments.

    :returns: see :func:`parseArgs`.
    """

    if argv is None:
        argv = sys.argv[1:]

    argv      = sanitiseArgs(argv)
    cfgfiles  = None
    namespace = None

    if '-cfg' in argv or '--config_file' in argv:
        cfgparser = makeParser('config_file')
        cfgfiles  = cfgparser.parse_known_args(argv)[0].config_file

    if cfgfiles is not None:
        for cf in cfgfiles:
            namespace = loadConfigFile(cf, namespace)

    return parseArgs(argv, namespace)


def parseArgs(argv=None, namespace=None):
    """Parses ``funpack`` command line arguments.

    :arg argv:      List of arguments to parse.

    :arg namespace: Existing ``argparse.Namespace`` - if not provided, an
                    empty one will be created.

    :returns:       A tuple containing:

                     - an ``argparse.Namespace`` object containing the parsed
                       command-line arguments.
                     - A list of the original arguments that were parsed.
    """

    if argv is None:
        argv = sys.argv[1:]

    argv = sanitiseArgs(argv)
    args = makeParser().parse_args(argv, namespace)

    # error if output file exists
    if (not args.dry_run) and (not args.overwrite) and op.exists(args.outfile):
        print('Output file already exists, and --overwrite was not '
              'specified!')
        sys.exit(1)

    # -1 implies max-parallel
    if   args.num_jobs <= -1: args.num_jobs = mp.cpu_count()
    elif args.num_jobs ==  0: args.num_jobs = 1

    if args.noisy is None: args.noisy = 0
    if args.quiet:         args.noisy = 0

    _prepareInputAndOutputFiles(        args)
    _prepareTableFiles(                 args)
    _prepareAuxFileNames(               args)
    _prepareSubjectAndVariableSelectors(args)
    _prepareCategorySelectors(          args)
    _prepareColumnSelectors(            args)
    _prepareVisitSelectors(             args)
    _prepareCleaningSelectors(          args)
    _prepareIDsOnly(                    args)

    return args, argv


def _prepareInputAndOutputFiles(args):
    """Sub-function of :func:`parseArgs`. Prepares arguments related to
    the primary input and output files.

    :arg args: ``argparse.Namespace`` object.
    """

    # make input/output files absolute
    args.infile  = [op.realpath(f) for f in args.infile]
    args.outfile =  op.realpath(args.outfile)

    # the importing.loadData function accepts
    # either a single encoding, or one encoding
    # for each data file. If the former, we
    # convert it into the latter, and then we
    # convert it into a dict of {infile:encoding}
    # mappings
    if args.encoding is not None:
        if len(args.encoding) == 1:
            args.encoding = [args.encoding[0]] * len(args.infile)
        elif len(args.encoding) != len(args.infile):
            raise ValueError('Wrong number of encodings specified - specify '
                             'either one encoding, or one encoding for each '
                             'input file.')
        args.encoding = dict(zip(args.infile, args.encoding))

    # turn loaders into dict of { absfile : name } mappings
    if args.loader is not None:
        args.loader = {op.realpath(f) : n for f, n in args.loader}

    # Remove/rename duplicates options are mutually exclusive
    if args.remove_duplicates and args.rename_duplicates:
        raise ValueError('Only one of--remove_duplicates and '
                         '--rename_duplicates may be used.')

    # turn index indices into dict of
    # { file : [index] } mappings
    if args.index is not None:
        indexes = {}
        for fname, idx in args.index:
            idx = [int(i) for i in idx.split(',')]
            indexes[op.abspath(fname)] = idx
        args.index = indexes

    # turn formatters into dict of { vid : name } mappings
    if args.var_format is None:
        args.var_format = []

    var_format = {}
    for v, n in args.var_format:

        # Formatters should be set on integer
        # variable IDs. But we allow non-integers
        # to pass through, as the exportData
        # function will also check against column
        # names.
        try:               v = int(v)
        except ValueError: pass

        var_format[v] = n

    args.var_format = var_format


def _prepareTableFiles(args):
    """Sub-function of :func:`parseArgs`. Prepares arguments related to
    the input table files.

    :arg args: ``argparse.Namespace`` object.
    """

    # The variable_file, datacoding_file, type_file,
    # processing_file, and category_file options
    # can be specified relative to funpackdir
    configdir = op.join(op.dirname(__file__), 'configs')

    def fixPath(f):

        if f is None:
            return f

        options = [
            f,
            op.join(configdir, f),
            op.join(configdir, f.replace('.', op.sep) + '.tsv')
        ]

        for o in options:
            if op.exists(o):
                return o

        # if the fixed version does not
        # exist, allow processing to
        # continue - it will fail later on.
        return f

    if args.variable_file is not None:
        args.variable_file = [fixPath(f) for f in args.variable_file]
    if args.datacoding_file is not None:
        args.datacoding_file = [fixPath(f) for f in args.datacoding_file]

    args.type_file       = fixPath(args.type_file)
    args.processing_file = fixPath(args.processing_file)
    args.category_file   = fixPath(args.category_file)


def _prepareAuxFileNames(args):
    """Sub-function of :func:`parseArgs`. Prepares arguments related to
    the auxillary output files.

    :arg args: ``argparse.Namespace`` object.
    """
    # assign default names to
    # auxillary output files
    outbase, outext = op.splitext(args.outfile)
    auxfiles        = ['log', 'non_numerics', 'unknown_vars',
                       'icd10_map', 'description', 'summary']
    auxexts         = collections.defaultdict(lambda : '.txt',
                                              non_numerics=outext)
    for auxfile in auxfiles:
        writeatt = 'write_{}'.format(auxfile)
        fileatt  = '{}_file' .format(auxfile)
        write    = getattr(args, writeatt)
        filename = getattr(args, fileatt)

        if write and filename is None:
            setattr(args, fileatt, '{}_{}{}'.format(outbase,
                                                    auxfile,
                                                    auxexts[auxfile]))
        else:
            setattr(args, writeatt, filename is not None)


def _prepareSubjectAndVariableSelectors(args):
    """Sub-function of :func:`parseArgs`. Prepares arguments related to
    the subject and variable selection options.

    :arg args: ``argparse.Namespace`` object.
    """

    # turn --subject/--variable/--exclude/
    # --exclude_variable arguments into
    # lists of IDs. If error is True, an
    # error is raised on unparseable
    # arguments.
    def replaceIDs(things, error=True):
        newthings = []
        failed    = []
        for thing in things:

            # --subject/--variable/--exclude args
            # may be may be a file name containing
            # a list of IDs
            if op.exists(thing):
                with open(thing, 'rt') as f:
                    parsed = f.read().split()
                    parsed = [int(t.strip()) for t in parsed]

            else:
                # Or they may be one or more comma-separated
                # IDs or matlab start:step[:stop] ranges,
                # both handled by the parseMatlabRange function.
                try:
                    parsed = []
                    for tkn in thing.split(','):
                        parsed.extend(util.parseMatlabRange(tkn))

                except ValueError:
                    parsed = None

                    # --subject may also be an expression,
                    # so if error is False, and the range/
                    # list parses fail, we pass the argument
                    # through. Otherwise we propagate the
                    # error.
                    if error:
                        raise

                if parsed is None:
                    failed.append(thing)
                    continue

            for t in parsed:
                if t not in newthings:
                    newthings.append(t)

        if len(newthings) == 0: newthings = None
        if len(failed)    == 0: failed    = None

        return newthings, failed

    # variable/exclude is transformed into
    # a list of integer IDs, but subject is
    # transformed into a tuple containing
    # ([ID], [exprStr])
    if args.subject is not None:
        args.subject  = replaceIDs(args.subject, False)
    else:
        args.subject  = None, None

    if args.variable is not None:
        args.variable = replaceIDs(args.variable)[0]
    if args.exclude is not None:
        args.exclude = replaceIDs(args.exclude)[0]
    if args.exclude_variable is not None:
        args.exclude_variable  = replaceIDs(args.exclude_variable)[0]


def _prepareCategorySelectors(args):
    """Sub-function of :func:`parseArgs`. Prepares arguments related to
    the category selection options.

    :arg args: ``argparse.Namespace`` object.
    """

    # categories can be specified
    # either by name or by ID -
    # convert the latter to integers.
    if args.category is not None:
        for i, c in enumerate(args.category):
            try:               args.category[i] = int(c)
            except ValueError: continue
    if args.exclude_category is not None:
        for i, c in enumerate(args.exclude_category):
            try:               args.exclude_category[i] = int(c)
            except ValueError: continue


def _prepareColumnSelectors(args):
    """Sub-function of :func:`parseArgs`. Prepares arguments related to
    the column selection options.

    :arg args: ``argparse.Namespace`` object.
    """
    # The column option accepts
    # column names, or a file
    # containing column names
    def loadIfExists(path):
        if op.exists(path):
            with open(path, 'rt') as f:
                items = f.readlines()
        else:
            items = [path]
        return [i.strip() for i in items]

    if args.column is not None:
        args.column = list(it.chain(*[loadIfExists(c) for c in args.column]))


def _prepareVisitSelectors(args):
    """Sub-function of :func:`parseArgs`. Prepares arguments related to
    visit selection options.

    :arg args: ``argparse.Namespace`` object.
    """
    # visits are restricted using the
    # keepVisits cleaning function
    if args.visit is not None:
        visit = []
        for v in args.visit:
            if v in ('first', 'last'): visit.append('"{}"'.format(v))
            else:                      visit.append(str(v))

        visit = 'keepVisits({})'.format(','.join(visit))

        if args.global_clean is None: args.global_clean  =       visit
        else:                         args.global_clean += ',' + visit


def _prepareCleaningSelectors(args):
    """Sub-function of :func:`parseArgs`. Prepares arguments related to
    cleaning function options.

    :arg args: ``argparse.Namespace`` object.
    """

    # convert na_values from a sequence of [(varid, values)]
    # pairs into a dict of {varid : values} mappings
    if args.na_values is not None:
        args.na_values = {int(vid) : values for vid, values in args.na_values}

    # Convert recoding from a sequence of [(varid, rawlevels, newlevels)]
    # tuples to a dict of {varid : (rawlevels, newlevels)} mappings
    if args.recoding is not None:
        args.recoding = {int(vid) : (rawlevels, newlevels)
                         for vid, rawlevels, newlevels in args.recoding}

    # Convert child_values from a sequence of
    # [(varid, exprs, values)] tuples to a dict of
    # {varid : (exprs, values)} mappings
    if args.child_values is not None:
        args.child_values = {int(vid) : (exprs, values)
                             for vid, exprs, values in args.child_values}

    # convert clean from a sequence of [(varid, expr)]
    # pairs into a dict of {varid : expr} mappings.
    if args.clean is not None:
        args.clean = {int(vid) : expr for vid, expr in args.clean}

    # convert type_clean from a sequence of [(type, expr)]
    # pairs into a dict of {type : expr} mappings.
    if args.type_clean is not None:
        args.type_clean = {util.CTYPES[t] : e for t, e in args.type_clean}


def _prepareIDsOnly(args):
    """Sub-function of :func:`parseArgs`. Prepares arguments related to
    the --ids_only option.

    :arg args: ``argparse.Namespace`` object.
    """
    if not args.ids_only:
        return

    args.skip_insertna      = True
    args.skip_childvalues   = True
    args.skip_clean_funcs   = True
    args.skip_recoding      = True
    args.skip_processing    = True

    # See main.main, and the do* functions
    # that it calls - aux file export is
    # ultimately toggled by these arguments
    args.unknown_vars_file  = None
    args.icd10_map_file     = None
    args.description_file   = None
    args.summary_file       = None
