import abc
import collections
from contextlib import contextmanager

import sympy

from gamma.utils import latex


def Rule(name, props=""):
    # GOTCHA: namedtuple class name not considered!
    def __eq__(self, other):
        return self.__class__ == other.__class__ and tuple.__eq__(self, other)

    def __neq__(self, other):
        return not __eq__(self, other)

    cls = collections.namedtuple(name, props + " context symbol")
    cls.__eq__ = __eq__
    cls.__ne__ = __neq__
    return cls


def functionnames(numterms):
    if numterms == 2:
        return ["f", "g"]
    elif numterms == 3:
        return ["f", "g", "h"]
    else:
        return ["f_{}".format(i) for i in range(numterms)]


def replace_u_var(rule, old_u, new_u):
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


class JSONPrinter:
    def __init__(self, rule):
        self.alternative_functions_printed = set()
        self.rule = rule
        self.stack = []
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
        self.u, self.du = sympy.Symbol('u'), sympy.Symbol('du')
        yield self.u, self.du

    def append(self, *contents):
        self.stack.append({'p': contents})

    def append_header(self, text):
        self.stack.append({'header': text})
