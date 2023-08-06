#!/usr/bin/env python
#
# __init__.py - the importing package
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""The ``importing`` package implements the data import stage - identifying
which columns are to be loaded, loading data from the input files, and
filtering/re-arranging the resulting data frame.

The :func:`.core.importData` function is the entry point to the import stage.
"""


from .core import   (importData,
                     NUM_ROWS,
                     MERGE_AXIS,
                     MERGE_STRATEGY,
                     MERGE_AXIS_OPTIONS,
                     MERGE_STRATEGY_OPTIONS)              # noqa
from .filter import (restrictVariables,
                     REMOVE_DUPLICATE_COLUMN_IDENTIFIER)  # noqa
