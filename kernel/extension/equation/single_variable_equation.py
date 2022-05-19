from sympy import S, Set, Symbol, solveset

from extension.util import DICT, Latex, format_latex, no_undefined_function
from gamma.result_card import ResultCard
from gamma.utils import latex


def solve_single_var(components: DICT, parameters=None) -> tuple[Set, Symbol, bool]:
    equation = components['input_evaluated']
    x: Symbol = components['variable']
    try:
        result = solveset(equation, x)
        is_complex = True
    except ValueError:
        result = solveset(equation, x, S.Reals)
        is_complex = False
    return result, x, is_complex


def format_solution(output: tuple[Set, Symbol, bool]):
    result, x, is_complex = output
    pre_output = f'{"Complex" if is_complex else "Real"} root: '
    return format_latex(Latex().t(pre_output).a(R'x \in', latex(result)).f())


single_variable_equation_card = ResultCard('Root', None, eval_method=solve_single_var, format_output=format_solution,
                                           applicable=no_undefined_function)
