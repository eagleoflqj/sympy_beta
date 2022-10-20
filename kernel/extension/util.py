import base64
from contextlib import contextmanager
import importlib
import io
from typing import TYPE_CHECKING, Any, Callable, Iterable, cast

import matplotlib
from matplotlib.figure import Figure
from sympy import Basic, Symbol
import sympy
from sympy.core.function import Function, UndefinedFunction

from data_type import Svg, Tex, Text, _Tex

if TYPE_CHECKING:
    from gamma.result_card import ResultCard

matplotlib.use('SVG')
matplotlib.rcParams['svg.hashsalt'] = 'fixed'

DICT = dict[str, Any]


def t(text: str) -> str:
    return R'\text{' + text + '}'


class Latex:
    def __init__(self):
        self.buffer: list[str] = []

    def a(self, *args):  # append
        for arg in args:
            self.buffer.append(str(arg))
        return self

    def t(self, arg):
        return self.a(t(arg))

    def n(self):  # new line
        return self.a(R'\\\\\\')

    def eq(self, lhs, rhs):
        return self.a(lhs, '=', rhs)

    def for_we_have_so(self, conditions: list[str], conclusions: list[str], results: list[str]):
        self.a(t('For '), ', '.join(conditions),
               t(', we have '), ', '.join(conclusions),
               t(', so ') + ', '.join(results))
        return self.n()

    def as_a_result(self, conclusions: list[str]):
        return self.a(t('As a result, '), ', '.join(conclusions))

    def f(self):  # finish
        return ''.join(self.buffer)


def format_latex(tex: str) -> _Tex:
    return Tex(tex=tex)


def format_text(text: str):
    return Text(text=text)


def format_figure(output: tuple[Figure, str]):
    import matplotlib.pyplot as plt  # must appear after switching backend, see pyodide#442
    figure, category = output
    buf = io.BytesIO()
    figure.savefig(buf, format='svg', metadata={
        'Creator': None, 'Date': None, 'Format': None, 'Type': None
    })
    plt.close(figure)
    buf.seek(0)
    svg = base64.b64encode(buf.read()).decode()
    return Svg(svg=svg, category=category)


def take_int_input(inner: Callable[[int], Any]) -> Callable[[DICT, Any], Any]:
    def wrapper(components: DICT, parameters: None) -> Any:
        return inner(int(components['input_evaluated']))
    return wrapper


def load_with_source(sub_module_name: str) -> 'ResultCard':
    module_name = f'extension.{sub_module_name}'
    module = importlib.import_module(module_name)
    dirs = module_name.split('.')
    card_name = f'{dirs[-1]}_card'
    card: ResultCard = module.__getattribute__(card_name)
    card.source = '/'.join(dirs) + '.py'
    return card


def no_undefined_function(components: DICT) -> bool:
    def helper(obj):
        if isinstance(obj, Basic):
            return not any(isinstance(type(fx), UndefinedFunction) for fx in obj.find(Function))
        if isinstance(obj, Iterable):
            return all(helper(item) for item in (obj.values() if isinstance(obj, dict) else obj))
        return True
    return helper(components['input_evaluated'])


def sorted_free_symbols(obj: Basic) -> list[Symbol]:
    return sorted(cast(set[Symbol], obj.free_symbols), key=lambda s: s.name)

@contextmanager
def patch_latex():

    def handle_limit(func):
        sub = func.limit_sub()
        if sub.LETTER():
            var = Symbol(sub.LETTER().getText())
        elif sub.SYMBOL():
            var = Symbol(sub.SYMBOL().getText()[1:])
        else:
            var = Symbol('x')
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
        
    handle_limit_orig = sympy.parsing.latex._parse_latex_antlr.handle_limit
    _print_Limit_orig = sympy.StrPrinter._print_Limit

    try:
        sympy.parsing.latex._parse_latex_antlr.handle_limit = handle_limit
        sympy.StrPrinter._print_Limit = _print_Limit
        yield
    finally:
        sympy.parsing.latex._parse_latex_antlr.handle_limit = handle_limit_orig
        sympy.StrPrinter._print_Limit = _print_Limit_orig
