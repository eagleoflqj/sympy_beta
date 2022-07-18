from typing import Callable

import sympy

ENTRY = tuple[str, str, Callable | None]


def is_integer(n):
    return n.is_Integer


def is_non_zero_integer(n):
    return n.is_Integer and n != 0


def is_expr(expr):
    return isinstance(expr, sympy.Expr)


def is_symbol(expr):
    return expr.is_Symbol


def expr_and_symbol(expr, x):
    return is_expr(expr) and is_symbol(x)
