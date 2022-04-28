import ast
import re
from typing import cast

import sympy
from sympy.core.relational import Relational

from api.data_type import Tex
from gamma.evaluator import eval_node

OTHER_SYMPY_FUNCTIONS = ('sqrt',)


class LatexVisitor(ast.NodeVisitor):
    EXCEPTIONS = {'integrate': sympy.Integral, 'diff': sympy.Derivative}
    formatters = {}

    @staticmethod
    def formats_function(name):
        def _formats_function(f):
            LatexVisitor.formatters[name] = f
            return f
        return _formats_function

    def format(self, name, node):
        formatter = LatexVisitor.formatters.get(name)

        if not formatter:
            return None

        return formatter(node)

    def visit_Call(self, node):
        buffer = []
        func = cast(ast.Name, node.func)
        fname = func.id

        # Only apply to lowercase names (i.e. functions, not classes)
        if fname in self.__class__.EXCEPTIONS:
            func.id = self.__class__.EXCEPTIONS[fname].__name__
            self.latex = sympy.latex(eval_node(node))
        else:
            result = self.format(fname, node)
            if result:
                self.latex = result
            elif fname[0].islower() and fname not in OTHER_SYMPY_FUNCTIONS:
                buffer.append("\\mathrm{%s}" % fname.replace('_', '\\_'))
                buffer.append('(')

                latexes = []
                for arg in node.args:
                    if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and arg.func.id[0].islower():
                        latexes.append(self.visit_Call(arg))
                    else:
                        latexes.append(sympy.latex(eval_node(arg)))

                buffer.append(', '.join(latexes))
                buffer.append(')')

                self.latex = ''.join(buffer)
            else:
                self.latex = sympy.latex(eval_node(node))
        return self.latex


@LatexVisitor.formats_function('solve')
def format_solve(node):
    expr = eval_node(node.args[0])
    buffer = [r'\mathrm{solve}\;', sympy.latex(expr)]

    if not isinstance(expr, Relational):
        buffer.append('=0')

    if len(node.args) > 1:
        buffer.append(r'\;\mathrm{for}\;')
    for arg in node.args[1:]:
        buffer.append(sympy.latex(eval_node(arg)))
        buffer.append(r',\, ')
    if len(node.args) > 1:
        buffer.pop()

    return ''.join(buffer)


@LatexVisitor.formats_function('limit')
def format_limit(node):
    if len(node.args) >= 3:
        return sympy.latex(
            sympy.Limit(*[eval_node(arg) for arg in node.args]))


@LatexVisitor.formats_function('prime')
def format_prime(node):
    number = sympy.latex(eval_node(node.args[0]))
    return ''.join([number,
                    r'^\mathrm{',
                    ordinal(int(number)),
                    r'}\; \mathrm{prime~number}'])


@LatexVisitor.formats_function('isprime')
def format_isprime(node):
    number = sympy.latex(eval_node(node.args[0]))
    return ''.join([r'\mathrm{Is~}', number, r'\mathrm{~prime?}'])


@LatexVisitor.formats_function('nextprime')
def format_nextprime(node):
    number = sympy.latex(eval_node(node.args[0]))
    return r'\mathrm{Least~prime~greater~than~}' + number


@LatexVisitor.formats_function('factorint')
def format_factorint(node):
    number = sympy.latex(eval_node(node.args[0]))
    return r'\mathrm{Prime~factorization~of~}' + number


@LatexVisitor.formats_function('factor')
def format_factor(node):
    expression = sympy.latex(eval_node(node.args[0]))
    return r'\mathrm{Factorization~of~}' + expression


@LatexVisitor.formats_function('solve_poly_system')
def format_solve_poly_system(node):
    equations = eval_node(node.args[0])
    variables = tuple(map(eval_node, node.args[1:]))

    if len(variables) == 1:
        variables = variables[0]

    return ''.join([r'\mathrm{Solve~} \begin{cases} ',
                    r'\\'.join(map(sympy.latex, equations)),
                    r'\end{cases} \mathrm{~for~}',
                    sympy.latex(variables)])


@LatexVisitor.formats_function('plot')
def format_plot(node):
    if node.args:
        function = sympy.latex(eval_node(node.args[0]))
    else:
        keywords = {}
        for keyword in node.keywords:
            keywords[keyword.arg] = eval_node(keyword.value)
        function = sympy.latex(keywords)
    return r'\mathrm{Plot~}' + function


@LatexVisitor.formats_function('rsolve')
def format_rsolve(node):
    recurrence = sympy.latex(sympy.Eq(eval_node(node.args[0]), 0, evaluate=False))
    if len(node.args) == 3:
        conds = eval_node(node.args[2])
        initconds = '\\\\\n'.join('&' + sympy.latex(sympy.Eq(eqn, val, evaluate=False)) for eqn, val in conds.items())
        text = r'&\mathrm{Solve~the~recurrence~}' + recurrence + r'\\'
        condstext = r'&\mathrm{with~initial~conditions}\\'
        return r'\begin{align}' + text + condstext + initconds + r'\end{align}'
    else:
        return r'\mathrm{Solve~the~recurrence~}' + recurrence


diophantine_template = (r"\begin{{align}}&{}\\&\mathrm{{where~}}"
                        r"{}\mathrm{{~are~integers}}\end{{align}}")


@LatexVisitor.formats_function('diophantine')
def format_diophantine(node):
    expression = eval_node(node.args[0])
    symbols = None
    if isinstance(expression, sympy.Basic):
        symbols = sorted(expression.free_symbols, key=str)
    equation = sympy.latex(sympy.Eq(expression, 0, evaluate=False))

    result = r'\mathrm{Solve~the~diophantine~equation~}' + equation
    if symbols:
        result = diophantine_template.format(result, tuple(symbols))
    return result


@LatexVisitor.formats_function('summation')
@LatexVisitor.formats_function('product')
def format_sum_product(node):
    if node.func.id == 'summation':
        klass = sympy.Sum
    else:
        klass = sympy.Product
    return sympy.latex(klass(*list(map(eval_node, node.args))))


@LatexVisitor.formats_function('help')
def format_help(node):
    if node.args:
        function = eval_node(node.args[0])
        return r'\mathrm{Show~documentation~for~}' + function.__name__
    return r'\mathrm{Show~documentation~(requires~1~argument)}'


# From https://stackoverflow.com/a/739301/262727
def ordinal(n):
    if 10 <= n % 100 < 20:
        return 'th'
    else:
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, "th")


# TODO: modularize all of this
def latexify(node):
    a = LatexVisitor()
    a.visit(node)
    return a.latex


re_calls = re.compile(r'(Integer|Symbol|Float|Rational)\s*\([\'\"]?([a-zA-Z0-9\.]+)[\'\"]?\s*\)')


def re_calls_sub(match):
    return match.groups()[1]


def removeSymPy(string):
    try:
        return re_calls.sub(re_calls_sub, string).replace(" ", "")
    except IndexError:
        return string


def latex(expr: sympy.Basic | str | int) -> str:
    # sympy.latex('') == '\\mathtt{\\text{}}'
    if expr == '':
        return ''
    if isinstance(expr, sympy.Basic):
        # solveset(sin(x)) click More Digits
        expr = expr.replace(sympy.Symbol('_n'), sympy.Dummy('n'))  # type: ignore
    return sympy.latex(expr, ln_notation=True)


def is_approximatable_constant(input_evaluated):
    # is_constant, but exclude Integer/Float/infinity
    return isinstance(input_evaluated, sympy.Expr) and not input_evaluated.free_symbols \
           and not input_evaluated.is_Integer and not input_evaluated.is_Float \
           and input_evaluated.is_finite  # type: ignore


def mathjax_latex(*args, digits: int | None = 15):
    tex_code = []
    for obj in args:
        if hasattr(obj, 'as_latex'):
            tex_code.append(obj.as_latex())
        else:
            tex_code.append(latex(obj))

    result = Tex(tex=''.join(tex_code))
    if digits is not None and len(args) == 1:
        obj = args[0]
        if is_approximatable_constant(obj):
            result['numeric'] = True
            result['expression'] = repr(obj)
            result['approximation'] = latex(obj.evalf(digits))
    return result
