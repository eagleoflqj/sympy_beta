from __future__ import annotations

from typing import Any, Callable

import sympy

from gamma.evaluator import eval_node

DICT = dict[str, Any]


# Decide which result card set to use

def is_derivative(input_evaluated):
    return isinstance(input_evaluated, sympy.Derivative)


def is_integral(input_evaluated):
    return isinstance(input_evaluated, sympy.Integral)


def is_float(input_evaluated):
    return isinstance(input_evaluated, sympy.Float)


def is_numbersymbol(input_evaluated):
    return isinstance(input_evaluated, sympy.NumberSymbol)


def is_constant(input_evaluated):
    # is_constant reduces trig identities (even with simplify=False?) so we
    # check free_symbols instead
    return hasattr(input_evaluated, 'free_symbols') \
        and not input_evaluated.free_symbols


def is_complex(input_evaluated):
    try:
        return sympy.I in input_evaluated.atoms()
    except (AttributeError, TypeError):
        return False


def is_trig(input_evaluated):
    return isinstance(input_evaluated, sympy.Basic) \
        and any(input_evaluated.find(func)
                for func in (sympy.sin, sympy.cos, sympy.tan, sympy.csc, sympy.sec, sympy.cot))


def is_not_constant_basic(input_evaluated):
    return not is_constant(input_evaluated) \
        and isinstance(input_evaluated, sympy.Basic) \
        and not is_logic(input_evaluated)


def is_uncalled_function(input_evaluated):
    return hasattr(input_evaluated, '__call__') and not isinstance(input_evaluated, sympy.Basic)


def is_matrix(input_evaluated):
    return isinstance(input_evaluated, sympy.Matrix)


def is_logic(input_evaluated):
    return isinstance(input_evaluated, (sympy.And, sympy.Or, sympy.Not, sympy.Xor))


def is_sum(input_evaluated):
    return isinstance(input_evaluated, sympy.Sum)


def is_product(input_evaluated):
    return isinstance(input_evaluated, sympy.Product)


# Functions to convert input and extract variable used

def default_variable(top_node, evaluated) -> DICT:
    variables = list(evaluated.free_symbols) if isinstance(evaluated, sympy.Basic) else []
    return {
        'variables': variables,
        'variable': variables[0] if variables else None,
        'input_evaluated': evaluated
    }


def extract_first(top_node, evaluated) -> DICT:
    result = default_variable(top_node, evaluated)
    result['input_evaluated'] = eval_node(top_node.args[0])
    return result


def extract_integral(top_node, evaluated) -> DICT:
    args = [eval_node(arg) for arg in top_node.args]
    expr, limits = args[0], args[1:]
    variables = []

    if not limits:
        variables = [expr.free_symbols.pop()]
        limits = variables
    else:
        for limit in limits:
            if isinstance(limit, tuple):
                variables.append(limit[0])
            else:
                variables.append(limit)

    return {
        'input_evaluated': evaluated,
        'integrand': expr,
        'variables': variables,
        'variable': variables[0],
        'limits': limits
    }


def extract_derivative(top_node, evaluated) -> DICT:
    args = [eval_node(arg) for arg in top_node.args]
    expr = args[0]
    free_variables = sorted(expr.free_symbols, key=str)

    if len(args) > 1:
        free_variables.remove(args[1])
        free_variables.insert(0, args[1])

    return {
        'function': expr,
        'variables': free_variables,
        'variable': free_variables[0],
        'input_evaluated': expr
    }


def extract_plot(top_node, evaluated) -> DICT:
    result = {}
    if top_node.args:
        args = [eval_node(arg) for arg in top_node.args]
        if isinstance(args[0], sympy.Basic):
            result['variables'] = list(args[0].atoms(sympy.Symbol))
            result['variable'] = result['variables'][0]
            result['input_evaluated'] = [args[0]]

            if len(result['variables']) != 1:
                raise ValueError("Cannot plot function of multiple variables")
        else:
            variables = set()
            try:
                for func in args[0]:
                    variables.update(func.atoms(sympy.Symbol))
            except TypeError:
                raise ValueError("plot() accepts either one function, a list of functions, or keyword arguments")

            variables = list(variables)
            if len(variables) > 1:
                raise ValueError('All functions must have the same and at most one variable')
            if len(variables) == 0:
                variables.append(sympy.Symbol('x'))
            result['variables'] = variables
            result['variable'] = variables[0]
            result['input_evaluated'] = args[0]
    elif top_node.keywords:
        kwargs = {keyword.arg: eval_node(keyword.value) for keyword in top_node.keywords}
        result['variables'] = [sympy.Symbol('x')]
        result['variable'] = sympy.Symbol('x')

        parametrics = 1
        functions = {}
        for f in kwargs:
            if f.startswith('x'):
                y_key = 'y' + f[1:]
                if y_key in kwargs:
                    # Parametric
                    x = kwargs[f]
                    y = kwargs[y_key]
                    functions['p' + str(parametrics)] = (x, y)
                    parametrics += 1
            else:
                if f.startswith('y') and ('x' + f[1:]) in kwargs:
                    continue
                functions[f] = kwargs[f]
        result['input_evaluated'] = functions
    return result


"""
predicate: str or func
  If a string, names a function that uses this set of result cards.
  If a function, the function, given the evaluated input, returns True if
  this set of result cards should be used.

extract_components: None or func
  If None, use the default function.
  If a function, specifies a function that parses the input expression into
  a components dictionary. For instance, for an integral, this function
  might extract the limits, integrand, and variable.

result_cards: tuple
  If empty, do not show any result cards for this function beyond the
  automatically generated 'Result' and 'Simplification' cards (if they are
  applicable).
  If not empty, specifies a list of result cards to display.
"""

Integer_result = (None, ('digits', 'factorization', 'factorizationDiagram'))

CONVERTER = Callable[[Any, Any], DICT]

function_map: dict[str, tuple[CONVERTER | None, tuple[str, ...]]] = {
    'Integer': Integer_result,
    'factorial': Integer_result,
    'factorial2': Integer_result,
    'integrate': (extract_integral, ('integral_alternate_fake', 'intsteps')),
    'diff': (extract_derivative, ('diff',)),
    'factorint': (extract_first, ('factorization', 'factorizationDiagram')),
    'isprime': (extract_first, ('result', 'is_prime',)),
    'totient': (extract_first, ('totient',)),
    'help': (extract_first, ('function_docs',)),
    'plot': (extract_plot, ('plot',)),
}

exclusive_predicates = [
    (is_complex, ('absolute_value', 'polar_angle', 'conjugate')),
    (is_float, ('fractional_approximation',)),
    # root_to_polynomial
    (is_uncalled_function, ('function_docs',)),
    (is_matrix, ('matrix_inverse', 'matrix_eigenvals', 'matrix_eigenvectors')),
    (is_logic, ('satisfiable', 'truth_table')),
    (is_sum, ('doit',)),
    (is_product, ('doit',)),
]

inclusive_predicates = [
    (is_trig, ('trig_alternate',)),
    (is_not_constant_basic, ('plot', 'roots', 'diff', 'integral_alternate', 'series'))
]


def find_result_set(function_name: str, input_evaluated, is_imperative: bool) -> tuple[CONVERTER, list[str]]:
    """
    Finds a set of result cards based on function name and evaluated input.

    Returns:

    - Function that parses the evaluated input into components. For instance,
      for an integral this would extract the integrand and limits of integration.
      This function will always extract the variables.
    - List of result cards.
    """
    result_converter: CONVERTER = default_variable

    converter, result_cards = function_map.get(function_name, (None, None))
    if result_cards is not None:
        result_converter = converter or result_converter
        return result_converter, list(result_cards)

    if is_imperative:
        return result_converter, []

    for predicate, result_cards in exclusive_predicates:
        if predicate(input_evaluated):
            return result_converter, list(result_cards)

    result: list[str] = []
    for predicate, result_cards in inclusive_predicates:
        if predicate(input_evaluated):
            result.extend(result_cards)

    return result_converter, result
