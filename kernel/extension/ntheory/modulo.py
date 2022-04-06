from api.data_type import Table
from extension.util import take_int_input
from gamma.result_card import ResultCard


@take_int_input
def modulo(n: int) -> tuple[int, list[int]]:
    return n, [n % i for i in range(2, 10)]


def format_output(output: tuple[int, list[int]]):
    return Table(titles=['m'] + list(map(str, range(2, 10))),
                 rows=[[f'{output[0]} mod m'] + [str(i) for i in output[1]]])


modulo_card = ResultCard('Modulo 2 to 9', None, eval_method=modulo, format_output=format_output,
                         wiki='Modulo_operation')
