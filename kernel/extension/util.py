import base64
import importlib
import io
from typing import Any, Callable

import matplotlib
from matplotlib.figure import Figure

from api.data_type import Svg, Tex, Text, _Tex
from gamma.dispatch import DICT
from gamma.result_card import ResultCard

matplotlib.use('SVG')


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


def format_latex(tex: str, formatter=None) -> _Tex:
    return Tex(tex=tex)


def format_text(text: str, formatter=None):
    return Text(text=text)


def format_figure(output: tuple[Figure, str], formatter=None):
    figure, name = output
    buf = io.BytesIO()
    figure.savefig(buf, format='svg', metadata={'Date': None})
    buf.seek(0)
    svg = base64.b64encode(buf.read()).decode()
    return Svg(svg=svg, name=name)


def take_int_input(inner: Callable[[int], Any]) -> Callable[[DICT, Any], Any]:
    def wrapper(components: DICT, parameters: None) -> Any:
        return inner(int(components['input_evaluated']))
    return wrapper


def load_with_source(module_name: str) -> ResultCard:
    module = importlib.import_module(module_name)
    dirs = module_name.split('.')
    card_name = f'{dirs[-1]}_card'
    card: ResultCard = module.__getattribute__(card_name)
    card.source = '/'.join(dirs) + '.py'
    return card
