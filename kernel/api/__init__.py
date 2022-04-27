import traceback
from typing import Callable

from sympy.parsing.latex import parse_latex

from gamma.dispatch import DICT
from gamma.logic import SymPyGamma


def catch(func: Callable) -> Callable:
    def closure(*args):
        try:
            return func(*args)
        except Exception:
            return {'error': traceback.format_exc()}
    return closure


@catch
def eval_input(raw_input: str, variable: str | None = None):
    return SymPyGamma(raw_input, variable).eval()


@catch
def eval_latex_input(raw_input: str):
    expr = parse_latex(raw_input)
    return {'result': str(expr)}


@catch
def eval_card(card_name: str, expression: str, variable: str | None, parameters: DICT | None):
    return SymPyGamma(expression, variable).eval_card(card_name, parameters)


def get_sympy_version() -> str:
    import sympy
    return sympy.__version__  # type: ignore
