from sympy import Rational, latex

from extension.util import format_latex
from gamma.dispatch import DICT
from gamma.result_card import ResultCard


def format_input(result_statement, input_repr, components: DICT):
    expression = components['expression']
    return f"Rational('{expression}')"


def rational(components: DICT, parameters=None) -> str:
    expression = components['expression']
    return latex(Rational(expression))  # todo: remove duplicated logic


rational_card = ResultCard('Rational', None, format_input=format_input, eval_method=rational,
                           format_output=format_latex)
