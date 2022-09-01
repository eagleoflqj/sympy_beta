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
    import sympy
    import sympy.parsing.latex._parse_latex_antlr

    handle_limit_orig = sympy.parsing.latex._parse_latex_antlr.handle_limit
    _print_Limit_orig = sympy.StrPrinter._print_Limit

    def handle_limit(func):
        sub = func.limit_sub()
        if sub.LETTER():
            var = sympy.Symbol(sub.LETTER().getText())
        elif sub.SYMBOL():
            var = sympy.Symbol(sub.SYMBOL().getText()[1:])
        else:
            var = sympy.Symbol('x')
        if sub.SUB():
            direction = "-"
        elif sub.ADD():
            direction = "+"
        else:
            direction = "+-"
        approaching = sympy.parsing.latex._parse_latex_antlr.convert_expr(sub.expr())
        content = sympy.parsing.latex._parse_latex_antlr.convert_mp(func.mp())

        return sympy.Limit(content, var, approaching, direction)

    def _print_Limit(self, expr):
        e, z, z0, dir = expr.args
        return "Limit(%s, %s, %s, dir='%s')" % tuple(map(self._print, (e, z, z0, dir)))

    def patch_latex():
        sympy.parsing.latex._parse_latex_antlr.handle_limit = handle_limit
        sympy.StrPrinter._print_Limit = _print_Limit

    def unpatch_latex():
        sympy.parsing.latex._parse_latex_antlr.handle_limit = handle_limit_orig
        sympy.StrPrinter._print_Limit = _print_Limit_orig

    patch_latex()
    sp_obj: Basic = parse_latex(raw_input)  # type: ignore
    sp_obj = sp_obj.replace(lambda x: x.is_Symbol, lambda x: Symbol(_braces_pattern.sub(R'\1_\2', x.name)))  # type: ignore
    result = str(sp_obj)
    unpatch_latex()
    return {'result': result}


@catch
def eval_card(card_name: str, expression: str, variable: str | None, parameters: DICT | None):
    return SymPyGamma(expression, variable).eval_card(card_name, parameters)


def get_sympy_version() -> str:
    return __version__
