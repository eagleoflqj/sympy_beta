import pytest

from api import eval_card

cases = [
    (12, "12 doesn't have primitive root"),
    (43, '3, 5, 12, 18, 19, 20, 26, 28, 29, 30, 33, 34'),
]


@pytest.mark.parametrize('n, expected', cases)
def test(n: int, expected: str):
    actual = eval_card('primitive_root', str(n), None, None)['text']
    assert actual == expected
