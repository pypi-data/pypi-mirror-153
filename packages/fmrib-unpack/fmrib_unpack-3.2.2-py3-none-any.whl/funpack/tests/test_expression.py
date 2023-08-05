#!/usr/bin/env python
#
# test_expression.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import io
import textwrap as tw

import pytest

import pyparsing as pp

import pandas as pd
import numpy as np

import funpack.expression as expression

from . import gen_DataTable, gen_DataTableFromDataFrame



def test_Expression():

    _test_data = tw.dedent("""
    index 10 20 30
    1 1 2 3
    2 4 5 6
    3 7  9
    4 10 11 12
    5 13  15
    """).strip().replace(' ', '\t')

    _test_cols = {
        10 : '10',
        20 : '20',
        30 : '30',
    }


    _expr_tests = [
        (      'v10 == 1',   [1, 0, 0, 0, 0]),
        (      'v10 != 1',   [0, 1, 1, 1, 1]),
        (      'v10 >  7',   [0, 0, 0, 1, 1]),
        (      'v10 >= 7',   [0, 0, 1, 1, 1]),
        (      'v10 <  7',   [1, 1, 0, 0, 0]),
        (      'v10 <= 7',   [1, 1, 1, 0, 0]),
        (    '~(v10 == 1)',  [0, 1, 1, 1, 1]),
        (    '~(v10 != 1)',  [1, 0, 0, 0, 0]),
        (  'all(v10 != 1)',  [0, 1, 1, 1, 1]),
        (  'any(v10 != 1)',  [0, 1, 1, 1, 1]),
        ('~(all(v10 != 1))', [1, 0, 0, 0, 0]),
        ('~(any(v10 != 1))', [1, 0, 0, 0, 0]),
        ('all(~(v10 != 1))', [1, 0, 0, 0, 0]),


        ('v20 == na', [0, 0, 1, 0, 1]),
        ('v20 != na', [1, 1, 0, 1, 0]),

        (  'v10 >= 7 && v30 < 10',                [0, 0, 1, 0, 0]),
        ('~(v10 >= 7 && v30 < 10)',               [1, 1, 0, 1, 1]),
        ( 'v10 >= 4 &&  v30 < 10  || v20 != na',  [1, 1, 1, 1, 0]),
        ('(v10 >= 4 &&  v30 < 10) || v20 != na',  [1, 1, 1, 1, 0]),
        ( 'v10 >= 4 && (v30 < 10  || v20 != na)', [0, 1, 1, 1, 0]),

        ('v10 > 7 || v20 > 7 || v30 < 7',             [1, 1, 0, 1, 1]),
        ('v10 > 4 && v20 > 5 && v30 < 14',            [0, 0, 0, 1, 0]),
        ('v10 > 9 || v10 < 3 || v20 > 7 || v30 > 10', [1, 0, 0, 1, 1]),

        # n.b. and has higher precedence than or
        ('v10 > 4 && v20 > 5 || v30 < 14',        [1, 1, 1, 1, 0]),

        # bad
        ('10 == 1',        'error'),
        ('10 ==',          'error'),
        ('v10',            'error'),
        ('v10 ==',         'error'),
        ('v10 1',          'error'),
        ('v10 == 1 &&',    'error'),
        ('v10 == 1 && 24', 'error'),
        ('abcde',          'error'),
    ]

    def vine(e):
        vs = []
        if 'v10' in e: vs.append(10)
        if 'v20' in e: vs.append(20)
        if 'v30' in e: vs.append(30)
        return vs

    data =  pd.read_csv(io.StringIO(_test_data), sep='\t')

    for expr, expected in _expr_tests:

        if expected == 'error':
            with pytest.raises(pp.ParseException):
                e = expression.Expression(expr)
            continue
        else:
            e = expression.Expression(expr)

        assert sorted(e.variables) == sorted(vine(expr))

        result = e.evaluate(data, _test_cols)

        assert len(result) == len(expected)
        assert all([bool(r) == bool(e) for r, e in zip(result, expected)])


def test_Expression_multiple_columns():
    data       = np.random.randint(1, 100, (20, 6))
    data[:, 0] = np.arange(1, 21)
    cols       = ['eid', '1-0.0', '1-1.0', '1-2.0', '2-0.0', '2-1.0']
    df         = pd.DataFrame({c : d for c, d in zip(cols, data.T)}).set_index('eid')

    # one column
    e = expression.Expression('v1 > 50')
    result = e.evaluate(df, {1 : '1-0.0'})
    assert np.all(result.flatten() == (data[:, 1] > 50))

    # multiple columns
    e = expression.Expression('v1 <= 75')
    result = e.evaluate(df, {1 : ['1-0.0', '1-1.0']})
    assert np.all(result == (data[:, 1:3] <= 75))

    e = expression.Expression('v1 != 23')
    result = e.evaluate(df, {1 : ['1-0.0', '1-1.0', '1-2.0']})
    assert np.all(result == (data[:, 1:4] != 23))

    # multi-column multi-var - number
    # of columns per var must match
    e = expression.Expression('v1 > 50 && v2 < 50')
    result = e.evaluate(df, {1 : ['1-0.0', '1-1.0'],
                                 2 : ['2-0.0', '2-1.0']})
    exp = (data[:, 1:3] > 50) & (data[:, 4:] < 50)
    assert np.all(result == exp)

    # use any/all to collapse across columns
    e = expression.Expression('all(v1 > 50 && v2 < 50)')
    result = e.evaluate(df, {1 : ['1-0.0', '1-1.0'],
                             2 : ['2-0.0', '2-1.0']})
    exp = ((data[:, 1:3] > 50) & (data[:, 4:] < 50)).all(axis=1)
    assert np.all(result == exp)

    e = expression.Expression('any(v1 > 50 && v2 < 50)')
    result = e.evaluate(df, {1 : ['1-0.0', '1-1.0'],
                             2 : ['2-0.0', '2-1.0']})
    exp = ((data[:, 1:3] > 50) & (data[:, 4:] < 50)).any(axis=1)
    assert np.all(result == exp)

    e = expression.Expression('any(v1 > 50) && all(v2 < 50)')
    result = e.evaluate(df, {1 : ['1-0.0', '1-1.0', '1-2.0'],
                             2 : ['2-0.0', '2-1.0']})
    exp = (data[:, 1:4] > 50).any(axis=1) & (data[:, 4:] < 50).all(axis=1)
    assert np.all(result == exp)

    # column length mismatch - each variable
    # will be combined with logical OR, and
    # then expression evaluated on the 1D vectors
    e = expression.Expression('v1 > 50 && v2 < 50')
    exp = (data[:, 1:4] > 50).any(axis=1) & (data[:, 4:] < 50).any(axis=1)
    result = e.evaluate(df, {1 : ['1-0.0', '1-1.0', '1-2.0'],
                             2 : ['2-0.0', '2-1.0']})
    assert np.all(result == exp)


def test_calculateExpressionEvaluationOrder():

    def makexprs(exprstrs):
        exprs = []
        for exprstr in exprstrs:
            expr = [expression.Expression(e) for e in exprstr.split(',')]
            if len(expr) == 1:
                expr = expr[0]
            exprs.append(expr)
        return exprs

    vids = [1, 2, 3, 4, 5, 7]
    exprs = [
        'v3 == 0',             # 1 depends on 3
        'v3  > 2',             # 2 depends on 3
        'v4 != na',            # 3 depends on 4
        'v5 != na, v6 == na',  # 4 depends on 5 and 6
        'v6 < 0',              # 5 depends on 6
        'v8 == 34'             # 7 depends on 8
    ]

    expected = [
        (0, [1, 2, 7]),
        (1, [3]),
        (2, [4]),
        (3, [5]),
    ]

    exprs = makexprs(exprs)
    result = expression.calculateExpressionEvaluationOrder(vids, exprs)
    assert result == expected


    vids = [1, 2]
    exprs = ['v2 == 20, v3 > 400',
             'v3 < 200']
    expected = [(0, [1]),
                (1, [2])]
    exprs = makexprs(exprs)
    result = expression.calculateExpressionEvaluationOrder(vids, exprs)
    assert result == expected

    vids = [1, 2]
    exprs = ['v3 > 400, v2 == 20',
             'v3 < 200']
    expected = [(0, [1]),
                (1, [2])]
    exprs = makexprs(exprs)
    result = expression.calculateExpressionEvaluationOrder(vids, exprs)
    assert result == expected


    # error on self-dependency
    with pytest.raises(ValueError):
        vids  = [1, 2]
        exprs = ['v1 == 1', 'v4 == 42']
        expression.calculateExpressionEvaluationOrder(vids, makexprs(exprs))

    # error on circular-dependency
    with pytest.raises(ValueError):
        vids  = [1, 2]
        exprs = ['v2 == 1', 'v1 == 2']
        expression.calculateExpressionEvaluationOrder(vids, makexprs(exprs))


    # length mismatch
    with pytest.raises(ValueError):
        vids  = [1, 2, 3]
        exprs = ['v2 == 1']
        expression.calculateExpressionEvaluationOrder(vids, makexprs(exprs))


def test_Expresssion_non_numeric():
    test_data = tw.dedent("""
    index,10,20,30
    1,a,abc,a123
    2,b,def,a 101
    3,c,,b252
    4,d,jkl,b745
    5,e,,b254
    """).strip()

    test_cols = {
        10 : '10',
        20 : '20',
        30 : '30',
    }

    expr_tests = [
        ('v10 ==       "a"',     [1, 0, 0, 0, 0]),
        ("v10 ==       'a'",     [1, 0, 0, 0, 0]),
        ("v20 !=       'jkl'",   [1, 1, 1, 0, 1]),
        ('v20 ==       na',      [0, 0, 1, 0, 1]),
        ('v20 !=       na',      [1, 1, 0, 1, 0]),
        ('v30 ==       "a 101"', [0, 1, 0, 0, 0]),
        ('v30 contains "b2"',    [0, 0, 1, 0, 1]),
        ('v30 contains "b22"',   [0, 0, 0, 0, 0]),


        # bad
        ('v10 >  "a"', 'error'),
        ('v10 <= "a"', 'error'),
        ('v10 == a',  'error'),
        ('v10 == "a', 'error'),
        ('v10 == a"', 'error'),
    ]


    data =  pd.read_csv(io.StringIO(test_data), sep=',')

    for expr, expected in expr_tests:

        if expected == 'error':
            with pytest.raises(pp.ParseException):
                e = expression.Expression(expr)
            continue
        else:
            e = expression.Expression(expr)

        result = e.evaluate(data, test_cols)

        assert len(result) == len(expected)
        assert all([bool(r) == bool(e) for r, e in zip(result, expected)])


def test_Expresssion_datetime():
    testdata = tw.dedent("""
    eid,10,20
    1,2020-01-01,2020-01-01 01:00:00
    2,2020-02-01,2020-01-01 02:00:00
    3,2020-03-01,2020-01-01 03:00:00
    4,2020-04-01,2020-01-01 04:00:00
    """)

    test_cols = {
        10 : '10',
        20 : '20',
    }

    expr_tests = [
        ('v10 <= 2020-03-01',          [1, 1, 1, 0]),
        ('v10 == 2020-01-01',          [1, 0, 0, 0]),
        ('v10 >  2020-02-01',          [0, 0, 1, 1]),
        ('v20 == 2020-01-01 02:00:00', [0, 1, 0, 0]),
        ('v20 <  2020-01-01 03:00:00', [1, 1, 0, 0]),
        ('v20 >= 2020-01-01 02:00:00', [0, 1, 1, 1]),
    ]

    data =  pd.read_csv(io.StringIO(testdata),
                        sep=',',
                        parse_dates=['10', '20']).set_index('eid')

    for expr, expected in expr_tests:

        if expected == 'error':
            with pytest.raises(pp.ParseException):
                e = expression.Expression(expr)
            continue
        else:
            e = expression.Expression(expr)

        result = e.evaluate(data, test_cols)

        assert len(result) == len(expected)
        assert all([bool(r) == bool(e) for r, e in zip(result, expected)])
