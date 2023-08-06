#!/usr/bin/env python
#
# fileinfo.py - Get information about input files.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains the :class:`FileInfo` class, and the :func:`sniff` and
:func:`fileinfo` functions, for getting information about input data files.
"""


import itertools         as it
import                      io
import                      csv
import                      logging
import                      collections

import funpack.util      as util
import funpack.custom    as custom
import funpack.datatable as datatable


log = logging.getLogger(__name__)


def has_header(sample,
               dialect,
               candidateTypes=None,
               missingValues=None):
    """Used in place of the ``csv.Sniffer.has_header`` method.

    The ``Sniffer.has_header`` method can fail in some circumstances, e.g.:

     - for files which only contain a single column.
     - for files which contain lots of missing values.

    This function works in essentially the same manner as the
    ``csv.Sniffer.has_header`` function, but handles the above situations.

    :arg sample:         Text sample.

    :arg dialect:        CSV dialect as returned by the ``csv.Sniffer.sniff``
                         method, or a string describing the dialect
                         (e.g. ``'whitespace'``).

    :arg candidateTypes: Sequence of types to check. Defaults to ``[float]``.

    :arg missingValues:  Sequence of missing values to ignore. Defaults to
                         ``['', 'na', 'n/a', 'nan']``. The missing value
                         test is case insensitive.

    :returns:            ``True`` if the sample looks like it contains a
                         header, ``False`` otherwise.
    """

    # default behaviour is simply
    # to test whether each value
    # is a number of not a number
    if candidateTypes is None: candidateTypes = [float]
    if missingValues  is None: missingValues  = ('', 'na', 'n/a', 'nan')

    def inferType(val):
        val = val.strip()

        # missing values get their own type
        if val.lower() in missingValues:
            return None

        for ct in candidateTypes:
            try:
                ct(val)
                return ct
            except (ValueError, OverflowError):
                pass

        # if none of the candidate types
        # match, we take the length of
        # the value, in the hope that the
        # column will have a different
        # length to the header row value
        return len(val)

    if dialect == 'whitespace':
        rows = [list(line.split()) for line in sample.split('\n')]
    else:
        rows = list(csv.reader(io.StringIO(sample), dialect))

    # not enough data
    if len(rows) < 2:
        return True

    # infer types for every
    # value in every row
    hdr      = rows[0]
    row      = rows[1:]
    hdrtypes = [inferType(v) for v in hdr]
    coltypes = collections.defaultdict(list)

    for row in rows:
        for i, col in enumerate(row):
            ct = inferType(col)

            # missing values are treated
            # like any other value - they
            # are given a type of "None"
            coltypes[i].append(ct)

    # we build a score based on the
    # number of columns for which it
    # looks like there is a header
    # row. If it looks true for more
    # than 50% of columns, we'll say
    # that there is a header.
    #
    # This process is very similar to
    # the implementation in
    # csv.Sniffer.has_header.
    colcount = 0

    # if more than two thirds of rows
    # have a different type to the header
    # row, let's say we have a header.
    # But be lenient at low row counts.
    threshold    = collections.defaultdict(lambda : 0.34)
    threshold[1] = 0.0
    threshold[2] = 0.51
    threshold[3] = 0.66
    threshold[4] = 0.76

    for col, ctypes in coltypes.items():

        t0    = hdrtypes[col]
        hist  = collections.Counter(ctypes)
        thres = threshold[len(ctypes)]
        score = hist[t0] / len(ctypes)

        # short-circuit - if the rows
        # of any single column do not
        # have the same type as the
        # first row, assume it is a
        # header row.
        if   hist[t0] == 1: return True
        elif score < thres: colcount += 1
        else:               colcount -= 1

    # If more columns than not passed
    # the threshold, let's say we have
    # a header. But be lenient at low
    # column counts.
    threshold    = collections.defaultdict(lambda : 1)
    threshold[2] = 0
    threshold[4] = 0
    threshold[6] = 0

    return colcount >= threshold[len(coltypes)]


def sniff(datafile, encoding=None):
    """Identifies the format of the given input data file.

    :arg datafile: Input data file
    :arg encoding: File encoding (default: ``'latin1'``)
    :returns:      A tuple containing:

                    - A ``csv`` dialect type

                    - List of ``Column`` objects. The ``name`` attributes will
                      be ``None`` if the file does not have a header row.
                      The ``variable``, ``visit``, and ``instance`` attributes
                      will be ``None`` if the file does not have UKB-style
                      column names.
    """
    if encoding is None:
        encoding = 'latin1'

    # Read the first few lines
    lines = []
    with open(datafile, 'rt', encoding=encoding) as f:
        for i in range(100):

            line = f.readline()

            # eof
            if len(line) == 0:
                break

            line = line.strip('\n')

            if len(line) > 0:
                lines.append(line)

    if len(lines) == 0:
        raise ValueError('Empty file: {}'.format(datafile))

    # Identify the CSV dialect (e.g.
    # tab- or comma-separated values)
    sniffer = csv.Sniffer()
    sample  = '\n'.join(lines)

    try:
        dialect = sniffer.sniff(sample, ' .,\t:;|/\\~!@#$~%^&*')
    except csv.Error:
        dialect = None

    # But if the sniffer failed, or detected
    # space-separated data, let's try and
    # test whether it is fixed-width or
    # variable-whitespace delimited data (as
    # the sniffer can't detect these formats).
    if dialect is None or dialect.delimiter == ' ':

        linewords = [line.split() for line in lines]

        # Heuristic 1: If the number of columns
        # differs depending on whether we split
        # on a single space, or variable
        # whitespace, then this might be a fixed-
        # width or variable-whitespace delimited
        # file.
        spacesneq = any([line.split(' ') != words
                         for line, words in zip(lines, linewords)])

        # Heuristic 2: If each line has the same
        # number of space-separated words, it
        # might be whitespace-delimited
        nwords    = [len(lw) for lw in linewords]
        avgwords  = float(sum(nwords)) / len(nwords)
        samewords = all([n == avgwords for n in nwords])

        # variable-whitespace delimited
        if spacesneq and samewords:
            dialect = 'whitespace'

        # file contains a single column
        elif samewords and nwords[0] == 1:
            dialect = 'whitespace'

    # Give up if it doesn't look like
    # CSV or whitespace delimited data
    if dialect is None:
        raise ValueError('Could not determine file format: '
                         '{}'.format(datafile))

    # Use the has_header function to
    # figure out if we have column names
    hasHeader = has_header(sample, dialect)

    # And take a copy of the first row,
    # in case we do have column names.
    if dialect == 'whitespace':
        firstRow = lines[0].split()
    else:
        reader   = csv.reader(io.StringIO(sample), dialect)
        firstRow = next(reader)

    log.debug('Detected dialect for input file %s: (header: %s, '
              'delimiter: %s)',
              datafile, hasHeader,
              dialect if isinstance(dialect, str) else dialect.delimiter)

    # Now create a Column object for
    # each column in the data file.
    columns = []

    for i, col in enumerate(firstRow):

        name     = None
        vid      = None
        visit    = None
        instance = None

        # If there is a header, extract
        # the columns and attempt to
        # identify UKB variables.
        if hasHeader:

            name = col

            try:
                vid, visit, instance = util.parseColumnName(col)
            except ValueError:
                pass

        columns.append(
            datatable.Column(datafile, name, i, vid, visit, instance))

    return dialect, columns


class FileInfo:
    """The ``FileInfo`` class is a container for the information generated
    by the :func:`fileinfo` function for a collection of input datafiles.
    """


    def __init__(self,
                 datafiles,
                 indexes=None,
                 loaders=None,
                 encodings=None,
                 renameDuplicates=False,
                 renameSuffix=None):
        """Create a ``FileInfo`` object.

        :arg datafiles:        Path to input file, or sequence of paths.
        :arg indexes:          Dict of ``{datafile : index}`` mappings,
                               specifying non-default (non-0) index column
                               locations.
        :arg loaders:          Dict of ``{datafile : loader}`` mappings,
                               specifying custom loader functions.
        :arg encodings:        Dict of ``{datafile : encoding}`` mappigs,
                               specifying non-standard file encodings.
        :arg renameDuplicates: If ``True``, duplicate columns are re-named -
                               see :func:`renameDuplicateColumns`.
        :arg renameSuffix:     Passed as ``suffix`` to
                               :func:`renameDuplicateColumns`, if
                               ``renameDuplicates is True``.
        """

        if isinstance(datafiles, str): datafiles = [datafiles]
        if indexes   is None:          indexes   = {}
        if loaders   is None:          loaders   = {}
        if encodings is None:          encodings = {}

        dialects, headers, cols = fileinfo(datafiles,
                                           indexes,
                                           loaders,
                                           encodings,
                                           renameDuplicates,
                                           renameSuffix=renameSuffix)

        self.__datafiles = list(datafiles)
        self.__indexes   = dict(indexes)
        self.__loaders   = dict(loaders)
        self.__encodings = dict(encodings)
        self.__dialects  = dict(zip(datafiles, dialects))
        self.__headers   = dict(zip(datafiles, headers))
        self.__cols      = dict(zip(datafiles, cols))


    @property
    def datafiles(self):
        """Return a list containing the data files. """
        return list(self.__datafiles)


    def dialect(self, datafile):
        """Return the CSV dialect type for the given ``datafile``. """
        return self.__dialects[datafile]


    def header(self, datafile):
        """Return ``True`` if the given ``datafile`` has a header row,
        ``False`` otherwise.
        """
        return self.__headers[datafile]


    def columns(self, datafile):
        """Return a list of :class:`.Column` objects representing each
        of the columns that are present in the given ``datafile``.
        """
        return list(self.__cols[datafile])


    def index(self, datafile):
        """Return the index column for the given data file. """
        return self.__indexes.get(datafile, [0])


    def loader(self, datafile):
        """Return the custom loader for the given ``datafile``, or ``None.`` if
        there is no custom loader.
        """
        return self.__loaders.get(datafile, None)


    def sniffer(self, datafile):
        """Return the custom sniffer for the given ``datafile``, or ``None`` if
        there is no custom sniffer.  This is equivalent to :meth:`loader`, as
        sniffer/loader functions are always paired.
        """
        return self.loader(datafile)


    def encoding(self, datafile):
        """Return the encoding for the given ``datafile``, or ``None`` if
        no custom encoding was specified. """
        return self.__encodings.get(datafile, None)


def fileinfo(datafiles,
             indexes=None,
             sniffers=None,
             encodings=None,
             renameDuplicates=False,
             renameSuffix=None):
    """Identifies the format of each input data file, and extracts/generates
    column names and variable IDs for every column.

    :arg datafiles:        Sequence of data files to be loaded.

    :arg indexes:          Dict containing ``{filename : [index]}`` mappings,
                           specifying which column(s) to use as the index.
                           Defaults to 0 (the first column).

    :arg sniffers:         Dict containing ``{file : snifferName}`` mappings,
                           specifying custom sniffers to be used for specific
                           files. See the :mod:`.custom` module.

    :arg encodings:        Dict of ``{datafile : encoding}`` mappings,
                           specifying non-standard file encodings. If not
                           specified, ``latin1`` is assumed.

    :arg renameDuplicates: Defaults to ``False``. If ``True``, columns
                           which have the same name are renamed - see
                           :func:`renameDuplicateColumns`.

    :arg renameSuffix:     Passed as ``suffix`` to
                           :func:`renameDuplicateColumns`, if
                           ``renameDuplicates is True``.

    :returns: A tuple containing:

               - List of ``csv`` dialect types

               - List  of booleans, indicating whether or not each file has a
                 header row.

               - List of lists, ``Column`` objects representing the columns
                 in each file.
    """

    if isinstance(datafiles, str):
        datafiles = [datafiles]

    if sniffers  is None: sniffers  = {}
    if indexes   is None: indexes   = {}
    if encodings is None: encodings = {}

    sniffers  = dict(sniffers)
    indexes   = dict(indexes)
    encodings = dict(encodings)

    # The index column for each file is
    # assumed to be the first column,
    # unless otherwise specified in the
    # indexes mapping.
    indexes = [indexes.get(f, [0]) for f in datafiles]

    # Situations we need to handle:
    #
    #  1. Data file is UKB-style - each column
    #     has a variable ID, visit, and instance
    #
    #  2. Data file has arbitray column names.
    #  3. Data file has no column names.
    #
    # In the latter two cases, we need to
    # generate variable IDs for each column
    # and, for the last case, generate
    # column names as well.
    dialects = []
    cols     = []

    for f in datafiles:

        sniffer  = sniffers. get(f, None)
        encoding = encodings.get(f, None)

        if sniffer is not None:
            dialect = 'custom ({})'.format(sniffer)
            fcols   = custom.runSniffer(sniffer, f)
        else:
            dialect, fcols = sniff(f, encoding)

        dialects.append(dialect)
        cols    .append(fcols)

    # Now we need to fix all non-UKB
    # style input files - generating
    # dummy variables, and generating/
    # mangling column names if necessary.
    headers = []
    autovid = datatable.AUTO_VARIABLE_ID
    for fi in range(len(datafiles)):

        fcols   = cols[   fi]
        idxcols = indexes[fi]

        # save whether or not each
        # file has a header row -
        # if not, all of the Column
        # instances returned by
        # the sniff function will
        # have a name equal to None
        headers.append(fcols[0].name is not None)

        for ci, col in enumerate(fcols):

            # Index columns always get
            # a variable ID of 0
            if ci in idxcols:
                vid = 0

            # UKB-style - we already
            # have a variable id, visit,
            # and instance.
            elif col.vid is not None:
                continue

            # Non-UKB style file - assign
            # a (vid, visit, instance) to
            # each column
            else:
                vid      = autovid
                autovid += 1

            col.vid      = vid
            col.basevid  = vid
            col.visit    = 0
            col.instance = 0

            # And generate a name for
            # each column if necessary
            if col.name is None:
                col.name = util.generateColumnName(vid, 0, 0)

    if renameDuplicates:
        renameDuplicateColumns(it.chain(*cols), suffix=renameSuffix)

    return dialects, headers, cols


def renameDuplicateColumns(cols, suffix=None):
    """Identifies any columns which have the same name, and re-names the
    subsequent ones.  If ``N`` columns have the same name ``X``, they are
    renamed ``X``, ``X.1<suffix>``, ``X.2<suffix>``, ``...``,
    ``X.<N-1><suffix>``.

    The ``name`` attribute of each :class:`.Column` object is modified
    in-place.

    :arg cols:   Sequence of :class:`.Column` objects.
    :arg suffix: String to append to the name of all renamed columns.
                 Defaults to an empty string.
    """

    if suffix is None:
        suffix = ''

    counts = collections.defaultdict(list)

    for col in cols:

        # do not rename index columns
        if col.vid == 0:
            continue

        counts[col.name].append(col)
        count = len(counts[col.name])
        if count > 1:
            newname  = '{}.{}{}'.format(col.name, count - 1, suffix)
            col.name = newname

            log.warning('Duplicate column detected (%s: %s) - renamed to %s',
                        col.datafile, col.origname, col.name)
