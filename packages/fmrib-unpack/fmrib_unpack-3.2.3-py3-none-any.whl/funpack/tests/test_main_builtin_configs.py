#!/usr/bin/env python
#
# test_main_builtin_configs.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import numpy  as np
import pandas as pd

import funpack.main as main

from . import tempdir, patch_logging


@patch_logging
def test_main_fmrib(cfg='fmrib_logs'):

    # Just checking one rule - categorical recoding
    # from datacodings_recoding.tsv for datacoding
    # 100334 / variable 1100: 1,2,3,4 -> 0,1,2,3

    eids = np.arange(1, 101)
    vals = np.random.randint(1, 5, 100)
    data = pd.DataFrame({'eid' : eids, '1100-0.0' :  vals})     .set_index('eid')
    exp  = pd.DataFrame({'eid' : eids, '1100-0.0' : (vals - 1)}).set_index('eid')

    with tempdir():
        data.to_csv('data.csv')

        main.main('-cfg {} out.tsv data.csv'.format(cfg).split())

        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)

        assert (got == exp).all().all()
