import ast

from sympy.parsing.sympy_parser import split_symbols, function_exponentiation, implicit_application, \
    standard_transformations, convert_xor, stringify_expr, eval_expr, NAME

SYNONYMS = {
    'derivative': 'diff',
    'derive': 'diff',
    'integral': 'integrate',
    'antiderivative': 'integrate',
    'factorize': 'factor',
    'graph': 'plot',
    'draw': 'plot'
}


def synonyms(tokens, local_dict, global_dict):
    """Make some names synonyms for others.

    This is done at the token level so that the "stringified" output that
    Gamma displays shows the correct function name. Must be applied before
    auto_symbol.
    """

    result = []
    for token in tokens:
        if token[0] == NAME:
            if token[1] in SYNONYMS:
                result.append((NAME, SYNONYMS[token[1]]))
                continue
        result.append(token)
    return result


def custom_implicit_transformation(result, local_dict, global_dict):
    """Allows a slightly relaxed syntax.

    - Parentheses for single-argument method calls are optional.

    - Multiplication is implicit.

    - Symbol names can be split (i.e. spaces are not needed between
      symbols).

    - Functions can be exponentiated.

    Example:

    >>> from sympy.parsing.sympy_parser import (parse_expr,
    ... standard_transformations, implicit_multiplication_application)
    >>> parse_expr("10sin**2 x**2 + 3xyz + tan theta",
    ... transformations=(standard_transformations +
    ... (implicit_multiplication_application,)))
    3*x*y*z + 10*sin(x**2)**2 + tan(theta)

    """
    for step in (split_symbols, implicit_application, function_exponentiation):
        result = step(result, local_dict, global_dict)

    return result


namespace = {}
exec('from gamma.pre_exec import *', {}, namespace)


def plot(f=None, **kwargs):
    """Plot functions. Not the same as SymPy's plot.

    This plot function is specific to Gamma. It has the following syntax::

        plot([x^2, x^3, ...])

    or::

        plot(y=x,y1=x^2,r=sin(theta),r1=cos(theta))

    ``plot`` accepts either a list of single-variable expressions to
    plot or keyword arguments indicating expressions to plot. If
    keyword arguments are used, the plot will be polar if the keyword
    argument starts with ``r`` and will be an xy graph otherwise.

    Note that Gamma will cut off plot values above and below a
    certain value, and that it will **not** warn the user if so.

    """
    pass


namespace.update({
    'plot': plot,  # prevent textplot from printing stuff
    'help': lambda f: f,
    'len': len,
    'str': str,
})

transformations = [synonyms, *standard_transformations, convert_xor, custom_implicit_transformation]


def eval_input(s: str):
    parsed = stringify_expr(s, {}, namespace, transformations)
    evaluated = eval_expr(parsed, {}, namespace)
    return parsed, ast.parse(parsed).body[0].value, evaluated


def eval_node(node):
    tree = ast.fix_missing_locations(ast.Expression(node))
    return eval(compile(tree, '<string>', 'eval'), namespace)
