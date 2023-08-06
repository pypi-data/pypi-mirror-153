FUNPACK release history
=======================



3.2.3 (Wednesday 1st June 2022)
-------------------------------


Changed
^^^^^^^


* New additions to ``fmrib`` categories.


3.2.2 (Tuesday 31st May 2022)
-----------------------------


Changed
^^^^^^^


* Updated internal datafield/encoding schemas to the latest available
  on the UK BioBank showcase.


3.2.1 (Tuesday 31st May 2022)
-----------------------------


Changed
^^^^^^^


* Adjustment to the categories that are loaded in the ``fmrib`` profile.


3.2.0 (Friday 13th May 2022)
----------------------------


Added
^^^^^

* New ``--exclude_variable`` and ``--exclude_category`` options, allowing
  variables / categories to be explicitly excluded from being imported.


Changed
^^^^^^^


* The :func:`.removeIfRedundant` processing function now uses ``double``
  precision by default.


3.1.1 (Tuesday 10th May 2022)
-----------------------------


Changed
^^^^^^^


* Updated categorisations in the ``fmrib`` configuration profile.


3.1.0 (Thursday 5th May 2022)
-----------------------------


Added
^^^^^


* New ``numeric`` and ``convertNumeric`` options to the
  :func:`.flattenHierarchical` cleaning function, which allow it to be used
  with unique numeric labels (node IDs) for hierarchical data encodings,
  rather than coding labels (which are not necessarily numeric, or unique)
  (!88).


Changed
^^^^^^^


* Updated internal data field and data coding to the latest from the UK
  BioBank showcase.


Fixed
^^^^^


* Fixed an issue with the interpretation of hierarchical data codings, which
  was causing the ``flattenHierarchical`` cleaning function to crash (!88).


3.0.0 (Wednesday 5th January 2022)
----------------------------------


Changed
^^^^^^^


* The ``funpack`` command has been renamed to ``fmrib_unpack``, to avoid
  naming conflicts with other packages.


2.9.1 (Wednesday 29th December 2021)
------------------------------------


Fixed
^^^^^


* Fixed some compatibility issues with Python 3.10.



2.9.0 (Tuesady 28th December 2021)
----------------------------------


Added
^^^^^


* New ``--remove_duplicates`` option, which causes columns with duplicate
  names to be removed, with only the first retained.


Changed
^^^^^^^


* Explicitly use the ``fork`` method for the ``multiprocessing`` module.


2.8.0 (Thursday 19th August 2021)
---------------------------------


Added
^^^^^


* New ``skipUnknowns`` option to the ``removeIfRedundant`` processing function,
  whereby if a column is found to be redundant with respect to a column of an
  unkknown or uncategorised data field, it is *not* dropped. This option is
  used in the ``fmrib`` configuration.


Changed
^^^^^^^


* Added a recoding rule for data coding `100348
  <https://biobank.ctsu.ox.ac.uk/crystal/coding.cgi?id=100348>`_ to the
  ``fmrib`` configuration.


2.7.1 (Tuesday 22nd June 2021)
------------------------------


Fixed
^^^^^


* Fixed some issues with the ``binariseCategorical`` and ``removeIfSparse``
  processing functions, which could cause them to cause a crash when
  processing empty columns.


2.7.0 (Friday 14th May 2021)
----------------------------


Changed
^^^^^^^


* The ``--na_values``, ``--child_values`` and ``--recoding`` options can now
  be applied to non-numeric data fields.
* Updated internal data field and data coding to the latest from the UK
  BioBank showcase.
* Updates to FMRIB categories and processing rules.


2.6.0 (Monday 29th March 2021)
------------------------------


Changed
^^^^^^^


* Documentation for FUNPACK can now be found online at
  https://open.win.ox.ac.uk/pages/fsl/funpack/.
* The way that "uncategorised" variables are identified has been changed.
  Previously, a variable which was not in a category *and* which had no
  cleaning/processing rules specified was classified as uncategorised. This
  has been simplified so that a variable which not in a category is classified
  as uncategorised. This has been done to avoid the possibility of missing
  newly added variables which use an existing data coding, and therefore may
  implicitly have cleaning rules specified for them.


2.5.2 (Monday 15th March 2021)
------------------------------


Changed
^^^^^^^


* A warning message is now emitted if a processing step is requested for a
  variable that is not present in the input data.


Fixed
^^^^^


* Fixed an issue with the ``binariseCatgegorical`` processing function where,
  when it was applied to multiple variables, each with a separate ``take``
  variable (as is the case in the ``fmrib`` configuration), would cause an
  error if any of the ``take`` variables were not present.


2.5.1 (Wednesday 3rd March 2021)
--------------------------------


Added
^^^^^


* New ``--escape_newlines`` option, which causes non-numeric values containing
  escape characters (e.g. ``\n``, ``\t``, etc) to be output literally.


Fixed
^^^^^


* Fixed a bug where subject inclusion expressions were causing zero rows to be
  imported if the variable was not present in the input file.
* Fixed some compatibility issues with Pandas 1.2.


2.5.0 (Wednesday 9th December 2020)
-----------------------------------


Added
^^^^^


* New ``--rename_duplicates`` option, which can be used to give duplicate
  columns unique names.


Changed
^^^^^^^


* Conditional expressions used with the ``--subject`` option can now be used
  on date/time variables.
* Internal re-organisation of the ``funpack.fileinfo`` module, and minor
  changes to function interfaces in the ``funpack.importing`` and
  ``funpack.loadtables`` modules.


2.4.0 (Thursday 26th November 2020)
___________________________________


Added
^^^^^


* New ``--ids_only`` option which causes only the subject IDs to be saved,
  suitable for use with the ``--subject`` option in subsequent calls to
  ``funpack``.


Changed
^^^^^^^

* Changed how binary subject selection expressions are evaluated when the
  different variables have different numbers of columns.
* All internal UKB showcase data tables have been updated to their
  latest versions.
* The node name for `Chapter V - Supplementary classification ...` in the ICD9
  data table has been changed from `Chapter V` to `Chapter V sup` to avoid
  collisions with the `Chapter V` node.


2.3.3 (Wednesday 5th October 2020)
----------------------------------


Changed
^^^^^^^


* Improved performance when appying the ``--column`` command-line argument.


2.3.2 (Wednesday 10th June 2020)
--------------------------------


Fixed
^^^^^


* Fixed an issue which was preventing FUNPACK from being used on Windows
  platforms (!65).


2.3.1 (Sunday 17th May 2020)
----------------------------


Changed
^^^^^^^


* The :func:`.removeIfSparse` processing function can now parallelise the
  check across columns, rather than relying on the :mod:`.processing` module
  to parallelise calls across variables (!64).


Fixed
^^^^^


* The improved :mod:`.fmrib` date/time normalisation routines were not
  converting ``NaTs`` (Not-a-Time) correctly (!62).
* Fixed a problem in the FMRIB configuration - diagnosis timestamps were not
  being injected into binarised ICD variables (!63).


2.3.0 (Tuesday 12th May 2020)
-----------------------------


Changed
^^^^^^^


* Modified the :func:`.processing_functions.binariseCategorical` function so
  that it parallelises tasks internally, instead of being called in parallel
  for different variables. This should give superior performance (!60).
* Revisited the :meth:`.DataTable.merge` to optimise performance in all
  scenarios (!60).
* Improved performance of the :mod:`.fmrib` date/time normalisation routines,
  and changed their usage so they are now applied as "cleaning" functions
  after data import, rather than just before export. This means that date/
  time columns can be subjected to the redundancy check (as they will have
  a numeric type), and will improve data export performance (!60, !61).


2.2.1 (Monday 4th May 2020)
---------------------------


Fixed
^^^^^


* Reverted some changes to :meth:`.DataTable.merge` which caused performance
  degradations.


2.2.0 (Friday 1st May 2020)
---------------------------


Changed
^^^^^^^


* Substantial performance improvements to the
  :func:`.cleaning_functions.codeToNumeric` cleaning function, and to
  :func:`.processing_functions.removeIfRedundant`,
  :func:`.processing_functions.binariseCategorical`, and other processing
  functions.
* The default implementation of
  :func:`.processing_functions.removeIfRedundant` now uses matrix algebra
  rather thsn pairwise comparisons. This requires more memory, but is much
  faster.
* Added `threadpoolctl <https://github.com/joblib/threadpoolctl/>`_ as a
  dependency, for setting the number of threads to use when parallelising
  ``numpy`` operations.


Fixed
^^^^^


* The :func:`.removeIfRedundant` processing function was not testing columns
  with no missing values when a NA correlation threshold was being used.
* :func:`.removeIfRedundant` was also potentially producing inconsistent
  results for columns with no present values, or with a constant value.


2.1.0 (Tuesday 21st April 2020)
-------------------------------


Added
^^^^^


* New ``--drop_na_rows`` option, which tells ``funpack`` to drop rows which do
  not contain a value for any column.


Changed
^^^^^^^


* Internal changes to improve performance.


2.0.0 (Tuesday 7th April 2020)
------------------------------


Changed
^^^^^^^


* The ``fmrib`` and ``fmrib_logs`` configuration profiles no longer define the
  variables/categories to be loaded - by default all variables in the input file
  will be loaded and processed.
* The ``--non_numeric_file`` option has been replaced with ``--suppress_non_numerics``
  (which tells FUNPACK to only save numeric columns to the main output file),
  and the ``--write_non_numerics`` and ``--non_numerics_file`` options, which
  tell FUNPACK to save non-numeric columns to an auxillary output file.
* The ``--tsv_var_format`` option has been renamed to ``--var_format``, and is
  applied to all export formats.
* The default output file format is now inferred from the output file suffix -
  one of ``tsv``, ``csv``, or ``h5``.
* The format of the ``--unknown_vars_file`` has changed - the ``processed``
  column has been removed (as with the removal of the ``--import_all`` option,
  it is now equivalent to the ``exported`` column), and uncategorised columns
  now have a ``class`` of ``uncategorised`` instead of ``unprocessed``.


Removed
^^^^^^^


* Removed several obscure, redundant, or deprecated options, including
  ``--import_all``, ``--remove_unknown``, ``--pass_through``,
  ``--output_id_column``, ``--column_pattern``, ``--column_name``,
  ``--low_memory``, and ``--work_dir``.
* Removed the unused :mod:`funpack.storage` module.
* Removed the unused :meth:`.DataTable.order` method.


1.9.1 (Sunday 29th March 2020)
------------------------------


Changed
^^^^^^^


* Updates to FMRIB categories.


1.9.0 (Friday 28th February 2020)
---------------------------------


Added
^^^^^


* New ``--write_log``, ``--write_unknown_vars``, ``--write_icd10_map``,
  ``--write_description``, and ``--write_summary`` options, which will save
  the respective auxillary output file using a default naming convention which
  is based on the name of the main output file. Exact names can still be
  specified via the ``--log_file``, ``--unknown_vars_file``,
  ``--icd10_map_file``, ``--description_file``, and ``--summary_file``
  options.


Changed
^^^^^^^


* Refactored the ``fmrib`` configuration profile. ``fmrib`` now just applies
  cleaning/processing rules. ``fmrib_logs`` applies ``fmrib``, and also
  specifies logging/auxillary output files.


Removed
^^^^^^^


* Removed the built-in ``ukb`` configuration.


Deprecated
^^^^^^^^^^


* The ``--pass_through`` option is deprecated - the same behaviour can be
  achieved by running FUNPACK without specifying any cleaning or processing
  steps.


1.8.2 (Monday 24th February 2020)
---------------------------------


Changed
^^^^^^^


* The ``--config_file`` option can be used more than once, and can also be
  used from within a configuration file (i.e. one configuration file may
  "include" another).
* Changed the way that the :func:`.processing_functions.removeIfRedundant`
  process splits up the data set for parallel processing.


1.8.1 (Wednesday 19th February 2020)
------------------------------------


Added
^^^^^


* New ``naval`` option to the :func:`.processing_functions.removeIfSparse`
  processing function.


Changed
^^^^^^^


* Changes to the ``fmrib`` configuration, to correctly apply sparsity check
  to variables 41202, 41203, 41270 and 41271.


1.8.0 (Tuesday 18th February 2020)
----------------------------------


Added
^^^^^


* New ``take`` option to the :func:`.processing_functions.binariseCategorical`
  processing function, which allows the generated columns to contain values
  from another column, instead of containing binary labels.
* New ``fillval`` option to the
  :func:`.processing_functions.binariseCategorical` processing function, which
  can be used in conjunction with ``take``, to specify the fill value for
  missing rows.
* Argument **broadcasting** for processing functions - when a process is
  applied independently to more than one variable, the input arguments to the
  process may need to be different for each variable. This can be accomplished
  by using a _broadcast_ argument - simply prefix the argument name with
  ``'broadcast_'``, and then specify a list containing the argument.
* Processing functions can now be passed lists of values.


Changed
^^^^^^^


* Changes to the ``fmrib`` configuration - variables
  `41202 <http://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=41202>`_,
  `41203 <http://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=41203>`_,
  `41270 <http://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=41270>`_, and
  `41271 <http://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=41271>`_ are
  binarised, and the binarised values replaced with diagnosis dates from
  the corresponding date variables.
* The processing function interface has been changed - processing functions
  which return metadata for newly added columns must now return a sequence of
  dicts containing arguments to the :class:`.Column` constructor, which can
  include metadata.


Fixed
^^^^^


* Fixed a bug whereby only the first two conditions were being parsed in
  an expression comprising multiple identical chained boolean operations
  (e.g. `v10 == 1 || v20 == 2 || v30 == 3`).


1.7.1 (Thursday 30th January 2020)
----------------------------------


Added
^^^^^


* New built-in ``ukb`` configuration, which applies NA insertion, categorical
  recoding, and child value replacement rules from the ``fmrib`` configuration.


Fixed
^^^^^

* Fixed a bug which arose from combining the ``--import_all`` and ``--column``
  options.


1.7.0 (Friday 24th January 2020)
--------------------------------


Added
^^^^^


* New ``--index_visits`` option, which re-arranges variables with separate
  columns per visit into single columns indexed by both subject ID and visit.


Changed
^^^^^^^


* The ``--index`` option now supports specification of multiple index columns
  for each input file.
* The :func:`.fileinfo.has_header` function has been modified to be more
  lenient.
* The :mod:`.importing` module has been internally refactored to improve
  code cleanliness.
* Various minor internal API changes.
* The :func:`.removeIfRedundant` processsing function will now drop columns
  which are redundant with respect to other columns which have already been
  dropped.
* Update to the FMRIB configuration (handling variable `6150
  <https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=6150>`_).
* The ``'codingdesc'`` metaproc function takes into account possible
  categorical recodings when retrieving the description for a particular
  value.


Fixed
^^^^^


* The :func:`.removeIfRedundant` processsing function was unnecessarily
  evaluating column pairs more than once, when run in parallel.


1.6.0 (Wednesday 11th December 2019)
------------------------------------


Added
^^^^^


* Non-numeric variables can now be used in conditional expressions, e.g.
  ``'v41202 == "A009"'``. Within such expressions, the value must be contained
  within single or double quotes.
* New ``contains`` operator, for use within conditional expressions to test
  presence of sub-strings.


Changed
^^^^^^^


* Parallelisation is now disabled by default, and must be explicitly enabled
  via the ``--num_jobs`` option. This is done in the ``fmrib`` configuration.
* Subject inclusion expressions are now evaluated during, rather than after,
  data import. They are now therefore performed in parallel on different
  chunks of the input file(s) (when parallelisaton is enabled).


1.5.0 (Monday 9th December 2019)
--------------------------------


Added
^^^^^


* New :func:`.util.wc` function to count the rows (lines) of a file;
  this is simply a wrapper around the UNIX ``wc`` tool.
* New :func:`.util.cat` function to concatenate multiple files together;
  this is simply a wrapper around the UNIX ``cat`` tool.
* New :func:`.util.inMainProcess` function so a process can determine whether
  it is the main process or a worker process.
* New :meth:`.DataTable.subtable` and :meth:`.DataTable.merge` methods, to aid
  in passing data to/from worker processes.
* Processing functions can now be specified to run independently on a subset
  of variables by using ``'independent'`` in the variable list.
* New ``any`` and ``all`` operations which can be used in conditional
  statements to control how the conditional results are combined across
  multiple columns for one variable. These can be used with the ``--subject``
  option.


Changed
^^^^^^^


* FUNPACK will now parallelise tasks by default; previously it would only
  parallelise tasks if ``--low_memory`` mode were selected.
* The data import stage is parallelised by using multiple processes to read
  different chunks of the input file(s), and then concatenating the resulting
  ``pandas.DataFrame`` objects afterwards.
* Cleaning functions are executed on each variable in parallel.
* Each processing step is executed in parallel where possible
  (e.g. ``independent`` processes), but processing steps are still executed
  sequentially.  New columns created by processing functions are saved to
  disk, and re-loaded by the main process, rather than being passed back to
  the main process via inter-process communication.
* The ``removeIfRedundant`` process now compares pairs of columns in parallel.
* The data export stage is parallelised by writing chunks of rows to different
  files, and then concatenating them into a single output file afterwards.
* The ``--variable``, ``--subject`` and ``--exclude`` options now accept
  comma-separated mixtures of IDs and MATLAB-style ranges.
* Updates to FMRIB categories.
* Updates to FMRIB processing rules, to take advantage of parallelism.
* The ,:mod:`icd10` module must now be initialised via the
  :func:`.icd10.initialise` function, when it is to be used in a multiprocessing
  context. This is not necessary when ``funpack`` is configured to not
  parallelise tasks (e.g. with ``--num_jobs 1``).


Deprecated
^^^^^^^^^^


* The ``--low_memory`` and ``--work_dir`` options have been deprecated, and no
  longer have any effect. The :mod:`.storage` module is no longer used, but is
  still present for possible future usage.


1.4.5 (Thursday 5th December 2019)
----------------------------------


Changed
^^^^^^^


* The ``funpack_demo`` notebook is now executed from a temporary directory, so
  it does not require write-permissions to the FUNPACK installation directory.


Fixed
^^^^^


* Fixed a bug where non-numeric variables (e.g.
  `41271 <https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=41271>`_ ) were
  being interpreted by ``pandas`` as being numeric.


1.4.4 (Friday 15th November 2019)
---------------------------------


Changed
^^^^^^^


* Updates to the FMRIB categories and configuration.


1.4.3 (Monday 11th November 2019)
---------------------------------


Changed
^^^^^^^


* Updated internal variable and data coding tables to the latest available from
  the UK Biobank showcase.
* Increased the file sample size used by :func:`.fileinfo.sniff`.


1.4.2 (Tuesday 6th August 2019)
-------------------------------


Changed
^^^^^^^


* Minor changes to the FMRIB configuration.


1.4.1 (Monday 8th July 2019)
----------------------------


Added
^^^^^


* New ``--trust_types`` command-line flag which tells FUNPACK to assume that
  the data in known-to-be-numeric columns is parseable (i.e. that there are no
  bad/unparseable values). This option improves import performance, but at the
  cost of causing FUNPACK to crash if the assumption is not true.


1.4.0 (Sunday 7th July 2019
---------------------------


Added
^^^^^


* Added a new ``InternalType`` column to the variable table, which can be used
  to specify the type to use internally for a given variable
  (e.g. ``float64``).  This is so that the default type of ``float32`` can be
  overridden for specific variables for which this is problematic, such as
  variable
  `20003 <https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=20003>`_.
  This column is initially populated from ``funpack/data/type.txt``.
* New :mod:`funpack.coding` module, for retrieving descriptive information
  about data codings. The information is stored in the
  ``funpack/data/coding/`` directory.  Hierarchical data codings are still
  accessed via the :mod:`.hierarchy` module.
* New :func:`hierarchicalDescriptionFromCode`,
  :func:`hierarchicalDescriptionFromNumeric`, and
  :func:`codingDescriptionFromValue` metaprocessing functions.



Changed
^^^^^^^

* The hierarchical coding name no longer needs to be specified when using the
  :func:`.cleaning_functions.codeToNumeric` cleaning function - the coding is
  automatically looked up.
* Variable 4288 has been moved from ``cognitive phenotypes`` to
  ``miscellaneous`` in the FMRIB categories.
* Variable 20003 is now binarised in the FMRIB categories.
* Changed the meta-processing function signature - these functions are now
  passed the :class:`.DataTable` and variable ID, in addition the value.


Fixed
^^^^^


* Now using an internal type of ``float64`` for variable 20003, as it
  potentially has values which cannot be represented in ``float32``.


Deprecated
^^^^^^^^^^


* Deprecated the `xDescriptionFromCode` and `xDescriptionFromNumeric`
  metaprocessing functions.


1.3.2 (Tuesday 4th June 2019)
-----------------------------


Changed
^^^^^^^


* Minor adjustments to the FMRIB categories.


1.3.1 (Thursday 30th May 2019)
------------------------------


Changed
^^^^^^^


* Updates to documentation.


1.3.0 (Wednesday 29th May 2019)
-------------------------------


Added
^^^^^


* New :func:`.cleaning_functions.codeToNumeric` cleaning function, for
  transforming hierarhical variable codes.
* New :func:`.hierarchy.codeToNumeric` and
  :func:`.hierarchy.numericToCode` functions.
* New meta-process functions for generating descriptions for ICD9, OPCS3 and
  OPCS4 hierarchical variables.
* Variable, data coding, processing, category and type files in the
  ``funpack/config`` directory can be specified on the command line and in
  configuration files as relative paths, and using a "dot" syntax, e.g.
  ``fmrib/categories.tsv``, or ``fmrib.categories``.


Changed
^^^^^^^


* Built-in cleaning and processing rules are no longer applied by default -
  they are now a part of the built-in ``fmrib`` configuration, and can be
  applied via ``-cfg fmrib``.
* Updates to built-in ``fmrib`` processing.
* The ``flattenHierarchical`` processing function accepts a ``name`` argument,
  allowing the hierarchical data type name to be specified.  If not provided,
  the type is inferred from the variable ID if possible.


Fixed
^^^^^


* Fixed a bug where a processing step attempted to add a new column with
  the same name as an existing one.


Deprecated
^^^^^^^^^^


* The :func:`.convertICD10Codes` cleaning function has been replaced by the
  new :func:`.cleaning_functions.codeToNumeric` function, which can be used
  with any hierarchical variable.
* The :func:`.icd10.codeToNumeric` and :func:`.icd10.numericToCode` functions
  have been replaced by the :func:`.hierarchy.codeToNumeric` and
  :func:`.hierarchy.numericToCode` functions.
* The :func:`.loadDefaultTables` function is obsolete and has been deprecated.



1.2.1 (Tuesday 28th May 2019)
-----------------------------


Changed
^^^^^^^


* Minor changes to built-in variable categories.


1.2.0 (Saturday 25th May 2019)
------------------------------


Added
^^^^^


* New ``--summary_file`` option, which exports a summary of the
  cleaning/processing steps that have been applied to each variable.


Changed
^^^^^^^


* Built-in recoding, NA insertion, and child value replacement rules have
  been revised and updated.


1.1.4 (Friday 17th May 2019)
----------------------------


Changed
^^^^^^^


* Changed default processing rules so a column with standard deviation less
  than ``1e-6`` is deemed sparse, and dropped.



1.1.3 (Thursday 16th May 2019)
------------------------------


Changed
^^^^^^^


* The :func:`.isSparse` function has been changed so that, when the ``mincat``
  or ``maxcat`` tests are specified as proportions, they are applied relative
  to the number of *non-missing* data points, rather than the total number of
  data points.


1.1.2 (Thursday 16th May 2019)
------------------------------


Fixed
^^^^^


* Fixed a bug in :func:`.flattenHierarchical` with respect to handling missing
  values.


1.1.1 (Wednesday 15th May 2019)
-------------------------------


Fixed
^^^^^


* Changed the :func:`.isSparse` function to avoid issues with non-numaric
  data.


1.1.0 (Tuesday 14th May 2019)
-----------------------------


Changed
^^^^^^^


* The ``--visit``/``-vi`` command line option will no longer be applied to
  variables which do not have an `instancing
  <https://biobank.ctsu.ox.ac.uk/crystal/schema.cgi?id=9>`_ code 2.
  This is implemented in the :func:`.keepVisits` function.
* The :func:`.remove` and :func:`.keepVisits` function signatures have changed
  - they now require the variable table to be passed in as the first argument.


1.0.2 (Tuesday 14th May 2019)
-----------------------------


Changed
^^^^^^^


* The :func:`.removeIfSparse` processing function accepts an ``ignoreType``
  parameter which forces all tests to be run, regardless of the variable type.


Fixed
^^^^^


* The :func:`.isSparse` function was skipping the ``mincat``/``maxcat`` tests
  for non-numeric categorical variables.


1.0.1 (Friday 9th May 2019)
---------------------------


Changed
^^^^^^^


* Python package name changed from ``fmrib_unpack`` to ``fmrib-unpack``.


1.0.0 (Friday 9th May 2019)
---------------------------


Changed
^^^^^^^


* ``ukbparse`` is now called ``FUNPACK`` - the *FMRIB UKBiobank Normalisation,
  Processing And Cleaning Kit*.


Removed
^^^^^^^


* The ``ukbparse_htmlparse``, ``ukbparse_join``, and
  ``ukbparse_compare_tables`` scripts have been removed.
* The ``ukbparse.icd10.readICD10CodingFile`` function and
  ``ukbparse.icd10.ICD10Hierarchy`` class have been removed (their
  functionality was replaced by the :mod:`.hierarchy` module)
* The :func:`.processing_functions.removeIfSparse` and
  :func:`.processing_functions_core.removeIfSparse` functions no longer accept
  an ``absolute`` argument.



0.21.1 (Thursday 8th May 2019)
------------------------------


Changed
^^^^^^^


* Addd categories 1, 2 and 99 to the ``fmrib`` configuration.



0.21.0 (Thursday 8th May 2019)
------------------------------


Added
^^^^^


* :class:`.Column` objects now have a ``metadata`` attribute which may be used
  in the column description (if the ``--description_file`` option is used).
  Processing functions can set the metadata for newly added columns.
* New ``metaproc`` plugin type to manipulate column metadata.
* All processing functions accept a ``metaproc`` argument, allowing a
  ``metaproc`` function to be applied to any column metadata that is returned
  by the processing function..


Changed
^^^^^^^


* The :func:`.processing_functions.binariseCategorical` function sets the
  categorical value as column metadata on the new binarised columns.


0.20.1 (Wednesday 8th May 2019)
-------------------------------


Fixed
^^^^^


* Fixed some typos in the ``README`` file.


0.20.0 (Tuesday 7th May 2019)
-----------------------------


Added
^^^^^


* The :func:`.isSparse` and :func:`.removeIfSparse` functions accept
  a new option, ``mincat``, which allows a categorical to be deemed sparse
  if the size of its smallest category is below a given threshold.
* New ``--description_file`` option which, for UK BioBank data, saves the
  description for each column to a text file.


Changed
^^^^^^^


* The ``absolute`` parameter to the :func:`.isSparse` and
  :func:`.removeIfSparse` functions is deprecated. Instead, they now accept
  ``abspres`` and ``abscat`` arguments, allowing the
  absoluteness/proportionality of the ``minpres`` and ``mincat``/``maxcat``
  options to be specified separately.
* Changed default processing rules so that ICD10 variables undergo a slightly
  different sparsity test.


Fixed
^^^^^


* Fixed a bug in the categorical recoding rules for Data Coding `100012
  <https://biobank.ctsu.ox.ac.uk/crystal/coding.cgi?id=100012>`_.



0.19.2 (Friday 26th April 2019)
-------------------------------


Changed
^^^^^^^


* Changes to built-in categories and to ``fmrib`` configuration.


0.19.1 (Thursday 25th April 2019)
---------------------------------


Changed
^^^^^^^


* Changed the default processing rules for ICD10 variables 40001, 40002,
  40006, 41202, and 41204.
* Added ICD10 variables 41201 and 41270 to the default cleaning/processing
  rules.


0.19.0 (Wednesday 24th April 2019)
----------------------------------


Added
^^^^^


* The ``--column`` option now accepts a file which contains a list of column
  names to import.


Changed
^^^^^^^


* The :func:`.icd10.codeToNumeric` and :func:`.icd10.numericToCode` functions
  have been changed to use the integer node IDs in the ICD10 hierarchy
  file. The previous approach could not handle parent categories, nor a small
  number of ICD10 codes which do not have a ``<letter><number>`` structure.
* The :func:`.fileinfo.has_header` function has been made more lenient for
  files with a small number of columns.


0.18.0 (Tuesday 23rd April 2019)
--------------------------------


Added
^^^^^


* New :func:`.icd10.numericToCode` function for converting from a numeric
  ICD10 code representation back to its alphanumeric representation.


Changed
^^^^^^^


* The default binarised ICD10 column name format has been changed from
  ``[variable_id][numeric_code]-[visit].0`` to
  ``[variable_id]-[visit].[numeric_code]``.
* The ``--non_numeric_file`` will not be created if there are not any
  non-numeric columns.
* The built-in ``fmrib`` configuration now includes verbosity and logging
  settings.
* The :func:`.isSparse` function now returns the reason and value for
  columns which fail the sparsity test.



0.17.0 (Monday 22nd April 2019)
-------------------------------


Added
^^^^^


* New ``--non_numeric_file`` option allows non-numeric columns to be saved to
  a separate file (TSV export only).
* Built-in ``fmrib.cfg`` configuration file, which can be used via
  ``-cfg fmrib``.


Changed
^^^^^^^


* The file generated by ``--unknown_vars_file`` now includes variables which
  are known, but are not in an existing category, and do not have any cleaning
  or processing rules specified for them.
* Built-in categories have been updated.


Fixed
^^^^^


* A bug in the column names generated for binarised ICD10 categorical codes
  has been fixed. This bug would potentially have resulted in collisions
  between column names for different ICD10 codes.


0.16.0 (Friday 22nd March 2019)
-------------------------------


Changed
^^^^^^^


* Full variable and datacoding table files no longer need to be provided -
  ``ukbparse`` uses ``ukbparse/data/field.txt`` and
  ``ukbparse/data/encoding.txt`` files, obtained from the UK Biobank showcase
  website, as the basis for recognising variables and data codings. The
  ``--variable_file``/``-vf`` and ``--datacoding_file``/``-df`` options now
  accept partial table definitions - these will be merged with the built-in
  rules (still stored in ``ukbparse/data/variables_*.tsv`` and
  ``ukbparse/data/datacodings_*.tsv``) when ``ukbparse`` is invoked.


Deprecated
^^^^^^^^^^


* The ``ukbparse_htmlparse``, ``ukbparse_join`` , and
  ``ukbparse_compare_tables`` commands.


Removed
^^^^^^^


* The ``--icd10_file`` command-line option has been removed.


0.15.1 (Thursday 21st March 2019)
---------------------------------


Fixed
^^^^^


* Fixed a bug which arose when using the ``--rename_column`` option.


0.15.0 (Monday 18th March 2019)
-------------------------------


Added
^^^^^


* New cleaning function, :func:`.flattenHierarchical`, for use with
  hierarchical variables (e.g. ICD10). The function can be used to replace
  leaf values with parent values.
* New :mod:`.hierarchy` module which contains helper functions and data
  structures for working with hierarchical variables.
* Definitions for all hierarchical UK Biobank variables are located in the
  ``ukbparse/data/hierarchy/`` directory.


Deprecated
^^^^^^^^^^


* The :func:`.readICD10ConfigFile` function has been replaced with the
  :func:`.loadHierarchyFile` function.
* The :class:`.ICD10Hierarchy` class has been replaced with the
  :class:`.Hierarchy` class .


0.14.8 (Monday 18th March 2019)
-------------------------------


Fixed
^^^^^


* Fixed an issue with the :func:`.processing_functions.binariseCategorical`
  processing function being applied to ICD10 codes.


0.14.7 (Sunday 17th March 2019)
-------------------------------


Changed
^^^^^^^


* Changes to default cleaning rules - negative values for integer/categorical
  types are no longer discarded.


0.14.6 (Saturday 16th March 2019)
---------------------------------


Fixed
^^^^^


* Fixed a ``KeyError`` which was occurring during the child-value replacement
  stage for input files which did not have column names of the form
  ``[variable]-[visit].[instance]``.
* Fixed some issues introduced by behavioural changes in the
  ``pandas.HDFStore`` class.


0.14.5 (Thursday 17th January 2019)
-----------------------------------


Fixed
^^^^^


* Implemented a workaround for a `bug <https://bugs.python.org/issue9334>`_ in
  the Python ``argparse`` module.


0.14.4 (Friday 11th January 2019)
---------------------------------


Changed
^^^^^^^


* Updated the default processing rules for variable
  [1120-1150](https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=1120).


0.14.3 (Tuesday 8th January 2019)
---------------------------------


Fixed
^^^^^


* Fixed a regression introduced in 0.14.2, where column loading restrictions
  (e.g. ``--variable``) were not being honoured


0.14.2 (Monday 7th January 2019)
--------------------------------


Fixed
^^^^^


* Fixed a regression introduced in 0.14.1, where using the ``--variable`` and
  ``--visit`` options together could cause a crash.


0.14.1 (Monday 7th January 2019)
--------------------------------


Fixed
^^^^^


* If the index columns for each input file have different names, the output
  index column was unnamed.  It is now given the name of the index column in
  the first input file.
* When the ``--column`` and ``--variable`` options were used together, only
  columns which passed both tests were being loaded. Now, columns which pass
  either test are loaded.


0.14.0 (Tuesday 25th December 2018)
-----------------------------------


Added
^^^^^


* New ``--column`` option, allowing columns to be selected by name/name
  pattern.
* ``ukbparse`` can now be installed from `conda-forge
  <https://anaconda.org/conda-forge/ukbparse>`_.


Changed
^^^^^^^


* The index column in the output file no longer defaults to being named
  ``'eid'``. It defaults to the name of the index in the input file, but
  can still be overridden by the ``--output_id_column`` option.


Fixed
^^^^^


* Blank lines are now allowed in configuration files (#2)
* Fix to derived column names for ICD10 variables in default processing rules.


0.13.1 (Thursday 20th December 2018)
------------------------------------


Added
^^^^^


* Unit test to make sure that ``ukbparse`` crashes if given bad input
  arguments.


0.13.0 (Thursday 20th Deember 2018)
-----------------------------------


Added
^^^^^


* New ``--index`` option, allowing the position of the index column in input
  files to be specified.
* The ``--variable``, ``--subject``, and ``--exclude`` options now accept
  comma-separated lists, in addition to IDs, ID ranges, and text files.


Fixed
^^^^^


* Memory usage estimates in log messages were wrong under Linux.


0.12.3 (Tuesday 18th December 2018
----------------------------------


Changed
^^^^^^^


* Changes to new :func:`.fileinfo.has_header` function to improve robustness.


0.12.2 (Monday 17th December 2018)
----------------------------------


Changed
^^^^^^^


* Now using a custom implementation of ``csv.Sniffer.has_header``, as the
  standard library version does not handle some scenarios.


0.12.1 (Saturday 15th December 2018)
------------------------------------


Added
^^^^^


* Added some instructions for generating your own variable and data coding
  tables to the README.


Changed
^^^^^^^


* The ``ukbparse_demo`` script ensures that the Jupyter ``bash_kernel`` is
  installed.
* The ``ukbparse_compare_tables``, ``ukbparse_htmlparse`` and
  ``ukbparse_join`` scripts print some help documentation when called without
  any arguments.
* Added ``lxml`` as a dependency (required by ``beautifulsoup4``).


0.12.0 (Tuesday 11th December 2018)
-----------------------------------


Added
^^^^^


* The ``join``, ``compare_tables``, and ``htmlparse`` scripts are now
  installed as entry points called ``ukbparse_join``,
  ``ukbparse_compare_tables``, and ``ukbparse_htmlparse``.
* Jupyter notebook, demonstrating most of the features in ``ukbparse``, at
  ``ukbparse/demo/ukbparse_demonstration.ipynb``. You can run the demo via the
  ``ukbparse_demo`` entry point.


Changed
^^^^^^^


* Moved the ``scripts/`` directory into the ``ukbparse/`` directory.
* Improved string representation of process functions.


Fixed
^^^^^


* Fix to configuration file parsing code - ``shlex.split`` is now used instead
  of ``str.split``.
* Fixed mixed data type issues when merging the data coding and type tables into
  the variable table.


0.11.3 (Monday 10th December 2018)
----------------------------------


Changed
^^^^^^^


* Made the ``vid``, ``visit``, and ``instance`` parameters to the
  :class:`.Column` class optional, to make life easier for custom sniffer
  functions.


0.11.2 (Monday 10th December 2018)
----------------------------------


Fixed
^^^^^


* Fixed a bug in the handling of new variable IDs returned by processing
  functions.



0.11.1 (Monday 10th December 2018)
----------------------------------


Fixed
^^^^^


* Fixed a bug in the :func:`.removeIfSparse` processing function.


0.11.0 (Monday 10th December 2018)
----------------------------------


Added
^^^^^


* New ``--no_builtins`` option, which causes the built-in variable, data
  coding, type, and category table files to be bypassed.
* New :meth:`.PluginRegistry.get` function for getting a reference to a plugin
  function.
* Cleaning/processing functions are listed in command-line help.


0.10.5 (Saturday 8th December 2018)
-----------------------------------


Changed
^^^^^^^


* The ``minpres`` option to the :func:`.removeIfSparse` processing function
  is ignored if it is specified as an absolute value, and the data set length
  is less than it.


0.10.4 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* Fixed an issue with the `--subject` command line option.


0.10.3 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* Made use of the standard library ``resource`` module conditional, as it is
  not present on Windows.


0.10.2 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* Removed relative imports from test modules.


0.10.1 (Friday 7th December 2018)
---------------------------------


Fixed
^^^^^


* The :mod:`ukbparse.plugins` package was missing an ``__init__.py``, and was
  not being included in PyPI packages.


0.10.0 (Thursday 6th December 2018)
-----------------------------------


Added
^^^^^


* New ``--na_values``, ``--recoding``, and ``--child_values`` command-line
  options for specifying/overriding NA insertion, categorical recodings,
  and child variable value replacement.
* ``--dry_run`` mode now prints information about columns that would not be
  loaded.


Fixed
^^^^^


* Fixed a bug in the :func:`.calculateExpressionEvaluationOrder` function.


0.9.0 (Thursday 6th December 2018)
----------------------------------


Added
^^^^^


* Infrastructure for automatic deployment to PyPI and Zenodo.


Changed
^^^^^^^


* Improved ``--dry_run`` output formatting.


0.8.0
-----


Added
^^^^^


* New ``--dry_run`` command-line option, which prints a summary of the cleaning
  and processing that would take place.


0.7.1
-----


Fixed
^^^^^


* Fixed a bug in the :func:`.icd10.saveCodes` function.


0.7.0
-----


Changed
^^^^^^^


* Small refactorings in :mod:`ukbparse.config` so that command line arguments
  can be logged easily.


0.6.3
-----


Changed
^^^^^^^


* Minor updates to avoid deprecation warnings.


0.6.2
-----


Fixed
^^^^^


* Fixed a bug with the ``--import_all`` option, where an error would be thrown
  if a specifically requested variable was removed during processing.


0.6.1
-----


Changed
^^^^^^^


* Changed default processing for variables 41202/41204 so they are binarised
  *within* visit.


0.6.0
-----


Added
^^^^^


* New ``--import_all`` and ``--unknown_vars_file`` options for outputting
  information about previously unknown variables/columns.


Changed
^^^^^^^


* Changed processing function return value interface - see the
  :mod:`.processing_functions` module for details.


0.5.0
-----


Added
^^^^^


* Ability to export a mapping file containing the numeric values that ICD10
  codes have been converted into - see the ``--icd10_map_file`` argument.


Changed
^^^^^^^


* Changes to default processing - all ICD10 variables are binarised by default.
  Sparsity/redundancy tests happen at the end, so that columns generated by
  previous steps are tested.


Fixed
^^^^^


* :meth:`.HDFStoreCollection.loc` method returns a ``pandas.DataFrame`` when
  a list of columns are indexed, and a ``pandas.Series`` when a single column
  is indexed.


0.4.1
-----


Changed
^^^^^^^


* Updates to variable table for UKBiobank spirometry variables.


0.4.0
-----


Added
^^^^^


* New :func:`.parseSpirometryData` function for parsing spirometry data
  (i.e. `UKBiobank variable 3066
  <https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=3066>`_


Removed
^^^^^^^


* Removed the ``--disable_rename`` command line option, because having the
  columns renamed is really annoying.


0.3.3
-----


Changed
^^^^^^^


* Reverted the behaviour of :func:`.isSparse`.


0.3.2
-----


Changed
^^^^^^^


* Changed the behaviour of :func:`.isSparse` so that series which are *greater
  than* the ``minpres`` threshold pass, rather than *greater than or equal
  to*.


0.3.1
-----


Changed
^^^^^^^


* The :func:`.isSparse` function ignores the ``minpres`` argument if it
  is larger than the number of samples in the data set.


Fixed
^^^^^


* The :func:`.processing_functions.binariseCategorical` function now works on
  data with missing values.


0.3.0
-----


Added
^^^^^


* New :meth:`.DataTable.addColumns` method, so processing functions can
  now add new columns.
* New :func:`.processing_functions.binariseCategorical` processing function,
  which expands a categorical column into multiple binary columns, one for
  each unique value in the data.
* New :func:`.processing_functions.expandCompound` processing function, which
  expands a compound column into columns, one for each value in the compound
  data.
* Keyword arguments can now be used when specifying processing.


Fixed
^^^^^


* Fixed handling of non-numeric categorical variables


0.2.0
-----


Added
^^^^^

* Added a changelog file


Changed
^^^^^^^


* Updated variable/datacoding files to bring them in line with the latest
  Biobank data release.
