import abc
import re
from contextlib import contextmanager

import sympy

from gamma.utils import DerivExpr, latex


def functionnames(numterms):
    if numterms == 2:
        return ["f", "g"]
    elif numterms == 3:
        return ["f", "g", "h"]
    else:
        return ["f_{}".format(i) for i in range(numterms)]


def replace_u_var(rule, old_u: sympy.Symbol, new_u: sympy.Symbol):
    d = rule._asdict()
    for field, val in d.items():
        if isinstance(val, sympy.Basic):
            d[field] = val.subs(old_u, new_u)
        elif isinstance(val, tuple):
            d[field] = replace_u_var(val, old_u, new_u)
        elif isinstance(val, list):
            result = []
            for item in val:
                if type(item) is tuple:
                    result.append((replace_u_var(item[0], old_u, new_u), item[1]))
                elif isinstance(item, tuple):
                    result.append(replace_u_var(item, old_u, new_u))
                else:
                    result.append(item)
            d[field] = result
    return rule.__class__(**d)


u_index_re = re.compile(r'^u_?([1-9]\d*|0)$')


def u_index(symbol: sympy.Symbol) -> int:
    if symbol.name == 'u':
        return 0
    match = u_index_re.match(symbol.name)
    if match:
        return int(match.group(1))
    return -1


class JSONPrinter:
    def __init__(self, rule):
        self.alternative_functions_printed = set()
        self.rule = rule
        self.stack = []
        # avoid duplicated symbol u when doing substitution
        self.u_max = max((u_index(symbol) for symbol in rule.context.free_symbols), default=-1)
        self.print_rule(rule)

    @abc.abstractmethod
    def print_rule(self, rule):
        pass

    def format_text(self, text):
        return {'text': text}

    def format_math(self, math):
        if not isinstance(math, str):
            math = latex(math)
        return {'inline': math}

    def format_math_display(self, math):
        if not isinstance(math, str):
            math = latex(math)
        return {'block': math}

    @contextmanager
    def new_level(self):
        index = len(self.stack)
        yield
        self.stack, body = self.stack[:index], self.stack[index:]
        self.stack.append({'level': body})

    @contextmanager
    def new_step(self):
        index = len(self.stack)
        yield
        self.stack, body = self.stack[:index], self.stack[index:]
        self.stack.append({'step': body})

    @contextmanager
    def new_collapsible(self):
        index = len(self.stack)
        yield
        self.stack, body = self.stack[:index], self.stack[index:]
        self.stack.append({'collapsible': body})

    @contextmanager
    def new_u_vars(self):
        self.u_max += 1
        if self.u_max == 0:
            u = 'u'
        else:
            u = f'u_{self.u_max}'
        yield sympy.Symbol(u), DerivExpr(u)
        self.u_max -= 1

    def append(self, *contents):
        self.stack.append({'p': contents})

    def append_header(self, text):
        self.stack.append({'header': text})
