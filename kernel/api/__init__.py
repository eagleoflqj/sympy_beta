import re
import traceback
from typing import Callable

from sympy import Basic, Symbol, __version__
from sympy.parsing.latex import parse_latex

from extension.util import DICT
from gamma.logic import SymPyGamma
from nlp import translate


def catch(func: Callable) -> Callable:
    def closure(*args):
        try:
            return func(*args)
        except Exception:
            return {'error': traceback.format_exc()}
    return closure


@catch
def eval_input(raw_input: str, variable: str | None = None):
    try:
        return SymPyGamma(raw_input, variable).eval()
    except SyntaxError:
        try:
            fl = translate(raw_input)
            return {'result': fl}
        except SyntaxError:
            return {'error': "SymPy Beta can't understand your input."}
        except ValueError:
            return {'error': "This query probably doesn't make sense."}


_braces_pattern = re.compile(r'(\w+)_\{(\d+)}')


@catch
def eval_latex_input(raw_input: str):
    sp_obj: Basic = parse_latex(raw_input)  # type: ignore
    sp_obj = sp_obj.replace(lambda x: x.is_Symbol, lambda x: Symbol(_braces_pattern.sub(R'\1_\2', x.name)))
    return {'result': str(sp_obj)}


@catch
def eval_card(card_name: str, expression: str, variable: str | None, parameters: DICT | None):
    return SymPyGamma(expression, variable).eval_card(card_name, parameters)


def get_sympy_version() -> str:
    return __version__
