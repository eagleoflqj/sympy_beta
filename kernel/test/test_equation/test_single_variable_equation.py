import pytest

from api import eval_card

cases = [
    ('x^3+2',
     R'\text{Complex root: }x \in\left\{- \sqrt[3]{2}, '
     R'\frac{\sqrt[3]{2}}{2} - \frac{\sqrt[3]{2} \sqrt{3} i}{2}, '
     R'\frac{\sqrt[3]{2}}{2} + \frac{\sqrt[3]{2} \sqrt{3} i}{2}\right\}'),
    ('Heaviside(x)', R'\text{Real root: }x \in\left(-\infty, 0\right)'),
]


@pytest.mark.parametrize('equation, expected', cases)
def test(equation: str, expected: str):
    actual = eval_card('root', equation, 'x', None)['tex']
    assert actual == expected
