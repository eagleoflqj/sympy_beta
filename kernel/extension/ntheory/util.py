from sympy import Integer, Pow, latex

from extension.util import DICT


def is_positive_integer(components: DICT) -> bool:
    n = components['input_evaluated']
    return isinstance(n, Integer) and n > 0


def pow_list_from_factor_dict(factor_dict: dict[Integer, Integer]) -> list[Pow]:
    return [Pow(b, e, evaluate=False) for b, e in factor_dict.items()]


def is_prime_from_factor_dict(factor_dict: dict[Integer, Integer]) -> bool:
    return len(factor_dict) == 1 and all(e == 1 for _, e in factor_dict.items())


def cross_mul(*args) -> str:
    return R'\times'.join(latex(arg) for arg in args)
