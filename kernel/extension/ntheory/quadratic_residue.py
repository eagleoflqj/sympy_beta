from sympy import Integer, quadratic_residues

from api.data_type import Text
from extension.util import take_int_input
from gamma.dispatch import DICT
from gamma.result_card import ResultCard


def not_too_big(components: DICT) -> bool:
    n = components['input_evaluated']
    return isinstance(n, Integer) and 2 <= n <= 100


@take_int_input
def quadratic_residue(n: int) -> list[int]:
    return quadratic_residues(n)


def format_output(output: list[int], parameteres=None):
    return Text(text=', '.join(map(str, output)))


quadratic_residue_card = ResultCard('Quadratic residue', None, eval_method=quadratic_residue, applicable=not_too_big,
                                    format_output=format_output, wiki='Quadratic_residue')
