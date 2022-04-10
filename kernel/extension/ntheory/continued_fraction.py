from sympy import Integer, continued_fraction, continued_fraction_iterator, sympify

from api.data_type import ContinuedFraction
from gamma.dispatch import DICT
from gamma.result_card import ResultCard


def not_integer(components: DICT) -> bool:
    return not isinstance(components['input_evaluated'], Integer)


def continued_frac(components: DICT, parameters=None) -> tuple[int, list[int], list[int] | None]:
    num = sympify(components['expression'], rational=True)
    try:
        res: list = continued_fraction(num)
        if isinstance(res[0], list):
            n = res[0][0]
            res = [n] + [res[0][1:] + [n]]
        n = int(res[0])
        if isinstance(res[-1], list):  # periodic
            finite = list(map(int, res[1:-1]))
            repeated = list(map(int, res[-1]))
        else:  # rational
            finite = list(map(int, res[1:]))
            repeated = []
    except ValueError:  # non-periodic irrational
        iterator = continued_fraction_iterator(num)
        n = int(next(iterator))
        finite = [int(next(iterator)) for _ in range(9)]
        repeated = None
    return n, finite, repeated


def format_output(output: tuple[int, list[int], list[int] | None]):
    n, finite, repeated = output
    return ContinuedFraction(n=n, finite=finite, repeated=repeated)


continued_fraction_card = ResultCard('Continued fraction', None, eval_method=continued_frac, applicable=not_integer,
                                     format_output=format_output, wiki='Continued_fraction')
