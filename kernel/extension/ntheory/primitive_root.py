from sympy import Integer, igcd, is_primitive_root

from extension.util import DICT, format_text, take_int_input
from gamma.result_card import ResultCard


def not_too_big(components: DICT) -> bool:
    n = components['input_evaluated']
    return isinstance(n, Integer) and 2 <= n <= 100


@take_int_input
def primitive_root(n: int) -> str:
    primitive_roots = [i for i in range(1, n) if igcd(i, n) == 1 and is_primitive_root(i, n)]
    if primitive_roots:
        return ', '.join(map(str, primitive_roots))
    return f"{n} doesn't have primitive root"


primitive_root_card = ResultCard('Primitive root modulo n', None, eval_method=primitive_root, applicable=not_too_big,
                                 format_output=format_text, wiki='Primitive_root_modulo_n')
