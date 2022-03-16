from typing import Any, Callable

from gamma.dispatch import DICT


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


def format_latex(tex: str, formatter=None):
    return {
        'type': 'Tex',
        'tex': tex
    }


def take_int_input(inner: Callable[[int], str]) -> Callable[[DICT, Any], str]:
    def wrapper(components: DICT, parameters: None) -> str:
        return inner(int(components['input_evaluated']))
    return wrapper
