#!/usr/bin/env python
#
# __init__.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import itertools     as it
import functools     as ft
import os.path       as op
import unittest.mock as mock
import                  os
import                  shutil
import                  logging
import                  tempfile
import                  contextlib
import                  collections

import datetime

import numpy as np
import pandas as pd

import funpack.util       as util
import funpack.custom     as custom
import funpack.fileinfo   as fileinfo
import funpack.loadtables as loadtables
import funpack.datatable  as datatable


def patch_logging(func):

    log                   = mock.MagicMock()
    log.getEffectiveLevel = lambda : logging.INFO

    def wrapper(*a, **kwa):
        targets = [
            'funpack.cleaning.log',
            'funpack.cleaning_functions.log',
            'funpack.config.log',
            'funpack.custom.log',
            'funpack.datatable.log',
            'funpack.exporting.log',
            'funpack.exporting_hdf5.log',
            'funpack.exporting_tsv.log',
            'funpack.expression.log',
            'funpack.fileinfo.log',
            'funpack.importing.core.log',
            'funpack.importing.filter.log',
            'funpack.importing.reindex.log',
            'funpack.loadtables.log',
            'funpack.main.log',
            'funpack.merging.log',
            'funpack.processing.log',
            'funpack.processing_functions.log',
            'funpack.processing_functions_core.log',
            'funpack.util.log',
            'logging.getLogger',
        ]
        patches = [mock.patch(t, log) for t in targets]
        [p.start() for p in patches]
        try:
            return func(*a, **kwa)
        finally:
            [p.stop() for p in patches]
    return ft.update_wrapper(wrapper, func)


@contextlib.contextmanager
def patch_base_tables():
    with mock.patch('funpack.loadtables.loadTableBases',
                    return_value=(None, None)):
        yield


def clear_plugins(func):
    def wrapper(*a, **kwa):
        result = func(*a, **kwa)
        custom.clearRegistry()
        return result

    return ft.update_wrapper(wrapper, func)


@contextlib.contextmanager
def tempdir(root=None, changeto=True):

    testdir = tempfile.mkdtemp(dir=root)
    prevdir = os.getcwd()
    try:

        if changeto:
            os.chdir(testdir)
        yield testdir

    finally:
        if changeto:
            os.chdir(prevdir)
        shutil.rmtree(testdir)


def gen_test_data(num_vars,
                  num_subjs,
                  out_file,
                  max_visits=1,
                  max_instances=1,
                  start_var=1,
                  start_subj=1,
                  sep='\t',
                  ctypes=None,
                  missprop=0,
                  names=None,
                  min_visits=1):

    if ctypes is None:
        ctypes = {}


    varids = []
    cols   = []

    for varid in range(start_var, num_vars + start_var):

        nvisits    = np.random.randint(min_visits, max_visits    + 1)
        ninstances = np.random.randint(1,          max_instances + 1)

        for visit, instance in it.product(range(nvisits), range(ninstances)):
            cols.append(util.generateColumnName(varid, visit, instance))
            varids.append(varid)

    # subject IDs
    data = pd.DataFrame(index=range(start_subj, num_subjs + start_subj))
    data.index.name = 'eid'

    for varid, col in zip(varids, cols):
        ctype = ctypes.get(varid, 'float')

        if ctype == 'int':
            coldata = np.random.randint(1, 100, num_subjs)
        elif ctype == 'float':
            coldata = np.random.randint(1, 100, num_subjs)
        elif ctype == 'date':
            ys = np.random.randint(2000, 2019, num_subjs)
            ms = np.random.randint(1,    13,   num_subjs)
            ds = np.random.randint(1,    28,   num_subjs)
            coldata = [datetime.date(y, m, d) for y, m, d in zip(ys, ms, ds)]
        elif ctype == 'time':
            hs = np.random.randint(0,    23, num_subjs)
            ms = np.random.randint(0,    59, num_subjs)
            ss = np.random.randint(0,    59, num_subjs)
            coldata = [datetime.time(h, m, s) for h, m, s in zip(hs, ms, ss)]
        elif ctype == 'datetime':
            ys  = np.random.randint(2000, 2019, num_subjs)
            mos = np.random.randint(1,    13,   num_subjs)
            ds  = np.random.randint(1,    28,   num_subjs)
            hs  = np.random.randint(0,    23,   num_subjs)
            mis = np.random.randint(0,    59,   num_subjs)
            ss  = np.random.randint(0,    59,   num_subjs)
            coldata = [datetime.datetime(y, mo, d, h, mi, s)
                       for y, mo, d, h, mi, s in zip(ys, mos, ds, hs, mis, ss)]

        data[col] = coldata

        if missprop > 0:
            missing = np.random.choice(data.index,
                                       int(round(missprop * num_subjs)))
            data.loc[missing, col] = np.nan

    if names is None:
        names = True
    data.to_csv(out_file, sep, header=names)


table_headers  = {

    'variables'   : 'ID\tType\tInternalType\tDescription\tDataCoding\tInstancing\tNAValues\tRawLevels\tNewLevels\tParentValues\tChildValues\tClean',  # noqa
    'datacodings' : 'ID\tNAValues\tRawLevels\tNewLevels',
    'categories'  : 'ID\tCategory\tVariables',
    'types'       : 'Type\tClean',
    'processing'  : 'Variable\tProcess'
}

table_templates = {
    'variables'   : '{variable}\t{type}\t\t\t\t2\t\t\t\t\t\t',
    'datacodings' : '',
    'categories'  : '',
    'types'       : '',
    'processing'  : '',
}

def gen_tables(variables, vtypes=None, datafiles=None):

    if vtypes is None:
        vtypes = {}

    if datafiles is not None:
        datafiles = [op.abspath(f) for f in datafiles]

    with tempdir():

        if datafiles is None:
            with open('datafile.txt', 'wt') as f:
                colnames = ['eid'] + ['{}-0.0'.format(v) for v in variables]
                f.write('\t'.join(colnames))
            datafiles = ['datafile.txt']

        for table in ['variables',
                      'datacodings',
                      'categories',
                      'types',
                      'processing']:

            fname = '{}.tsv'.format(table)
            hdr   = table_headers[  table]
            tmpl  = table_templates[table]

            with open(fname, 'wt') as f:
                f.write(hdr + '\n')

                if table == 'variables':
                    for v in variables:

                        vtype = str(vtypes.get(v, 'continuous'))

                        f.write(tmpl.format(variable=v, type=vtype) + '\n')

        vt, pt, ct, uk, up = loadtables.loadTables(
            fileinfo.FileInfo(datafiles),
            ['variables.tsv'],
            ['datacodings.tsv'],
            'types.tsv',
            'processing.tsv',
            'categories.tsv',
            noBuiltins=True)
        return vt, pt, ct, uk


# vvis == [(vid, visit, instance), ...]
def gen_columns(vvis):
    cols = []
    for i, vvi in enumerate(vvis):
        if isinstance(vvi, str):
            cols.append(datatable.Column(None, vvi, i, 0))
            continue
        vid, visit, instance = vvi
        if visit is None:
            name = '{}.{}'.format(vid, instance)
            visit = 0
        else:
            name = '{}-{}.{}'.format(vid, visit, instance)
        cols.append(datatable.Column(None, name, i, vid, visit, instance))
    return cols


def gen_DataTable(cols, *a, **kwa):

    nsubjs    = len(cols[0])
    variables = range(0, len(cols) + 1)
    colnames  = ['eid'] + ['{}-0.0'.format(v) for v in variables[1:]]

    columns = collections.OrderedDict(zip(colnames[1:], cols))

    data = pd.DataFrame(columns)
    data['eid'] = np.arange(1, nsubjs + 1)
    data.set_index('eid', inplace=True)

    return gen_DataTableFromDataFrame(data, *a, **kwa)


def gen_DataTableFromDataFrame(df, tables=None, njobs=1, variables=None):

    if variables is None:
        variables = list(range(1, len(df.columns) + 1))

    colobjs   = [datatable.Column(None, df.index.name, 0, 0, 0, 0)] + \
                [datatable.Column(None, n, v, v, 0, 0)
                 for v, n in zip(variables, df.columns)]

    if tables is None:
        variables = list(set(variables))
        vartable, proctable, cattable, uvs = gen_tables(variables)
    else:
        vartable, proctable, cattable = tables

    return datatable.DataTable(df, colobjs, vartable, proctable, cattable,
                               njobs=njobs)
