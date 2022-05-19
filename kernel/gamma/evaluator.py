import ast
import re
from tokenize import NAME, OP
from typing import Any

from nltk.corpus import words
from sympy.parsing.sympy_parser import (AppliedFunction, _apply_functions, _flatten, _group_parentheses,
                                        _token_callable, convert_xor, function_exponentiation, implicit_application,
                                        split_symbols_custom, standard_transformations)

TOKEN = tuple[int, str]
DICT = dict[str, Any]

SYNONYMS = {
    'derivative': 'diff',
    'derive': 'diff',
    'integral': 'integrate',
    'antiderivative': 'integrate',
    'factorize': 'factor',
    'graph': 'plot',
    'draw': 'plot'
}


def synonyms(tokens: list[TOKEN], local_dict: DICT, global_dict: DICT):
    """Make some names synonyms for others.

    This is done at the token level so that the "stringified" output that
    Gamma displays shows the correct function name. Must be applied before
    auto_symbol.
    """

    result = []
    for token in tokens:
        token_type, token_value = token
        if token_type == NAME:
            synonym = SYNONYMS.get(token_value.lower())
            if synonym is not None:
                result.append((NAME, synonym))
                continue
        result.append(token)
    return result


vocabulary: set[str] = set(words.words())
variable_pattern = re.compile(r'([A-Za-z][a-z]*)_?\d*')


def token_splittable(token: str) -> bool:
    match = variable_pattern.fullmatch(token)
    if match:
        prefix = match.group(1)
        if prefix.lower() in vocabulary:
            return False
    return True


split_symbols = split_symbols_custom(token_splittable)


def _implicit_multiplication(tokens: list[TOKEN | AppliedFunction], local_dict: DICT, global_dict: DICT):
    """
    Copied from sympy 9c67e41e636886f5c36add48ef531cd5fdbde8cb
    """
    result: list[TOKEN | AppliedFunction] = []
    skip = False
    for tok, nextTok in zip(tokens, tokens[1:]):
        result.append(tok)
        if skip:
            skip = False
            continue
        if tok[0] == OP and tok[1] == '.' and nextTok[0] == NAME:
            # Dotted name. Do not do implicit multiplication
            skip = True
            continue
        if isinstance(tok, AppliedFunction):
            if isinstance(nextTok, AppliedFunction):
                result.append((OP, '*'))
            elif nextTok == (OP, '('):
                # Applied function followed by an open parenthesis
                if tok.function[1] == "Function":
                    # tok.function = (tok.function[0], 'Symbol')
                    continue  # modify: we don't want f(x) to be f*x
                result.append((OP, '*'))
            elif nextTok[0] == NAME:
                # Applied function followed by implicitly applied function
                result.append((OP, '*'))
        else:
            if tok == (OP, ')'):
                if isinstance(nextTok, AppliedFunction):
                    # Close parenthesis followed by an applied function
                    result.append((OP, '*'))
                elif nextTok[0] == NAME:
                    # Close parenthesis followed by an implicitly applied function
                    result.append((OP, '*'))
                elif nextTok == (OP, '('):
                    # Close parenthesis followed by an open parenthesis
                    result.append((OP, '*'))
            elif tok[0] == NAME and not _token_callable(tok, local_dict, global_dict):
                if isinstance(nextTok, AppliedFunction) or \
                        (nextTok[0] == NAME and _token_callable(nextTok, local_dict, global_dict)):
                    # Constant followed by (implicitly applied) function
                    result.append((OP, '*'))
                elif nextTok == (OP, '('):
                    # Constant followed by parenthesis
                    result.append((OP, '*'))
                elif nextTok[0] == NAME:
                    # Constant followed by constant
                    result.append((OP, '*'))
    if tokens:
        result.append(tokens[-1])
    return result


def implicit_multiplication(tokens: list[TOKEN], local_dict: DICT, global_dict: DICT) -> list[TOKEN]:
    # These are interdependent steps, so we don't expose them separately
    res1 = _group_parentheses(implicit_multiplication)(tokens, local_dict, global_dict)
    res2 = _apply_functions(res1, local_dict, global_dict)
    res3 = _implicit_multiplication(res2, local_dict, global_dict)
    result = _flatten(res3)
    return result


def custom_implicit_transformation(result, local_dict, global_dict):
    """Allows a slightly relaxed syntax.

    - Parentheses for single-argument method calls are optional.

    - Multiplication is implicit.

    - Symbol names can be split (i.e. spaces are not needed between
      symbols).

    - Functions can be exponentiated.
    """
    for step in (split_symbols, implicit_multiplication, implicit_application, function_exponentiation):
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

function_map = {
    'delta': 'DiracDelta',
    'theta': 'Heaviside',
}


def transform_function(tokens: list[TOKEN], local_dict: DICT, global_dict: DICT) -> list[TOKEN]:
    """
    map theta(x) to Heaviside(x)
    """
    result: list[TOKEN] = []
    i = 0
    while i < len(tokens):
        if tokens[i] == (NAME, 'Function'):
            name = tokens[i+2][1][1:-1]
            func = function_map.get(name)
            if func:
                result.append((NAME, func))
                i += 4
                continue
        result.append(tokens[i])
        i += 1
    return result


transformations = [synonyms, *standard_transformations, transform_function, convert_xor, custom_implicit_transformation]


def eval_node(node):
    tree = ast.fix_missing_locations(ast.Expression(node))
    return eval(compile(tree, '<string>', 'eval'), namespace)
