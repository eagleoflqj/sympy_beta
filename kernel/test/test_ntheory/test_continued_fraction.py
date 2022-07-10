import pytest

from api import eval_card

cases = [
    ('1.2', (1, [5], [])),
    ('sqrt(2)', (1, [], [2])),
    ('1+sqrt(3)', (2, [], [1, 2])),
    ('pi', (3, [7, 15, 1, 292, 1, 1, 1, 2, 1], None)),
    ('e', (2, [1, 2, 1, 1, 4, 1, 1, 6, 1], None)),
]


@pytest.mark.parametrize('num, expected', cases)
def test(num: str, expected: tuple[int, list[int], list[int] | None]):
    n, finite, repeated = expected
    actual = eval_card('continued_fraction', num, None, None)
    assert actual['n'] == n
    assert actual['finite'] == finite
    assert actual['repeated'] == repeated
