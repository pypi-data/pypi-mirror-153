#!/usr/bin/env python
#
# datatable.py - The DataTable class.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides the :class:`DataTable` class, a container
class which holds a reference to the loaded data.
"""


import itertools             as it
import multiprocessing       as mp
import multiprocessing.dummy as mpd
import                          random
import                          string
import                          logging
import                          contextlib
import                          collections
import collections.abc       as abc

import pandas                as pd

import funpack.util as util


log = logging.getLogger(__name__)


AUTO_VARIABLE_ID = 5000000
"""Starting variable ID to use for unknown data. Automatically generated
variable IDs really shoulld not conflict with actual UKB variable IDs.
"""


MODIFIED_COLUMN =  ''.join(random.choices(string.ascii_letters, k=20))
"""Flag used internally by the :class:`DataTable` when merging subtables.
"""


class Column:
    """The ``Column`` is a simple container class containing metadata
    about a single column in a data file.

    See the :func:`.parseColumnName` function for important information
    about column naming conventions in the UK BioBank.

    A fundamental assumption made throughout much of the ``funpack`` code-base
    is that columns with a variable ID (``vid``) equal to 0 are index columns
    (e.g. subject ID).

    A ``Column`` object has the following attributes:

     - ``datafile``: Input file that the column originates from (``None`` for
                     generated columns).

     - ``name``:     Column name.

     - ``origname``: Column name as it appears in the input/output file(s)

     - ``index``:    Location of the column in the input/output file(s)

     - ``vid``:      Variable ID

     - ``visit``:    Visit number

     - ``instance``: Instance number/code

     - ``metadata``: Metadata which may be used to generate descriptive
                     information about the column

     - ``basevid``: ID of the variable that the data in this column was
                     derived/generated from (and has the same data type as),
                     if not the original ``vid``.  For example, see the
                     ``take`` argument to
                     :func:`.processing_functions.binariseCategorical`.

     - ``fillval``:  Fill value to use for missing values, instead of the
                     global default (e.g. as specified by
                     ``--tsv_missing_values``).

    """
    def __init__(self,
                 datafile,
                 name,
                 index,
                 vid=None,
                 visit=0,
                 instance=0,
                 metadata=None,
                 basevid=None,
                 fillval=None,
                 origname=None):

        if basevid is None:
            basevid = vid

        if origname is None:
            origname = name

        self.datafile  = datafile
        self.name      = name
        self.origname  = origname
        self.index     = index
        self.vid       = vid
        self.visit     = visit
        self.instance  = instance
        self.metadata  = metadata
        self.basevid   = basevid
        self.fillval   = fillval


    def __str__(self):
        return 'Column({}, {} -> {}, {}, {}, {}, {}, {}, {})'.format(
            self.datafile,
            self.name,
            self.origname,
            self.index,
            self.vid,
            self.visit,
            self.instance,
            self.basevid,
            self.fillval)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return (isinstance(other, Column)       and
                self.datafile == other.datafile and
                self.name     == other.name     and
                self.origname == other.origname and
                self.index    == other.index    and
                self.vid      == other.vid      and
                self.visit    == other.visit    and
                self.instance == other.instance and
                self.basevid  == other.basevid  and
                self.fillval  == other.fillval)



class DataTable(util.Singleton):
    """The ``DataTable`` is a simple container class.

    It keeps references to the variable and processing tables, and the data
    itself. The :func:`importData` function creates and returns a
    ``DataTable``.

    A ``DataTable`` has the following attributes and helper methods:

    .. autosummary::
       :nosignatures:

       pool
       manager
       parallel
       vartable
       proctable
       cattable
       columns
       allColumns
       present
       visits
       instances
       variables


    Data should be accessed/modified via these methods:

    .. autosummary::
       :nosignatures:

       index
       __getitem__
       __setitem__


    Columns can be added/removed, and rows removed, via these methods:

    .. autosummary::
       :nosignatures:

       maskSubjects
       addColumns
       removeColumns

    Columns can be "flagged" with metadata labels via the :meth:`addFlag`
    method. All of the flags on a column can be retrieved via the
    :meth:`getFlags` method.


    The :meth:`subtable` method can be used to generate a replica
    ``DataTable`` with a specific subset of columns. It is intended for
    parallelisation, so that child processes are given a view of only the
    columns that are relevant to them, and as little copying between processes
    as possible takes place. The :meth:`subtable` and :meth:`merge` methods
    are intended to be used like so:

      1. Create subtables which only contain data for specific columns::

             cols      = ['1-0.0', '2-0.0', '3-0.0']
             subtables = [dtable.subtable([c]) for c in cols]

      2. Use multiprocessing to perform parallel processing on each column::

             def mytask(dtable, col):
                 dtable[:, col] += 5
                 return dtable

             with dtable.pool() as pool:
                 subtables = pool.starmap(mytask, zip(subtables, cols))

      3. Merge the results back into the main table::

             dtable.merge(subtables)

    Modifications must occur through the :meth:`DataTable.__setitem__`
    interface, so it can keep track of which columns have been modified.
    Addition or removal of columns or rows on subtables is not supported.
    """


    def __init__(self,
                 data,
                 columns,
                 vartable,
                 proctable,
                 cattable,
                 njobs=1,
                 mgr=None,
                 subtable=False):
        """Create a ``DataTable``.

        :arg data:      ``pandas.DataFrame`` containing the data.
        :arg columns:   List of :class:`.Column` objects, representing the
                        columns that are in the data.
        :arg vartable:  ``pandas.DataFrame`` containing the variable table.
        :arg proctable: ``pandas.DataFrame`` containing the processing table.
        :arg cattable   ``pandas.DataFrame`` containing the category table.
        :arg njobs:     Number of jobs to use for parallelising tasks.
        :arg mgr:       :class:`multiprocessing.Manager` object for
                        parallelisation
        :arg subtable:  For internal use. Used to differentiate between the
                        main ``DataTable``, and child ``DataTable`` objects
                        created via :meth:`subtable`.
        """

        self.__data      = data
        self.__vartable  = vartable
        self.__proctable = proctable
        self.__cattable  = cattable
        self.__njobs     = njobs
        self.__mgr       = mgr
        self.__subtable  = subtable
        self.__flags     = collections.defaultdict(set)

        # The varmap is a dictionary of
        # { vid : [Column] } mappings,
        # and the colmap is a dictionary
        # of { name : Column } mappings
        self.__varmap = collections.OrderedDict()
        self.__colmap = collections.OrderedDict()

        for col in columns:
            self.__colmap[col.name] = col
            if col.vid in self.__varmap: self.__varmap[col.vid].append(col)
            else:                        self.__varmap[col.vid] = [col]


    def __getstate__(self):
        """Returns the state of this :class:`.DataTable` for pickling. """
        return (self.__data,
                self.__vartable,
                self.__proctable,
                self.__cattable,
                self.__varmap,
                self.__colmap,
                self.__subtable,
                self.__flags)


    def __setstate__(self, state):
        """Set the state of this :class:`.DataTable` for unpickling. """

        self.__data      = state[0]
        self.__vartable  = state[1]
        self.__proctable = state[2]
        self.__cattable  = state[3]
        self.__varmap    = state[4]
        self.__colmap    = state[5]
        self.__subtable  = state[6]
        self.__flags     = state[7]
        self.__njobs     = 1
        self.__mgr       = None


    @contextlib.contextmanager
    def pool(self):
        """Return a ``multiprocessing.Pool`` object for performing tasks in
        parallel on the data. If the ``njobs`` argument passed to
        :meth:`__init__` was ``1``, or if this is a ``DataTable`` instance that
        has been unpickled (i.e. instances which are running in a sub-process),
        a ``multiprocessing.dummy.Pool`` instance is created and returned.
        """
        if self.__njobs == 1: Pool = mpd.Pool
        else:                 Pool = mp.Pool

        with Pool(self.__njobs) as pool:
            yield pool
            pool.close()
            pool.join()


    @property
    def isSubtable(self):
        """Returns ``True`` if this ``DataTable`` was created by a
        :meth:`subtable` call.
        """
        return self.__subtable


    @property
    def manager(self):
        """Returns a ``multiprocessing.Manager`` for sharing data between
        processes.
        """
        if self.__mgr is None: return mpd.Manager()
        else:                  return self.__mgr


    @property
    def njobs(self):
        """Returns the number of jobs that will be used by the :attr:`pool`
        for parallelising tasks.
        """
        return self.__njobs


    @property
    def parallel(self):
        """Returns ``True`` if this invocation of ``funpack`` has the ability
        to run tasks in parallel, ``False`` otherwise.
        """
        return self.__njobs > 1


    @property
    def vartable(self):
        """Returns the ``pandas.DataFrame`` containing the variable table. """
        return self.__vartable


    @property
    def proctable(self):
        """Returns the ``pandas.DataFrame`` containing the processing table.
        """
        return self.__proctable


    @property
    def cattable(self):
        """Returns the ``pandas.DataFrame`` containing the category table. """
        return self.__cattable


    @property
    def index(self):
        """Returns the subject indices."""
        return self.__data.index


    @property
    def shape(self):
        """Returns the (nrows, ncolumns) shape of the data."""
        return self.__data.shape


    @property
    def variables(self):
        """Returns a list of all integer variable IDs present in the data.

        The list includes the index variable (which has an id of ``0``).
        """
        return list(self.__varmap.keys())


    @property
    def allColumns(self):
        """Returns a list of all columns present in the data, including
        index columns.
        """
        return list(it.chain(*[self.columns(v) for v in self.variables]))


    @property
    def indexColumns(self):
        """Returns a list of all index columns present in the data. """
        return list(self.columns(0))


    @property
    def dataColumns(self):
        """Returns a list of all non-index columns present in the data. """
        return [c for c in self.allColumns if c.vid != 0]


    def present(self, variable, visit=None, instance=None):
        """Returns ``True`` if the specified variable (and optionally visit/
        instance) is present in the data, ``False`` otherwise.
        """
        try:
            self.columns(variable, visit, instance)
            return True
        except KeyError:
            return False


    def columns(self, variable, visit=None, instance=None):
        """Return the data columns corresponding to the specified ``variable``,
        ``visit`` and ``instance``.

        :arg variable: Integer variable ID
        :arg visit:    Visit number. If ``None``, column names for all visits
                       are returned.
        :arg instance: Instance number. If ``None``, column names for all
                       instances are returned.
        :returns:      A list of :class:`.Column` objects.
        """

        cols = list(self.__varmap[variable])

        if visit is not None:
            cols = [c for c in cols if c.visit == visit]

        if instance is not None:
            cols = [c for c in cols if c.instance == instance]

        return cols


    def visits(self, variable):
        """Returns the visit IDs for the given ``variable``. """
        cols = self.columns(variable)
        return list({c.visit for c in cols})


    def instances(self, variable):
        """Returns the instance IDs for the given ``variable``. """
        cols = self.columns(variable)
        return list({c.instance for c in cols})


    def maskSubjects(self, mask):
        """Remove subjects where ``mask is False``. """
        self.__data = self.__data[mask]


    def removeColumns(self, cols):
        """Remove the columns described by ``cols``.

        :arg cols: Sequence of :class:`Column` objects to remove.
        """

        names = [c.name for c in cols]

        self.__data.drop(names, axis=1, inplace=True)

        for col in cols:

            vcols = self.__varmap[col.vid]
            vcols.remove(col)

            self.__colmap.pop(col.name)

            if len(vcols) > 0: self.__varmap[col.vid] = vcols
            else:              self.__varmap.pop(col.vid)


    def addColumns(self, series, vids=None, kwargs=None):
        """Adds one or more new columns to the data set.

        .. note:: It is assumed that each ``pandas.Series`` object shares
                  the same row indices as this ``DataTable``.

        :arg series: Sequence of ``pandas.Series`` objects containing the
                     new column data to add.

        :arg vids:   Sequence of variables each new column is associated
                     with. If ``None`` (the default), variable IDs are
                     automatically assigned.

        :arg kwargs: Sequence of dicts, one for each series, containing
                     arguments to pass to the :class:`Column` constructor
                     (e.g. ``visit``, ``metadata``, etc).
        """

        import funpack.loadtables as loadtables  # noqa: E501 pylint: disable=import-outside-toplevel

        if vids   is None: vids   = [None] * len(series)
        if kwargs is None: kwargs = [None] * len(series)

        for s in series:
            if s.name in self.__data.columns:
                raise ValueError(
                    'A column with name {} already exists - remove '
                    'it, or assign to it directly'.format(s.name))

        if len(vids) != len(series):
            raise ValueError('length of vids does not match series')
        if len(kwargs) != len(series):
            raise ValueError('length of kwargs does not match series')

        startidx = len(self.__data.columns)
        idxs     = range(startidx, startidx + len(series))

        # if vids are not provided, auto-generate
        # a vid for each column starting from here.
        startvid = max(max(self.variables) + 1, AUTO_VARIABLE_ID)

        # It's much faster to concatenate two
        # DataFrames together than to seuentially
        # concatenate each series to our existing
        # dataframe. We've already checked for
        # column conflicts, and we assume that
        # row indices are aligned.
        log.debug('Merging %u new columns into main data table.', len(series))

        series      = pd.concat(series, axis=1, verify_integrity=False)
        self.__data = pd.concat((self.__data, series),
                                axis=1,
                                copy=False,
                                verify_integrity=False)

        # create a new Column object
        # describing each new column
        for name, idx, vid, kw in zip(series, idxs, vids, kwargs):

            if vid is None:
                vid      = startvid
                startvid = startvid + 1

            if kw is None:
                kw = {}

            col = Column(None, name, idx, vid, **kw)
            self.__colmap[name] = col

            # new column on existing variable.
            # We assume the data type is the
            # same as the existing columns for
            # this variable
            if vid in self.__varmap:
                self.__varmap[vid].append(col)

            # new variable - the addNewVariable
            # function will sort things out
            else:
                dtype = self.__data[name].dtype
                self.__varmap[vid] = [col]
                loadtables.addNewVariable(
                    self.__vartable, vid, name, dtype)


    def getFlags(self, col):
        """Return any flags associated with the specified column.

        :arg col: :class:`Column` object
        :returns: A ``set`` containing any flags associated with ``col``
        """
        return set(self.__flags[col])


    def addFlag(self, col, flag):
        """Adds a flag for the specified column.

        :arg col:  :class:`Column` object
        :arg flag: Flag to add
        """
        self.__flags[col].add(flag)


    def __getitem__(self, slc):
        """Get the specified slice from the data. This method has
        the same interface as the ``pandas.DataFrame.loc`` accessor.
        """
        return self.__data.loc[slc]


    def __setitem__(self, slc, value):
        """Set the specified slice in the data.

        This method suports a limited form of the ``pandas.DataFrame.loc``
        interface. Slices/labels for both rows and columns must be specified,
        and columns may only be specified via a slice, list, tuple, or
        individual label.
        """
        if not isinstance(slc, tuple) or len(slc) != 2:
            raise RuntimeError('DataTable.__setitem__ requires both '
                               'rows and columns to be indexed.')

        self.__data.loc[slc] = value

        # Flag the column as modified. This is
        # detected by the merge method when
        # it merges subtables back in.
        if self.isSubtable:
            cols = slc[1]
            if isinstance(cols, slice):
                cols = self.__data.columns[cols]
            elif not isinstance(cols, (list, tuple)):
                cols = [cols]

            for col in cols:
                self.addFlag(self.__colmap[col], MODIFIED_COLUMN)


    def __len__(self):
        """Returns the number of rows in the data set. """
        return len(self.__data)


    def subtable(self, columns=None, rows=None):
        """Return a new ``DataTable`` which only contains the data for
        the specified ``columns`` and/or ``rows``.

        This method can be used to create a replica ``DataTable`` where the
        underlying ``pandas.DataFrame`` only contains the specified
        columns. It is intended to be used when parallelising tasks, so that
        child processes are given a view of only the relevant columns.

        .. note:: The :meth:`merge` method cannot be used to merge in a
                  subtable that contains a subset of rows.

        :arg columns: List of :class:`Column` objects.
        :arg rows:    Sequence of row indices.
        :returns:     A new :class:`DataTable`.
        """

        if columns is None:
            columns  = self.dataColumns
            colnames = slice(None)
        else:
            colnames = [c.name for c in columns]

        columns = [self.allColumns[0]] + columns

        if rows is None:
            rows = slice(None)

        return DataTable(self.__data.loc[rows, colnames],
                         columns,
                         self.__vartable,
                         self.__proctable,
                         self.__cattable,
                         self.__njobs,
                         subtable=True)


    def merge(self, subtables):
        """Merge the data from the given ``subtables`` into this ``DataTable``.

        It is assumed that the ``subtables`` each contain a sub-set of the
        columns in this ``DataTable``.

        .. note:: The :meth:`merge` method cannot be used to merge in a
                  subtable that contains a subset of rows.

        :arg subtables: A single ``DataTable``, or a sequence of ``DataTable``
                        instances, returned by :meth:`subtable`.
        """

        if not isinstance(subtables, abc.Sequence):
            subtables = [subtables]

        # Gather a list of all subtable dataframes,
        # and a list of all columns to be copied.
        # We only copy modified columns - we assume
        # that all changes to the subtable occurred
        # via DataTable.__setitem__
        subdfs  = []
        subcols = []

        for subtable in subtables:
            subtcols = [c.name for c in subtable.dataColumns
                        if MODIFIED_COLUMN in subtable.getFlags(c)]
            subdfs.append(subtable[:, subtcols])
            subcols.extend(subtcols)

        # if there are columns to merge from
        # any subtable, create a single dataframe
        # containing all of them - quicker than
        # merging them separately
        if len(subcols) > 0:

            log.debug('merging %u subtable dataframes (%u columns)',
                      len(subdfs), len(subcols))

            if len(subdfs) > 1:
                subdf = pd.concat(subdfs,
                                  axis='columns',
                                  verify_integrity=False,
                                  copy=False)
            else:
                subdf = subdfs[0]

            # merge subtable data into the
            # main dataframe, preserving
            # column ordering
            colorder    = self.__data.columns
            self.__data = pd.concat((self.__data.drop(columns=subcols),
                                     subdf.loc[:, subcols]),
                                    axis='columns',
                                    verify_integrity=False,
                                    copy=False)
            self.__data = self.__data[colorder]

        # copy column metadata
        # over from subtables
        for subtable in subtables:
            for subcol in subtable.dataColumns:

                mycol               = self.__colmap[subcol.name]
                myflags             = self.__flags[mycol]
                subflags            = subtable.getFlags(subcol)
                subflags            = subflags.difference((MODIFIED_COLUMN,))
                self.__flags[mycol] = myflags.union(subflags)

                if subcol.metadata is not None:
                    mycol.metadata = subcol.metadata
