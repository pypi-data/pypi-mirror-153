#!/usr/bin/env python
#
# main.py - funpack entry point
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains the ``funpack`` entry point. """


import multiprocessing     as mp
import os.path             as op
import                        sys
import                        logging
import                        warnings
import                        datetime
import                        calendar

import pandas              as pd
import pandas.api.types    as pdtypes
import                        threadpoolctl

import funpack
import funpack.util        as util
import funpack.icd10       as icd10
import funpack.config      as config
import funpack.custom      as custom
import funpack.dryrun      as dryrun
import funpack.fileinfo    as fileinfo
import funpack.cleaning    as cleaning
import funpack.datatable   as datatable
import funpack.exporting   as exporting
import funpack.hierarchy   as hierarchy
import funpack.importing   as importing
import funpack.loadtables  as loadtables
import funpack.processing  as processing


log = logging.getLogger(__name__)


def main(argv=None):
    """``funpack`` entry point. """

    # Make sure built in plugins are
    # registered, as they are queried
    # in the command-line help. Set
    # logging to critical until we've
    # parsed command-line args.
    logging.getLogger().setLevel(logging.CRITICAL)
    custom.registerBuiltIns()

    args, argv = config.parseArgsWithConfigFile(argv)
    date = datetime.date.today()

    # Set the number of threads
    # that numpy should use
    threadpoolctl.threadpool_limits(args.num_jobs)

    # Now that args are passed,
    # we can set up logging properly.
    configLogging(args)

    log.info('funpack %s', funpack.__version__)
    log.info('Date: %s (%s)', date.today(), calendar.day_name[date.weekday()])
    log.info('Command-line arguments %s', ' '.join(argv))
    log.debug('Running with the following options')
    for name, val in args.__dict__.items():
        if val is not None:
            val = str(val)
            if len(val) <= 30: log.debug('  %s: %s',    name, val)
            else:              log.debug('  %s: %s...', name, val[:30])

    # Load any custom plugins
    # that have been specified.
    if args.plugin_file is not None:
        for p in args.plugin_file:
            custom.loadPluginFile(p)

    # default output format inferred
    # from output filename or, failing
    # that, tsv
    if args.format is None:
        fmt = op.splitext(args.outfile)[1].lower().strip('.')
        if fmt in ('h5', 'hdf'):
            fmt = 'hdf5'
        if not custom.exists('exporter', fmt):
            fmt = 'tsv'
        args.format = fmt

    # error if any loaders/formats are
    # invalid (we can only perform this
    # check after plugins have been
    # loaded)
    if args.loader is not None:
        for f, l in args.loader.items():
            if not custom.exists('loader', l):
                raise ValueError('Unknown loader {} [{}]'.format(l, f))
    if not custom.exists('exporter', args.format):
        raise ValueError('Unknown output format {}'.format(args.format))
    if args.date_format is not None and \
       not custom.exists('formatter', args.date_format):
        raise ValueError('Unknown date format {}'.format(args.date_format))
    if args.time_format is not None and \
       not custom.exists('formatter', args.time_format):
        raise ValueError('Unknown time format {}'.format(args.time_format))
    if args.var_format is not None:
        for v, f in args.var_format.items():
            if not custom.exists('formatter', f):
                raise ValueError('Unknown formatter {} [{}]'.format(f, v))

    if args.num_jobs > 1:
        log.debug('Running up to %i jobs in parallel', args.num_jobs)

        # Funpack relies on fork() to share
        # the dataset to child processes
        # when parallelising tasks. This
        # is potentially dangerous on macOS
        # - see the "macOS issues" note in
        # README, and the python bug report:
        # https://bugs.python.org/issue33725
        if mp.get_start_method(True) is None:
            mp.set_start_method('fork')

        # The icd10 module maintains information
        # which is potentially shared (read from
        # and written to) by multiple processes,
        # so we use a mp.Manager to handle
        # shared state.
        mgr = mp.Manager()
        icd10.initialise(mgr)
    else:
        mgr = None

    with util.timed(None, log, fmt='Total time: %s (%+iMB)'):

        dtable, unknowns, uncategorised, drop = doImport(args, mgr)

        if args.dry_run:
            dryrun.doDryRun(dtable, unknowns, uncategorised, drop, args)
        else:
            doCleanAndProcess(  dtable, args)
            doExport(           dtable, args)
            doUnknownsExport(   dtable, args, unknowns, uncategorised)
            doICD10Export(              args)
            doDescriptionExport(dtable, args)
            doSummaryExport(    dtable, args)

    return 0


def doImport(args, mgr):
    """Data import stage.

    :arg args: :class:`argparse.Namespace` object containing command line
               arguments
    :arg mgr:  :class:`multiprocessing.Manager` object for parallelisation (may
               be ``None``)

    :returns:  A tuple containing:

                - A :class:`.DataTable` containing the data
                - A sequence of :class:`.Column` objects representing the
                  unknown columns.
                - A sequence of :class:`.Column` objects representing columns
                  which are uncategorised, and have no processing or cleaning
                  rules specified on them.
                - A list of :class:`.Column` objects that were not loaded from
                  each input file.
    """

    # if --remove_duplicates, we append
    # an identifying suffix to the names
    # of columns to be removed. This is
    # then passed through as an exclusion
    # pattern to the importData function
    # via its excludeColnames option.
    if args.remove_duplicates:
        suffix           = importing.REMOVE_DUPLICATE_COLUMN_IDENTIFIER
        renameDuplicates = True
    else:
        suffix           = None
        renameDuplicates = args.rename_duplicates

    finfo = fileinfo.FileInfo(args.infile,
                              indexes=args.index,
                              loaders=args.loader,
                              encodings=args.encoding,
                              renameDuplicates=renameDuplicates,
                              renameSuffix=suffix)

    with util.timed('Table import', log):
        vartable, proctable, cattable, unknowns, uncategorised = \
            loadtables.loadTables(
                finfo,
                args.variable_file,
                args.datacoding_file,
                args.type_file,
                args.processing_file,
                args.category_file,
                noBuiltins=args.no_builtins,
                naValues=args.na_values,
                childValues=args.child_values,
                recoding=args.recoding,
                clean=args.clean,
                typeClean=args.type_clean,
                globalClean=args.global_clean,
                skipProcessing=args.skip_processing,
                prependProcess=args.prepend_process,
                appendProcess=args.append_process)


    subjects, exprs = args.subject
    if suffix is None: excludeColnames = []
    else:              excludeColnames = [suffix]

    # Import data
    with util.timed('Data import', log):
        dtable, drop = importing.importData(
            fileinfo=finfo,
            vartable=vartable,
            proctable=proctable,
            cattable=cattable,
            variables=args.variable,
            colnames=args.column,
            excludeColnames=excludeColnames,
            categories=args.category,
            subjects=subjects,
            subjectExprs=exprs,
            exclude=args.exclude,
            excludeVariables=args.exclude_variable,
            excludeCategories=args.exclude_category,
            trustTypes=args.trust_types,
            mergeAxis=args.merge_axis,
            mergeStrategy=args.merge_strategy,
            indexVisits=args.index_visits,
            dropNaRows=args.drop_na_rows,
            njobs=args.num_jobs,
            mgr=mgr,
            dryrun=args.dry_run)

    # Filter unknown/uncategorised
    # column lists to only contain
    # those that were loaded
    allcols       = dtable.dataColumns
    unknowns      = [c for c in unknowns      if c in allcols]
    uncategorised = [c for c in uncategorised if c in allcols]

    # if it appears that we're doing
    # a full run on a large data set,
    # emit warnings about unknown/
    # uncategorised variables.
    bigrun = any((args.variable_file   is not None,
                  args.datacoding_file is not None,
                  args.processing_file is not None,
                  args.category_file   is not None))

    if bigrun:
        for u in unknowns:
            log.warning('Variable %s [file %s, column %s, assigned '
                        'variable ID %s] is unknown.',
                        u.name, u.datafile, u.index, u.vid)
        for u in uncategorised:
            log.warning('Variable %s [file %s, column %s, assigned '
                        'variable ID %s] is uncategorised.',
                        u.name, u.datafile, u.index, u.vid)

    return dtable, unknowns, uncategorised, drop


def doCleanAndProcess(dtable, args):
    """Data cleaning and processing stage.

    :arg dtable: :class:`.DataTable` containing the data
    :arg args:   :class:`argparse.Namespace` object containing command line
                 arguments
    :arg pool:   :class:`multiprocessing.Pool` object for parallelisation (may
                 be ``None``)
    """

    # Clean data (it times each step individually)
    cleaning.cleanData(
        dtable,
        skipNAInsertion=args.skip_insertna,
        skipCleanFuncs=args.skip_clean_funcs,
        skipChildValues=args.skip_childvalues,
        skipRecoding=args.skip_recoding)

    # Process data
    with util.timed('Data processing', log):
        processing.processData(dtable)


def splitDataTable(dtable, args):
    """Splits the .:class:`DataTable` into separate numeric/non-numeric tables.

    Called by :func:`doExport`.  If the ``--suppress_non_numerics`` and/or
    ``--write_non_numerics`` options are active, non-numeric columns need to
    be separated from numeric columns, and possibly saved to a separate output
    file.

    :arg dtable: :class:`.DataTable` containing the data
    :arg args:   :class:`argparse.Namespace` object containing command line
                 arguments
    :returns:    A list of ``(DataTable, filename)`` tuples, containing the
                 :class:`.DataTable` instances and corresponding output
                 file names.
    """

    # We're outputting one main output file
    # with all columns - no need to split
    if not (args.suppress_non_numerics or args.write_non_numerics):
        return [(dtable, args.outfile)]

    # we need to separate out numeric from
    # non-numeric columns, and potentially
    # create two separate datatables
    dtables = []
    ncols   = []
    nncols  = []

    # we run a single value from each
    # column through formatting in
    # order to determine whether each
    # column is numeric or non-numeric
    for col in dtable.dataColumns:

        idx = dtable[:, col.name].first_valid_index()

        # column is all nan
        if idx is None:
            continue

        # format a subtable containing
        # just the column and the first
        # non-na value
        series = exporting.formatColumn(
            col,
            dtable.subtable([col], [idx]),
            dateFormat=args.date_format,
            timeFormat=args.time_format,
            formatters=args.var_format)[:, col.name]

        # separate accordingly
        if pdtypes.is_numeric_dtype(series): ncols .append(col)
        else:                                nncols.append(col)

    # if suppress, only numeric columns
    # are saved to main output file
    if args.suppress_non_numerics:
        log.debug('Separating out %u / %u numeric columns for export',
                  len(ncols), len(dtable.dataColumns))
        dtables.append((dtable.subtable(ncols), args.outfile))
    else:
        dtables.append((dtable, args.outfile))

    # if write, non-numeric columns
    # are saved to an auxillary file
    if args.write_non_numerics:
        log.debug('Separating out %u / %u non-numeric columns for export',
                  len(nncols), len(dtable.dataColumns))
        dtables.append((dtable.subtable(nncols), args.non_numerics_file))

    return dtables


def doExport(dtable, args):
    """Data export stage.

    :arg dtable: :class:`.DataTable` containing the data
    :arg args:   :class:`argparse.Namespace` object containing command line
                 arguments
    """

    # if ids_only is specified, all we
    # need to do is output the index
    if args.ids_only:
        with open(args.outfile, 'wt') as f:
            for i in dtable.index:
                f.write(f'{i}\n')
        return

    # Otherwise we are exporting the full
    # data set, and things become more
    # complicated...

    # List of data tables and file names
    # for export (we may split the dtable
    # up into two - numeric/non-numeric)
    dtables = splitDataTable(dtable, args)

    # If not parallelising, we export the
    # entire file in one go. Because what's
    # the point in chunked export if we're
    # not parallelising across chunks?
    if args.num_jobs <= 1:
        args.num_rows = len(dtable)

    with util.timed('Data export', log):
        for dtable, outfile in dtables:

            # set the DataTable singleton for
            # shared mem to child processes
            # during export.
            datatable.DataTable.setInstance(dtable)

            exporting.exportData(
                dtable,
                outfile,

                # General export options
                fileFormat=args.format,
                numRows=args.num_rows,
                dropNaRows=args.drop_na_rows,
                dateFormat=args.date_format,
                timeFormat=args.time_format,
                formatters=args.var_format,

                # TSV options
                escapeNewlines=args.escape_newlines,
                sep=args.tsv_sep,
                missingValues=args.tsv_missing_values,

                # HDF5 options
                key=args.hdf5_key,
                style=args.hdf5_style)


def doICD10Export(args):
    """If a ``--icd10_map_file`` has been specified, the ICD10 codes present
    in the data (and their converted values) are saved out to the file.
    """
    if args.icd10_map_file is None:
        return

    with util.timed('ICD10 mapping export', log):
        try:
            ihier = hierarchy.getHierarchyFilePath(name='icd10')
            ihier = hierarchy.loadHierarchyFile(ihier)
            icd10.saveCodes(args.icd10_map_file, ihier)

        except Exception as e:
            log.warning('Failed to export ICD10 mappings: {}'.format(e),
                        exc_info=True)


def doDescriptionExport(dtable, args):
    """If a ``--description_file`` has been specified, a description for every
    column is saved out to the file.
    """
    if args.description_file is None:
        return

    with util.timed('Description export', log):
        cols = dtable.dataColumns

        try:
            with open(args.description_file, 'wt') as f:
                for col in cols:
                    desc = generateDescription(dtable, col)
                    f.write('{}\t{}\n'.format(col.name, desc))

        except Exception as e:
            log.warning('Failed to export descriptions: {}'.format(e),
                        exc_info=True)


def generateDescription(dtable, col):
    """Called by :func:`doDescriptionExport`. Generates and returns a
    suitable description for the given column.

    :arg dtable: :class:`.Datatable` instance
    :arg col:    :class:`.Column` instance
    """
    vartable = dtable.vartable
    desc     = vartable.loc[col.vid, 'Description']

    if pd.isna(desc) or (desc == col.name):
        desc = 'n/a'

    # If metadata has been added to the column,
    # we add it to the description. See the
    # binariseCategorical processing function
    # for an example of this.
    if col.metadata is not None:
        suffix = ' ({})'.format(col.metadata)
    else:
        suffix = ' ({}.{})'.format(col.visit, col.instance)

    return '{}{}'.format(desc, suffix)


def doUnknownsExport(dtable, args, unknowns, uncategorised):
    """If the ``--unknown_vars_file`` argument was used, the unknown/
    unprocessed columns are saved out to a file.

    :arg dtable:        :class:`.DataTable` containing the data
    :arg args:          :class:`argparse.Namespace` object containing command
                        line arguments
    :arg unknowns:      List of :class:`.Column` objects representing the
                        unknown columns.
    :arg uncategorised: A sequence of :class:`.Column` objects representing
                        columns which are uncategorised, and have no processing
                        or cleaning rules specified on them.
    """

    if args.unknown_vars_file is None:
        return

    if len(unknowns) + len(uncategorised) == 0:
        return

    # Save unknown/uncategorised
    # vars list to file columns:
    #  - name      - column name
    #  - file      - originating input file
    #  - class     - unknown or uncategorised
    #  - exported  - whether column passed processing and was exported
    allcols     = list(dtable.dataColumns)
    allunknowns = list(unknowns + uncategorised)

    names       = [u.name            for u in allunknowns]
    files       = [u.datafile        for u in allunknowns]
    classes     = ['unknown'         for u in unknowns] + \
                  ['uncategorised'   for u in uncategorised]
    exported    = [int(u in allcols) for u in allunknowns]
    rows        = ['{}\t{}\t{}\t{}'.format(n, f, c, e)
                   for n, f, c, e in zip(names, files, classes, exported)]

    log.debug('Saving unknown/uncategorised variables to %s',
              args.unknown_vars_file)

    try:
        with open(args.unknown_vars_file, 'wt') as f:
            f.write('name\tfile\tclass\texported\n')
            f.write('\n'.join(rows))

    except Exception as e:
        log.warning('Error saving unknown variables to {}: '
                    '{}'.format(args.unknown_vars_file, e),
                    exc_info=True)


def doSummaryExport(dtable, args):
    """If a ``--summary_file`` has been specified, a summary of the cleaning
    steps that have been applied to each variable are saved out to the file.
    """
    if args.summary_file is None:
        return

    vartable = dtable.vartable
    vids     = sorted(dtable.variables)[1:]
    sumdf    = pd.DataFrame(columns=['NAValues', 'RawLevels', 'NewLevels',
                                     'ParentValues', 'ChildValues',
                                     'Clean', 'Flags'], index=vids)
    sumdf.index.name = 'ID'

    with util.timed('Summary export', log):
        for vid in vids:
            sumdf.at[vid, 'NAValues']     = vartable.at[vid, 'NAValues']
            sumdf.at[vid, 'RawLevels']    = vartable.at[vid, 'RawLevels']
            sumdf.at[vid, 'NewLevels']    = vartable.at[vid, 'NewLevels']
            sumdf.at[vid, 'ParentValues'] = vartable.at[vid, 'ParentValues']
            sumdf.at[vid, 'ChildValues']  = vartable.at[vid, 'ChildValues']

            clean = vartable.at[vid, 'Clean']
            if pd.notna(clean):
                sumdf.at[vid, 'Clean'] = list(clean.values())

            flagstr  = []
            cols     = dtable.columns(vid)
            colflags = {c : dtable.getFlags(c) for c in cols}
            flags    = set.union(*colflags.values())

            for flag in flags:
                if all([flag in colflags[c] for c in cols]):
                    flagstr.append(flag)
                else:
                    names = [c.name for c in cols if flag in colflags[c]]
                    flagstr.append('{} [{}]'.format(flag, ', '.join(names)))

            sumdf.at[vid, 'Flags'] = ';'.join(flagstr)

        sumdf.to_csv(args.summary_file, sep='\t')


def configLogging(args):
    """Configures ``funpack`` logging.

    :arg args: ``argparse.Namespace`` object containing parsed command line
               arguments.
    """

    # Custom log handler which
    # colours messages
    class LogHandler(logging.StreamHandler):

        def emit(self, record):

            levelno = record.levelno

            if   levelno >= logging.WARNING:  colour = '\x1b[31;1m'
            elif levelno >= logging.INFO:     colour = '\x1b[39;1m'
            elif levelno >= logging.DEBUG:    colour = '\x1b[90;1m'
            else:                             colour = ''

            # Reset terminal attributes
            # after each message.
            record.msg = '{}{}\x1b[0m'.format(colour, record.msg)

            return super(LogHandler, self).emit(record)

    logger = logging.getLogger('funpack')
    fmt    = logging.Formatter('%(asctime)s '
                               '%(levelname)8.8s '
                               '%(filename)20.20s '
                               '%(lineno)4d: '
                               '%(funcName)-15.15s - '
                               '%(message)s',
                               '%H:%M:%S')

    if args.log_file is None: handler = LogHandler()
    else:                     handler = logging.FileHandler(args.log_file)

    handler.setFormatter(fmt)
    logger.addHandler(handler)

    # configure verbosity
    if   args.quiet:      loglevel = logging.CRITICAL
    elif args.noisy == 0: loglevel = logging.INFO
    else:                 loglevel = logging.DEBUG

    logging.getLogger('funpack').setLevel(loglevel)

    if args.quiet or args.noisy < 3:
        warnings.filterwarnings('ignore',  module='pandas')
        warnings.filterwarnings('ignore',  module='numpy')
        warnings.filterwarnings('ignore',  module='tables')

    if args.noisy == 1:
        makequiet = ['funpack.expression',
                     'funpack.custom',
                     'funpack.cleaning_functions',
                     'funpack.processing_functions']
    elif args.noisy == 2:
        makequiet = ['funpack.expression',
                     'funpack.custom']
    else:
        makequiet = []

    for mod in makequiet:
        logging.getLogger(mod).setLevel(logging.INFO)


if __name__ == '__main__':
    sys.exit(main())
