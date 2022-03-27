from sympy import Integer

from extension.util import format_latex, take_int_input
from gamma.dispatch import DICT
from gamma.result_card import ResultCard

roman_chars = ['I', 'V', 'X', 'L', 'C', 'D', 'M', '', '']


def between_1_and_3999(components: DICT) -> bool:
    n = components['input_evaluated']
    return isinstance(n, Integer) and 1 <= n <= 3999


def helper(digit: int, one: str, five: str, ten: str) -> str:
    if digit == 0:
        return ''
    if digit <= 3:
        return one * digit
    if digit <= 5:
        return one * (5 - digit) + five
    if digit <= 8:
        return five + one * (digit - 5)
    return one + ten


@take_int_input
def int_to_roman_numeral(n: int) -> str:
    i = 0
    ret = ''
    while n:
        n, r = divmod(n, 10)
        ret = helper(r, roman_chars[i], roman_chars[i+1], roman_chars[i + 2]) + ret
        i += 2
    return R'\mathrm{' + ret + '}'


roman_numeral_card = ResultCard("Roman numeral", None, eval_method=int_to_roman_numeral, format_output=format_latex,
                                applicable=between_1_and_3999, wiki='Roman_numerals')
