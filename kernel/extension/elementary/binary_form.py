import numpy as np
from sympy import Integer

from extension.util import format_latex, take_int_input
from gamma.dispatch import DICT
from gamma.result_card import ResultCard


def not_too_big(components: DICT) -> bool:
    n = components['input_evaluated']
    return isinstance(n, Integer) and 0 <= n <= np.iinfo(np.uint64).max


@take_int_input
def binary_form(n: int) -> str:
    return np.base_repr(n) + '_2'


binary_form_card = ResultCard("Binary form", "np.base_repr(%s)", eval_method=binary_form,
                              format_output=format_latex, applicable=not_too_big)
