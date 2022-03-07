from sympy import Eq, latex


def t(text: str) -> str:
    return R'\text{' + text + '}'


class Latex:
    def __init__(self):
        self.buffer: list[str] = []

    def a(self, *args):  # append
        for arg in args:
            self.buffer.append(str(arg))

    def n(self):  # new line
        self.a(r'\\\\\\')

    def eq(self, lhs, rhs):
        eq = Eq(lhs, rhs, evaluate=False)
        self.a(latex(eq))

    def for_we_have_so(self, conditions: list[str], conclusions: list[str], results: list[str]):
        self.a(t('For '), ', '.join(conditions),
               t(', we have '), ', '.join(conclusions),
               t(', so ') + ', '.join(results))
        self.n()

    def as_a_result(self, conclusions: list[str]):
        self.a(t('As a result, '), ', '.join(conclusions))

    def f(self):  # finish
        return ''.join(self.buffer)


def format_latex(tex: str, formatter=None):
    return {
        'type': 'Tex',
        'tex': tex
    }
