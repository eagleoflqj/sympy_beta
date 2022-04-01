import pytest

from api import eval_card

cases = [
    (0, 'zero'),
    (1231628, 'one million, two hundred and thirty-one thousand, six hundred and twenty-eight'),
]


@pytest.mark.parametrize('n, expected', cases)
def test_card(n: int, expected: str):
    actual = eval_card('english_numeral', str(n), None, None)
    assert actual['text'] == expected
