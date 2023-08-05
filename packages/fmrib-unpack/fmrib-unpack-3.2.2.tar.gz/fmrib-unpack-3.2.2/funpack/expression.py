#!/usr/bin/env python
#
# expression.py - Parser for ParentValue expressions
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains functions for parsing conditional and logical
expressions, and the :class:`Expression` class for representing a parsed
expression.


.. autosummary::
   :nosignatures:

   Expression
   parseExpression
   variablesInExpression
   calculateExpressionEvaluationOrder


For a given variable, the ``ParentValues`` column of the variable table may
contain one or more *expressions*, which define conditions that parent
variables of the variable may meet in order for the variable value to be
replaced. This module contains logic for parsing and evaluating a single
expression - the evaluation of multiple comma-separated expressions is handled
in the :mod:`.importing` module.


An *expression* comprises one or more *conditional statements* (or
*statements* for short). A statement has the form::

    variable operator value

where:

  - ``variable`` is the ID of a parent variable of the variable in question.
    Variable IDs must be an integer preceded by the letter ``v``.
  - ``operator`` is a comparison operator (e.g. equals, greater than, etc.).
  - ``value`` is one of:
      - ``'na'`` indicating missing,
      - a numeric value against which the parent variable is to be compared.
      - a non-numeric value (i.e. a string), against which the parent variable
        is to be compared. The value must be quoted with either single or
        double quotes.

The following comparison operators are allowed (and the symbols used in a
statement can be found in the :attr:`SYMBOLS` dictionary):

 - equal to
 - not equal to
 - greater than
 - greater than or equal to
 - less than
 - less than or equal to


The *equal to* and *not equal to* operators may be used with a value of
``'na'`` to test whether the values for a variable are missing or present
respectively. Similarly, the *equal to* and *not equal to* operators may be
used with a non-numeric value to test for string equality.

Multiple conditional statements may be combined with ``and``, ``or``, and
``not`` logical operations (specific symbols can be found in the
:attr:`SYMBOLS` dictionary), and precedence may be enforced with the use of
round brackets.

The ``any`` and ``all`` operations can be applied to statements which have
been evaluated on multiple columns to combine the results column-wise.
"""


import                    collections
import                    logging
import                    re
import collections.abc as abc
import itertools       as it
import functools       as ft
import pyparsing       as pp
import numpy           as np


log = logging.getLogger(__name__)


SYMBOLS = {
    'var'      : 'v',
    'and'      : '&&',
    'or'       : '||',
    'not'      : '~',
    'any'      : 'any',
    'all'      : 'all',
    'eq'       : '==',
    'ne'       : '!=',
    'lt'       : '<',
    'le'       : '<=',
    'gt'       : '>',
    'ge'       : '>=',
    'contains' : 'contains',
    'na'       : 'na',
}
"""This dictionary contains the symbols for variables and operations that
may be used in expressions.
"""


class Expression:
    """The ``Expression`` class is a convenience class which can be used to
    parse and access an expression.
    """


    def __init__(self, expr):
        """Create an ``Expression`` object from the string ``expr``.

        :arg expr: Expression to be parsed.
        """

        self.__variables  = None
        self.__origExpr   = expr
        self.__expression = parseExpression(expr)


    def __str__(self):
        """Return the original string representation of the expression. """
        return self.__origExpr


    def __repr__(self):
        """Return the original string representation of the expression. """
        return str(self)


    @property
    def variables(self):
        """Return a list of all variables used in the expression. """

        if self.__variables is None:
            self.__variables = variablesInExpression(self.__expression)
        return self.__variables


    def evaluate(self, df, cols):
        """Evaluates this ``Expression`` and returns the result.

        :arg dtable: ``pandas.DataFrame`` containing the data.

        :arg cols:   Dictionary  containing ``{ variable : [column_name] }``
                     mappings from the variables used in the expressions to
                     columns in ``df``. Each mapping may also contain a
                     single column name, instead of a list.

        :returns:    The outcome of the expression - a ``numpy`` boolean array.
        """
        # replace any single column names
        # in the var-col mapping with lists
        cols = {v : [c] if isinstance(c, str) else c for v, c in cols.items()}
        return self.__expression(df, cols).squeeze()


def calculateExpressionEvaluationOrder(vids, exprs):
    """Identifies hierarchical relationships between variables.

    Given the variable table, identifies the hierarchical relationship order
    between all variables, and all parent variables used within their
    expressions.

    :arg vids:  Sequence of variable IDs

    :arg exprs: Sequence of parsed expression functions (as returned by
                :func:`parseExpression`), one for each variable in
                ``variables``. For each variable, there may be either one
                expression function, or a sequence of them.

    :returns:   A list of tuples, each containing:

                 - A hierarchy level
                 - A list of all variables at that level

                The list is in ascending order, by the hierarchy level
    """

    if len(vids) != len(exprs):
        raise ValueError('vids/exprs lengths don\'t match')

    # get a list of parents for each
    # var, then turn this into a dictionary
    # of { var : parents } mappings
    parents = []
    for expr in exprs:
        if not isinstance(expr, abc.Sequence):
            expr = [expr]
        parents.append(list(it.chain(*[e.variables for e in expr])))
    children = {i : list(sorted(p)) for i, p in zip(vids, parents)}

    # Make a list of all child/
    # parent variable IDs.
    childvids = vids
    allvids   = sorted(set(it.chain(vids, *parents)))

    # Then create a dictionary which will
    # store a hierarchy level for each
    # variable, where zero indicates that
    # the variable has no dependants.
    levels = collections.OrderedDict([(i, 0) for i in allvids])

    # Determine the hierarchy levels. For
    # each variable, we set the level on
    # each of its parents to one plus its
    # level. We use the seen set to keep
    # track of variables that have already
    # been visit, and thus to detect
    # circular or self-dependencies.
    def update(vid, level, seen):

        if vid in seen:
            raise ValueError('Circular dependency identified: {}'.format(vid))

        seen.add(vid)
        levels[vid] = level

        for parent in children.get(vid, set()):

            # only update parent level if it needs to
            # be updated - it may have already been
            # set by a sibling of this variable (i.e.
            # another variable at the same hierarchy
            # level as this one).
            if levels[parent] <= level:
                update(parent, level + 1, seen)

    for vid, level in levels.items():
        update(vid, level, set())

    # Now we can just sort the variables
    # by hierarchy to get the expression
    # evaluation order.
    bylevel = collections.OrderedDict()
    for vid, level in levels.items():
        if vid not in childvids:
            continue
        if level not in bylevel: bylevel[level]     = [vid]
        else:                    bylevel[level].append(vid)

    return list(sorted(bylevel.items(), key=lambda l: l[0]))


def parseExpression(expr):
    """Parses a string containing an expression.

    The expression may contain conditional statements of the form::
        variable comparison_operator value

    combined with logical expressions using symbols for ``and``, ``or``, and
    ``not``.

    The ``parseExpression`` function, given an expression string, will return
    a function that can be used to evaluate the expression. An expression
    function expects to be given two arguments:

    - A ``pandas.DataFrame`` which contains the data on all variables used
      in the expression
    - A dictionary containing ``{variable : column}`` mappings from the
      variables used in the expression to the columns of the data frame.

    An expression function will simply return ``True`` or ``False``, depending
    on the outcome of the expression.

    Expression functions have a few attributes containing metadata about the
    expression:

      - ``ftype`` contains the expression type, either ``unary`` (for *not*,
        *any* and *all* operations),
        ``binary`` (for *and*/*or* operations), or ``condition`` (for
        comparison operations)
      - ``operation`` contains the operation symbol

    Boolean *and*/*or* functions contain ``operand1`` and ``operand2``
    attributes which refer to the expression functions they will be applied
    to. Similarly, boolean *not* functions contain an ``operand`` attribute
    which refers to the expression function it will be applied to.  Comparison
    expression functions contain ``variable`` and ``value`` attributes, which
    contain the variable name and the value involved in the comparison.

    :arg expr: String containing an expression.
    :returns:  A function which can be used to evaluate the expression.
    """
    try:
        return list(makeParser().parseString(expr, parseAll=True))[0]
    except Exception as e:
        log.error('Error parsing expression "{}": {}'.format(expr, e))
        raise e


def variablesInExpression(expr):
    """Given an expression returned by :func:`parseExpression`, extracts all
    variables used in the expression.

    :arg expr: A *parsed* expression, produced by :func:`parseExpression`.
    :returns:  A set containing all of the variables that are mentioned in
               the expression.
    """

    if expr.ftype == 'condition':
        return set([expr.variable])

    elif expr.ftype == 'binary':
        variables = set()
        variables.update(variablesInExpression(expr.operand1))
        variables.update(variablesInExpression(expr.operand2))
        return variables

    elif expr.ftype == 'unary':
        return variablesInExpression(expr.operand)


def makeParser():
    """Generates a ``pyparsing`` parser which can be used to parse expressions.

    :returns: A ``pyparsing`` object which can parse an expression.
    """

    if getattr(makeParser, 'parser', None) is not None:
        return makeParser.parser

    CMP   = ['eq', 'ne', 'lt', 'le', 'gt', 'ge']
    CMPOP = pp.oneOf([SYMBOLS[c] for c in CMP])
    EQOP  = pp.oneOf([SYMBOLS[c] for c in ['eq', 'ne']])
    STROP = pp.oneOf([SYMBOLS[c] for c in ['eq', 'ne', 'contains']])
    ANY   = pp.CaselessLiteral(SYMBOLS['any'])
    ALL   = pp.CaselessLiteral(SYMBOLS['all'])
    AND   = pp.CaselessLiteral(SYMBOLS['and'])
    OR    = pp.CaselessLiteral(SYMBOLS['or'])
    NOT   = pp.CaselessLiteral(SYMBOLS['not'])
    NA    = pp.CaselessLiteral(SYMBOLS['na'])
    NUM   = pp.pyparsing_common.number
    DATE  = pp.Regex(r'\d\d\d\d-\d\d-\d\d',                re.ASCII)
    TIME  = pp.Regex(r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d', re.ASCII)
    DATE  = DATE ^ TIME
    STR   = pp.QuotedString("'") ^ pp.QuotedString('"')
    VAR   = (pp.CaselessLiteral(SYMBOLS['var']) +
             pp.pyparsing_common.integer).setParseAction(parseVariable)

    # a single conditional statement:
    # "variable comparison_operator value"
    NUMCOND  = pp.Group(VAR + CMPOP + NUM) .setParseAction(parseCondition)
    STRCOND  = pp.Group(VAR + STROP + STR) .setParseAction(parseCondition)
    DATECOND = pp.Group(VAR + CMPOP + DATE).setParseAction(parseCondition)
    NACOND   = pp.Group(VAR + EQOP  + NA)  .setParseAction(parseCondition)
    COND     = NUMCOND ^ STRCOND ^ DATECOND ^ NACOND

    # the infixNotation helper does the heavy
    # lifting for boolean/combine operations
    # and precedence
    parser = pp.infixNotation(
        COND,
        [(NOT, 1, pp.opAssoc.RIGHT, parseUnary),
         (ANY, 1, pp.opAssoc.RIGHT, parseUnary),
         (ALL, 1, pp.opAssoc.RIGHT, parseUnary),
         (AND, 2, pp.opAssoc.LEFT , parseBinary),
         (OR,  2, pp.opAssoc.LEFT,  parseBinary)])

    makeParser.parser = parser
    return parser


def parseVariable(toks):
    """Called by the parser created by :func:`makeParser`. Parses a variable
    identifier, returning an integer ID.
    """
    return toks[1]


# These functions implement the logic for
# evaluating unary and binary expressions.
# They must be module-level functions, as
# they must be pickle-able.
#
# Conditional expressions are constructed to
# produce numpy arrays (see parseCondition
# and its use of _asarray), so that is what
# these unary/binary operations expect as
# einputs.
def _not(op, *args):
    return ~op(*args)

def _any(op, *args):
    result = op(*args)
    if len(result.shape) == 2: return result.any(axis=1)
    else:                      return result

def _all(op, *args):
    result = op(*args)
    if len(result.shape) == 2: return result.all(axis=1)
    else:                      return result

def _and(op1, op2, *args):
    op1, op2 = _evalBinaryOperands(op1, op2, *args)
    return op1 & op2

def _or( op1, op2, *args):
    op1, op2 = _evalBinaryOperands(op1, op2, *args)
    return op1 | op2

def _evalBinaryOperands(op1, op2, *args):
    op1 = op1(*args)
    op2 = op2(*args)

    if op1.shape != op2.shape:
        if len(op1.shape) == 2: op1 = op1.any(axis=1)
        if len(op2.shape) == 2: op2 = op2.any(axis=1)

    return op1, op2


def parseUnary(toks):
    """Called by the parser created by :func:`makeParser`. Parses an expression of
    the form ``[not|any|all] expression``, where ``not``/``any``/``all`` is
    the corresponding symbol in the :attr:`SYMBOLS` dictionary, and
    ``expression`` is a conditional statement or logical expression.

    Returns a function which can be used to evaluate the expression.
    """

    operation = toks[0][0]
    operand   = toks[0][1]

    log.debug('Parsing unary: %s %s', operation, operand)

    fn = {SYMBOLS['not'] : _not,
          SYMBOLS['any'] : _any,
          SYMBOLS['all'] : _all}[operation]

    fn           = ft.partial(fn, operand)
    fn.ftype     = 'unary'
    fn.operation = operation
    fn.operand   = operand

    return fn


def parseBinary(toks):
    """Called by the parser created by :func:`makeParser`. Parses an
    expression of the form ``expression1 [and|or] expression2``, where
    ``and``/``or`` are the corresponding symbols in the :attr:`SYMBOLS`
    dictionary, and ``expression1`` and ``expression2`` are conditional
    statements or logical expression.

    Binary expressions expect that the shape of both operands is equal;
    the number of rows is guaranteed to match (because ultimately the
    operands are coming from the same ``pandas.DataFrame``. But the
    number of columns may differ if, for example, one operand has been
    calculated from a multi-valued variable, and another from a single-
    valued variable.

    The outcome of this situation can be explicitly controlled in the query
    by use of the ``any`` and ``all`` operators, which can be used to
    collapse the columns of a variable down to a single column.

    But if this is not explicitly controlled, the default behaviour which
    occurs when the operands of a binary operator have a different number of
    columns is to collapse both operands down to a single column via the
    ``any`` operator - in other words, combining values within each row witha
    logical "or" operation.

    Returns a function which can be used to evaluate the expression.
    """

    # n.b. toks may be a pp.ParseResults object,
    # or a list of lists of topens - see below.
    operand1  = toks[0][0]
    operation = toks[0][1]

    # if multiple identical binary
    # conditions are chained together
    # (e.g. "a || b || c"), pyparsing
    # will pass them all to a single
    # parseBinary call. Here we cheat
    # a bit by recursively parsing
    # the rightmost condition(s).
    if len(toks[0]) == 3: operand2 = toks[0][2]
    else:                 operand2 = parseBinary([toks[0][2:]])

    log.debug('Parsing logical %s %s %s', operand1, operation, operand2)

    if   operation == SYMBOLS['and']: fn = _and
    elif operation == SYMBOLS['or']:  fn = _or

    fn           = ft.partial(fn, operand1, operand2)
    fn.ftype     = 'binary'
    fn.operation = operation
    fn.operand1  = operand1
    fn.operand2  = operand2

    return fn


def _isna( var, val, df, cols): return df[cols[var]].isna()  # noqa
def _notna(var, val, df, cols): return df[cols[var]].notna() # noqa
def _eq(   var, val, df, cols): return df[cols[var]] == val  # noqa
def _ne(   var, val, df, cols): return df[cols[var]] != val  # noqa
def _gt(   var, val, df, cols): return df[cols[var]] >  val  # noqa
def _ge(   var, val, df, cols): return df[cols[var]] >= val  # noqa
def _lt(   var, val, df, cols): return df[cols[var]] <  val  # noqa
def _le(   var, val, df, cols): return df[cols[var]] <= val  # noqa

# we can't perform str.contains
# on multiple columns at once
def _contains(var, val, df, cols):
    cols   = cols[var]
    result = np.zeros((len(df), len(cols)), dtype=np.bool)
    for i, col in enumerate(cols):
        result[:, i] = df[col].str.contains(val, case=False)
    return result


def _asarray(func, *args):
    """Calls ``func``, passing it ``*args``.

    The return value of ``func`` is assumed to be a ``pandas.DataFrame``.
    Its contents are converted to a ``numpy`` array.

    This function is used by :func:`parseCondition` to construct functions
    for evaluating conditional statements.
    """

    val = func(*args)

    if not isinstance(val, np.ndarray):
        # DataFrame.to_numpy is only
        # available in pandas >= 0.24
        val = val.to_numpy()

    return val


def parseCondition(toks):
    """Parses a conditional statement of the form::

        variable operation value

    where:
      - ``variable`` is a variable identifier
      - ``operation`` is a comparison operation
      - ``value`` is a numeric value

    Returns a function which can be used to evaluate the conditional statement.
    The function is constructed such that it expects a ``pandas.DataFrame``,
    and will output a boolean ``numpy`` array.
    """
    toks      = toks[0]
    variable  = toks[0]
    operation = toks[1]
    value     = toks[2]

    log.debug('Parsing condition: v%s %s %s', variable, operation, value)

    if   operation == SYMBOLS['eq'] and value == 'na': fn = _isna
    elif operation == SYMBOLS['ne'] and value == 'na': fn = _notna
    elif operation == SYMBOLS['eq']:                   fn = _eq
    elif operation == SYMBOLS['ne']:                   fn = _ne
    elif operation == SYMBOLS['ge']:                   fn = _ge
    elif operation == SYMBOLS['gt']:                   fn = _gt
    elif operation == SYMBOLS['le']:                   fn = _le
    elif operation == SYMBOLS['lt']:                   fn = _lt
    elif operation == SYMBOLS['contains']:             fn = _contains

    fn           = ft.partial(_asarray, fn, variable, value)
    fn.ftype     = 'condition'
    fn.operation = operation
    fn.variable  = variable
    fn.value     = value

    return fn
