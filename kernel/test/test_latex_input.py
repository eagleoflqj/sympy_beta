import pytest

from api import eval_latex_input

cases = [
    (R'\frac{1}{3}', '1/3'),
    ('x_1', 'x_1'),
]


@pytest.mark.parametrize('expression, expected', cases)
def test(expression: str, expected: str):
    actual = eval_latex_input(expression)['result']
    assert actual == expected
