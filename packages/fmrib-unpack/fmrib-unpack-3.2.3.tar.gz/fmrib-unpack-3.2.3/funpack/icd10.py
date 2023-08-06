#!/usr/bin/env python
#
# icd10.py - Query the ICD10 disease coding hierarchy.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains functions for working with the `ICD10
<https://en.wikipedia.org/wiki/ICD-10>`_ disease coding hierarcy.


The :func:`codeToNumeric` function will take an ICD10 coding, and return
a numeric variant of it.


The :func:`storeCodes` function allows sets of ICD10 codes to be stored
so that they can be saved out to a file via the :func:`saveCodes` function, at
a later stage.
"""


import              logging
import itertools as it
import functools as ft

import numpy     as np
import pandas    as pd

from . import util
from . import hierarchy


log = logging.getLogger(__name__)


def initialise(mgr=None):
    """Initialise the module-level storage used by the :func:`storeCodes`
    function.

    This function must be called if this module is to be used in a
    multiprocessing context. Furthermore, it must be called *before* the
    ``multiprocessing.Pool`` is created, so that the shared storage is
    initialised before the worker processes have been created. This is
    so that the shared storage will be available in the worker process'
    address space.

    This function does not need to be called in a single-process context.

    :arg mgr: ``multiprocessing.Manager`` used to create the shared storage.
              If ``None``, the created store will only work within-process.
    """

    if mgr is None: storeCodes.store = []
    else:           storeCodes.store = mgr.list()


def storeCodes(codes):
    """Stores the given sequence of ICD10 codes, so they can be exported to
    file at a later stage.

    The codes are stored in a list called ``store``, an attribute of this
    function.

    :arg codes: Sequence of ICD10 codes to add to the mapping file
    """
    store = getattr(storeCodes, 'store', [])
    store.append(codes)
    storeCodes.store = store


def saveCodes(fname, hier, fields=None):
    """Saves any codes which have been stored via :func:`storeCodes` out to
    the specified file.

    :arg fname:     File to save the codes to.

    :arg hier:      :class:`.Hierarchy` object containing the ICD10
                    hierarchy information.

    :arg fields:    Sequence of fields to include in the ``mapfile``. Defaults
                    to ``['code', 'value', 'description', 'parent_descs]``. May
                    contain any of the following:

                      - ``'code'``
                      - ``'value'``
                      - ``'description'``
                      - ``'parent_codes'``
                      - ``'parent_descs'``
    """

    if fields is None:
        fields = ['code', 'value', 'description', 'parent_descs']

    valid = ['code', 'value', 'description', 'parent_codes', 'parent_descs']
    if not all([f in valid for f in fields]):
        raise ValueError('Invalid field in: {}'.format(fields))

    store = getattr(storeCodes, 'store', [])
    store = pd.Series(list(it.chain(*store)), dtype=str)
    store = store[store.notna()]
    codes = np.sort(store.unique())

    def parent_codes(c):
        return ','.join(reversed(hier.parents(c)))

    def parent_descs(c):
        parents = reversed(hier.parents(c))
        descs   = [hier.description(p) for p in parents]
        return ' '.join(['[{}]'.format(d) for d in descs])

    df = pd.DataFrame({'code' : codes})

    for f in fields:
        if   f == 'code':         continue
        elif f == 'value':        func = ft.partial(hierarchy.codeToNumeric,
                                                    name='icd10')
        elif f == 'description':  func = hier.description
        elif f == 'parent_codes': func = parent_codes
        elif f == 'parent_descs': func = parent_descs

        df[f] = df['code'].apply(func)

    log.debug('Saving %u ICD10 codes to %s', len(df), fname)

    df = df[fields]
    df.to_csv(fname, sep='\t', index=False)
