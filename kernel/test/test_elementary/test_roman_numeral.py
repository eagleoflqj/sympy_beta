import pytest

from api import eval_card

card_cases = [
    (1568, 'MDLXVIII'),
    (2470, 'MMCDLXX'),
    (3999, 'MMMCMXCIX'),
]


@pytest.mark.parametrize('n, expected', card_cases)
def test_card(n: int, expected: str):
    actual = eval_card('roman_numeral', str(n), None, None)['tex']
    assert actual == R'\mathrm{' + expected + '}'
