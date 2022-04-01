from sympy import Integer, quadratic_residues

from extension.util import format_text, take_int_input
from gamma.dispatch import DICT
from gamma.result_card import ResultCard


def not_too_big(components: DICT) -> bool:
    n = components['input_evaluated']
    return isinstance(n, Integer) and 2 <= n <= 100


@take_int_input
def quadratic_residue(n: int) -> str:
    return ', '.join(map(str, quadratic_residues(n)))


quadratic_residue_card = ResultCard('Quadratic residue', None, eval_method=quadratic_residue, applicable=not_too_big,
                                    format_output=format_text, wiki='Quadratic_residue')
