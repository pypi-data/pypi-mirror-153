#!/usr/bin/env python
#
# processing.py - Cleaning and processing parsing and functions.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains functionality for parsing and running "processes",
processing steps which are applied to one or more variables, and which may
result in columns being removed from, or new columns being added to, the
data table. These processes are specified in the processing table.


The parsing and execution functionality in this module are also used to manage
cleaning functions, which are specified in the ``Clean`` column of the
variable table. Definitions of all available (pre-)processing functions are in
the :mod:`cleaning_functions` and :mod:`.processing_functions` modules.


The :func:`processData` function is also defined here - it executes the
processes defined in the processing table.


Special processing functions can be applied to a variable's data by adding
them to the ``Clean`` and ``Process``  of the variable or processing
table respectively.  Processing is specified as a comma-separated list of
process functions - for example::


    process1, process2(), process3('arg1', arg2=1234)


The :func:`parseProcesses` function parses such a line, and returns a list of
:class:`Process` objects which can be used to query the process name and
arguments, and to run each process.


The processing table
--------------------


Within the processing table, the above process specification is preceeded by a
variable definition, which states which variables the process should be
applied to, and how they should be applied - either independently, or
together. This information is used to parallelise the processing where
possible.


For each process, the processing table contains a "process variable type", a
list of vids, and the process itself.  The process variable type is one of
the following:

  - No process variable type, simply a comma-separated list of VIDS, The
    process is applied to the specified vids::

        1,2,3 processName

  - ``'independent'``: The process is applied independently to the specified
    vids::

        independent,1,2,3 processName

  - ``'all'``: The process is applied to all vids::

        all processName

  - ``'all_independent'``: The process is applied independently to all vids::

       all_independent processName

  - ``'all_except'``: The process is applied to all vids except the specified
    ones::

       all_except,1,2,3 processName

  - ``'all_independent_except'``: The process is applied independently to all
    vids except the specified ones::

       all_independent_except,1,2,3 processName


For example, the :func:`.processing_functions.binariseCategorical` function
applies its logic independently to each variable, so it makes sense to specify
that it should be applied independently to a set of variables::

    independent,1,2,3,4,5 binariseCategorical

However, the :func:`.removeIfRedundant` function works on a collection of
variables (probably all variables in the data set), and this must be specified
in the processing table.

    all,1,2,3,4,5 removeIfRedundant(0.99)


Broadcasting arguments
----------------------

When a process is applied independently to more than one variable, the input
arguments to the process may need to be different for each variable. This can
be accomplished by using a _broadcast_ argument - simply prefix the argument
name with ``'broadcast_'``, and then specify a list containing the argument
values for each variable. For example, the following specification will result
in the :func:`.processing_functions.binariseCategorical` process being applied
independently to variables 1, 2, and 3, with values taken from variables 4, 5,
and 6 respectively.

    independent,1,2,3 binariseCategorical(broadcast_take=[4, 5, 6])

Note that broadcast arguments are useful as a performance optimisation - the
above specification is functionally equivalent to::

    1 binariseCategorical(take=4)
    2 binariseCategorical(take=5)
    3 binariseCategorical(take=6)

however the latter example cannot take advantage of parallelism in a
multi-core environment.
"""


import functools       as ft
import itertools       as it
import os.path         as op
import                    os
import                    glob
import                    logging
import                    tempfile
import                    collections
import collections.abc as abc

import pyparsing as pp
import pandas    as pd

from . import util
from . import custom


log = logging.getLogger(__name__)


def processData(dtable):
    """Applies all processing specified in the processing table to the data.

    :arg dtable: The :class:`DataTable` instance.
    """

    for i in dtable.proctable.index:

        procs, vids, parallel = retrieveProcess(dtable, i)
        allvids               = list(it.chain(*vids))

        if len(allvids) == 0:
            continue

        # Run each process sequentially -
        # each process may be parallelised
        # by the runProcess function
        for proc in procs.values():

            log.debug('Running process %s on %u variables %s ...',
                      proc.name, len(allvids), allvids[:5])

            fmt = '[{} {} ...] completed in %s (%+iMB)'.format(
                proc.name, allvids[:5])

            with util.timed(proc.name, log, logging.DEBUG, fmt=fmt), \
                 tempfile.TemporaryDirectory() as workDir:
                runProcess(proc, dtable, vids, workDir, parallel)


def retrieveProcess(dtable, procIdx):
    """Used by :func:`processData`. Retrieves the process at index ``procIdx``
    in the processing table, and generates the variable groups that the
    process should be applied to.

    :arg dtable:  The :class:`.DataTable`
    :arg procIdx: Index into the processing table
    :returns:     A tuple containing:

                    - A dict of ``{ name : Process }`` mappings containing
                      the :class:`.Process` objects to be executed.

                    - A list of lists, each list containing a group of
                      variable IDs that the process should be applied to

                    - ``True`` if the process can be applied in parallel
                      across the variable groups, ``False`` otherwise.
    """

    i         = procIdx
    ptable    = dtable.proctable
    all_vids  = dtable.variables
    all_vids  = [v for v in all_vids if v != 0]

    # For each process, the processing table
    # contains a "process variable type",
    # a list of vids, and the process itself.
    # The pvtype is one of:
    #   - vids:                   apply the process to the specified vids
    #   - independent:            apply the process independently to the
    #                             specified vids
    #   - all:                    apply the process to all vids
    #   - all_independent:        apply the process independently to all
    #                             vids
    #   - all_except:             apply the process to all vids except the
    #                             specified ones
    #   - all_independent_except: apply the process independently to all
    #                             vids except the specified ones
    pvtype, vids = ptable.loc[i, 'Variable']
    procs        = ptable.loc[i, 'Process']

    # Build a list of lists of vids, with
    # each vid list a group of variables
    # that is to be processed together.

    # apply independently to every variable
    if pvtype in ('all_independent', 'all_independent_except'):
        if pvtype.endswith('except'): exclude = vids
        else:                         exclude = []
        vids = [[v] for v in all_vids if v not in exclude]

    # apply simultaneously to every variable
    elif pvtype in ('all', 'all_except'):
        if pvtype.endswith('except'): exclude = vids
        else:                         exclude = []
        vids = [[v for v in all_vids if v not in exclude]]

    # apply independently to specified variables
    elif pvtype == 'independent':
        vids = [[v] for v in vids]

    # apply simultaneously to specified variables
    else:  # ptype == 'vids'
        vids = [vids]

    return procs, vids, 'independent' in pvtype


def runProcess(proc, dtable, vids, workDir, parallel):
    """Called by :func:`processData`. Runs the given process, and updates
    the :class:`.DataTable` as needed.

    :arg proc:      :class:`.Process` to run.
    :arg dtable:    :class:`.DataTable` containing the data.
    :arg workDir:   Directory to save/load new columns to/from, if the
                    processing is performed in a worker process.
    :arg vids:      List of lists, groups of variable IDs to run the process
                    on.
    :arg parallel:  If ``True``, each variable group is processed in parallel.
                    Otherwise they are processed sequentially.
    """

    results = []

    def filterMissing(vids):
        """Takes a list of variable IDs and removes those that are not
        present in the data set, emitting a warning for each ID that
        is removed.
        """
        if not proc.filterMissing:
            return vids
        filtered = []
        for vid in vids:
            if dtable.present(vid):
                filtered.append(vid)
            else:
                log.warning('Process %s refers to missing variable %u! '
                            '(%s)', proc.name, vid, proc.processString)
        return filtered

    # run process serially
    if not parallel:
        for vg in vids:
            vg = filterMissing(vg)
            results.append(proc.run(dtable, vg))

    # or run in parallel across vid groups
    else:
        with dtable.pool() as pool:

            # Note. This code is horrible for a number of
            # reasons, including that parallelisation in
            # older versions of FUNPACK worked differently,
            # and for the sake of preserving backwards
            # compatibility with resepct to the use of the
            # argument broadcast feature (although I
            # seriously doubt that anybody is even using
            # broadcasting).

            # gather all variables required by this process -
            # the ones which are specified in the processing
            # table, along with any auxillary ones speciified
            # as arguments to the process. "allvids" is used
            # to creae the sub-table, and "vids" is the list
            # of vids that we ask the processing function to
            # process.
            unfiltered = vids
            vids       = []
            allvids    = []
            bcastIdxs  = []

            for i, vg in enumerate(unfiltered):
                vg      = filterMissing(vg)
                auxvids = filterMissing(proc.auxillaryVariables(i))
                if len(vg) > 0:
                    vids     .append(vg)
                    allvids  .append(vg + auxvids)
                    bcastIdxs.append(i)

            # generate a subtable for each variable group -
            # this is to minimise the amount of data that
            # needs to be transferred to worker processes,
            # if we are parallelising.
            allcols    = [list(it.chain(*[dtable.columns(v) for v in vg]))
                          for vg in allvids]
            subtables  = [dtable.subtable(cols) for cols in allcols]

            # separate work dir for each variable group
            workDirs   = [op.join(workDir, str(i))
                          for i in range(len(vids))]
            func       = ft.partial(runParallelProcess, proc)
            parresults = pool.starmap(func, zip(subtables,
                                                vids,
                                                workDirs,
                                                bcastIdxs))

            subtables, parresults = zip(*parresults)

            results.extend(parresults)

            # Merge results back in - this
            # includes in-place modifications
            # to columns, and column flags/
            # metadata. Added/removed columns
            # are handled below.
            log.debug('Processing for %u vid groups complete - merging '
                      'results into main data table.', len(subtables))
            dtable.merge(subtables)

    remove    = []
    add       = []
    addvids   = []
    addkwargs = []

    for r in results:
        results = unpackResults(proc, r)
        remove   .extend(results[0])
        add      .extend(results[1])
        addvids  .extend(results[2])
        addkwargs.extend(results[3])

    # Parallelised processes save new
    # series to disk - load them back in.
    if log.getEffectiveLevel() >= logging.DEBUG:
        savedSeries = list(glob.glob(
            op.join(workDir, '**', '*.pkl'), recursive=True))
        if len(savedSeries) > 0:
            log.debug('[%s]: Reading %u new columns from %s %s ...',
                      proc.name, len(savedSeries), workDir, vids[:5])

    for i in range(len(add)):
        if isinstance(add[i], str):
            add[i] = pd.read_pickle(add[i])

    # remove columns first, in case
    # there is a name clash between
    # the old and new columns.
    if len(remove) > 0: dtable.removeColumns(remove)
    if len(add)    > 0: dtable.addColumns(add, addvids, addkwargs)


def runParallelProcess(proc, dtable, vids, workDir, broadcastIndex=None):
    """Used by :func:`runProcess`. Calls ``proc.run``, and returns its
    result and the (possibly modified) ``dtable``.

    :arg proc:           :class:`Process` to run
    :arg dtable:         :class:`DataTable` instance (probably a subtable)
    :arg vids:           List of variable IDs
    :arg workDir:        Directory to save new columns to if running in
                         a worker process - this is used to reduce the
                         amount of data that must be transferred between
                         processes.
    :arg broadcastIndex: Index to use for broadcast arguments - passed
                         through to the :meth:`Process.run` method.
    :returns:            A tuple containing:
                          - A reference to ``dtable``
                          - the result of ``proc.run()``
    """
    os.mkdir(workDir)
    result = proc.run(dtable, vids, broadcastIndex=broadcastIndex)
    remove, add, addvids, addkwargs = unpackResults(proc, result)

    # New columns are saved to disk,
    # rather than being copied back
    # to the parent process. We only
    # do this if running in a
    # multiprocessing context
    if not util.inMainProcess() and len(add) > 0:
        log.debug('[%s]: Saving %u new columns to %s %s...',
                  proc.name, len(add), workDir, vids[:5])
        for i, series in enumerate(add):
            fname  = op.join(workDir, '{}.pkl'.format(i))
            add[i] = fname
            series.to_pickle(fname)

    return dtable, (remove, add, addvids, addkwargs)


def unpackResults(proc, result):
    """Parses the results returned by a :class:`.Process`. See the
    :mod:`.processing_functions` module for details on what can be returned
    by a processing function.

    :arg proc:   The :class:`.Process`
    :arg result: The value returned by :meth:`.Process.run`.
    :returns:    A tuple containing:
                  - List of columns to remove
                  - List of new series to add
                  - List of variable IDs for new series
                  - List of :class:`.Column` keyword arguments for new series
    """

    remove    = []
    add       = []
    addvids   = []
    addkwargs = []

    if result is None:
        return remove, add, addvids, addkwargs

    error = ValueError('Invalid return value from '
                       'process {}'.format(proc.name))

    def expand(res, length):
        if res is None: return [None] * length
        else:           return res

    # columns to remove
    if isinstance(result, list):
        remove.extend(result)

    elif isinstance(result, tuple):

        # series/vids to add
        if len(result) == 2:
            add      .extend(result[0])
            addvids  .extend(expand(result[1], len(result[0])))
            addkwargs.extend(expand(None,      len(result[0])))

        # columns to remove, and
        # series/vids to add
        elif len(result) in (3, 4):

            if len(result) == 3:
                result = list(result) + [None]

            remove   .extend(result[0])
            add      .extend(result[1])
            addvids  .extend(expand(result[2], len(result[1])))
            addkwargs.extend(expand(result[3], len(result[1])))
        else:
            raise error
    else:
        raise error

    return remove, add, addvids, addkwargs


class NoSuchProcessError(Exception):
    """Exception raised by the :class:`Process` class when an unknown
    process name is specified.
    """


class Process:
    """Simple class which represents a single processing step. The :meth:`run`
    method can be used to run the process on the data for one or more
    variables.
    """


    def __init__(self, ptype, name, args, kwargs, procstr):
        """Create a ``Process``.

        :arg ptype:   Process type - either ``cleaner`` or ``processor``
                      (see the :mod:`.custom` module).
        :arg name:    Process name
        :arg args:    Positional arguments to pass to the process function.
        :arg kwargs:  Keyword arguments to pass to the process function.
        :arg procstr: Input string containing the process specification.

        Any keyword arguments which begin with ``'broadcast_'`` are separated
        out the other keyword arguments - see the :meth:`run` method for more
        details.
        """

        bcastKwargs  = collections.OrderedDict()
        normalKwargs = collections.OrderedDict()

        for k, v in kwargs.items():
            if k.startswith('broadcast_'):
                k              = '_'.join(k.split('_')[1:])
                bcastKwargs[k] = v
            else:
                normalKwargs[k] = v

        # cleaner functions are not
        # defined in processing_functions,
        # so in this case func will be None.
        self.__ptype         = ptype
        self.__name          = name
        self.__args          = args
        self.__kwargs        = normalKwargs
        self.__procstr       = procstr
        self.__bcastKwargs   = bcastKwargs
        self.__metaproc      = normalKwargs.pop('metaproc', None)


    def __repr__(self):
        """Return a string representation of this ``Process``."""
        args    = ','.join([str(v) for v in self.__args])
        kwargs  = ','.join(['{}={}'.format(k, v) for k, v in
                           it.chain(self.__kwargs.items(),
                                    self.__bcastKwargs.items())])

        allargs = [args, kwargs]
        allargs = [a for a in allargs if a != '']
        allargs = ', '.join(allargs)
        return '{}[{}]({})'.format(self.__name, self.__ptype, allargs)


    @property
    def name(self):
        """Returns the name of this ``Process``. """
        return self.__name


    @property
    def args(self):
        """Returns the positional arguments for this ``Process``. """
        return self.__args


    @property
    def kwargs(self):
        """Returns the keyword arguments for this ``Process``. """
        return self.__kwargs


    @property
    def processString(self):
        """Returns the original string, from the processing table/
        command-line, which defines this ``Process``.
        """
        return self.__procstr


    @property
    def broadcastKwargs(self):
        """Returns the keyword arguments for this ``Process`` which
        will broadcasted across all variable IDs that are passed to
        an invocation of :meth:`run`.
        """
        return self.__bcastKwargs


    @property
    def filterMissing(self):
        """Return ``True`` if this processing function expects that the list of
        variable IDs which it is given will not contain the IDs of variables
        which are not present in the data.

        This property is set via a ``filterMissing`` argument passed to the
        processor decorator function. Its default value is ``True``.

        Note: This is a hack which is only used by the
        :func:`.processing_functions.binariseCategorical` function, and which
        is in place because that function used to be parallelised differently.
        """
        return custom.args(self.__ptype, self.__name).get('filterMissing', True)


    def auxillaryVariables(self, broadcastIndex=None):
        """Returns a list of "auxillary" variables for this process. Auxillary
        variables are variables which a process is not being applied to, but
        which is needed by the process. These variables are passed in as
        arguments to the process.

        The names of any arguments which contain auxillary variables are
        specified via the ``auxvids`` argument to the processor decorator
        function.

        Note: This is a hack which is only used by the
        :func:`.processing_functions.binariseCategorical` function, and which
        is in place because that function used to be parallelised differently.
        """

        auxargs = custom.args(self.__ptype, self.__name).get('auxvids', [])
        auxvids = []

        for arg in auxargs:
            if arg in self.kwargs:
                val = self.kwargs[arg]
            elif ((broadcastIndex is not None) and
                  (arg in self.broadcastKwargs)):
                val = self.broadcastKwargs[arg][broadcastIndex]
            else:
                continue

            if isinstance(val, abc.Sequence): auxvids.extend(val)
            else:                             auxvids.append(val)

        return auxvids


    def run(self, *args, broadcastIndex=None):
        """Run the process on the data, passing it the given arguments,
        and any arguments that were passed to :meth:`__init__`.

        :arg broadcastIndex: If provided, and if any broadcast arguments
                             were specified for this process, this index is
                             used to retrieve one value each broadcast argument
                             list - this value is then passed to the process
                             function.
        """

        kwargs = self.__kwargs.copy()
        bcast  = self.__bcastKwargs

        # retrieve the value for each broadcast argument,
        # and pass them in as regular keyword arguments
        if broadcastIndex is not None and len(bcast) > 0:
            for k, v in bcast.items():
                kwargs[k] = v[broadcastIndex]

        result = custom.run(self.__ptype,
                            self.__name,
                            *args,
                            *self.__args,
                            **kwargs)

        if self.__metaproc is not None and \
           isinstance(result, tuple)   and \
           len(result) == 4:

            # The first argument to a process
            # should be the data table
            dtable = args[0]

            # The 3rd/4th args returned from a
            # process should be a list of vids,
            # and a list of Column kwargs for
            # each of them
            vids      = result[2]
            kwargs    = result[3]
            mproc     = self.__metaproc
            newkwargs = []

            for vid, vkwargs in zip(vids, kwargs):

                if vkwargs is None or 'metadata' not in vkwargs:
                    newkwargs.append(vkwargs)
                    continue

                try:
                    vkwargs['metadata'] = custom.runMetaproc(
                        mproc, dtable, vid, vkwargs['metadata'])
                    newkwargs.append(vkwargs)

                except Exception as e:
                    log.warning('Metadata processing function '
                                'failed (vid %u): %s', vid, e)
                    newkwargs.append(vkwargs)

            result = tuple(list(result[:3]) + [newkwargs])

        return result


def parseProcesses(procs, ptype):
    """Parses the given string containing one or more comma-separated process
    calls, as defined in the processing table. Returns a list of
    :class:`Process` objects.

    :arg procs: String containing one or more comma-separated (pre-)processing
                steps.

    :arg ptype: either ``cleaner`` or ``processor``

    :returns:   A list of :class:`Process` objects.

    """

    def makeProcess(toks):
        name = toks[0]

        args   = ()
        kwargs = {}

        if len(toks) == 2:
            if isinstance(toks[1], tuple):
                args   = toks[1]
            elif isinstance(toks[1], dict):
                kwargs = toks[1]
        elif len(toks) == 3:
            args, kwargs = toks[1:]

        if not custom.exists(ptype, name):
            raise NoSuchProcessError(name)

        return Process(ptype, name, args, kwargs, procs)

    parser = pp.delimitedList(makeParser().setParseAction(makeProcess))

    try:
        parsed = parser.parseString(procs, parseAll=True)
    except Exception as e:
        log.error('Error parsing process list "{}": {}'.format(procs, e))
        raise e

    return list(parsed)


@ft.lru_cache()
def makeParser():
    """Generate a ``pyparsing`` parser which can be used to parse a single
    process call in the processing table.
    """

    lparen   = pp.Literal('(').suppress()
    rparen   = pp.Literal(')').suppress()
    lbracket = pp.Literal('[').suppress()
    rbracket = pp.Literal(']').suppress()

    def convertBoolean(tok):
        tok = tok[0]
        if   tok == 'True':  return True
        elif tok == 'False': return False
        else:                return tok

    def parseValList(toks):
        return [list(toks)]

    def parseArgs(toks):
        return [tuple(toks)]

    def parseKwargs(toks):
        kwargs = collections.OrderedDict()
        for i in range(0, len(toks), 2):
            kwargs[toks[i]] = toks[i + 1]
        return kwargs

    funcName = pp.pyparsing_common.identifier
    argval   = (pp.QuotedString('"')                                       ^
                pp.QuotedString("'")                                       ^
                pp.pyparsing_common.number                                 ^
                pp.oneOf(['True', 'False']).setParseAction(convertBoolean) ^
                pp.Literal('None').setParseAction(pp.replaceWith(None)))

    # argument values are either a
    # scalar, or a list of scalars
    # within square brackets
    vallist  = (lbracket + pp.delimitedList(argval) + rbracket)
    vallist  = vallist.setParseAction(parseValList)
    argval   = argval ^ vallist

    # arguments are either
    # positional or keyword
    kwargs   = (pp.pyparsing_common.identifier +
                pp.Literal('=').suppress() +
                argval)
    posargs  = pp.delimitedList(argval).setParseAction(parseArgs)
    kwargs   = pp.delimitedList(kwargs).setParseAction(parseKwargs)
    allargs  = pp.delimitedList(pp.Optional(posargs) + pp.Optional(kwargs))

    # function can be called as:
    #   function
    #   function()
    #   function(args)
    allargs  = lparen   + pp.Optional(allargs) + rparen
    function = funcName + pp.Optional(allargs)

    return function
