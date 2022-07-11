import pytest

from api import SymPyGamma

cases = [
    ('(x*f(x))', "(Symbol ('x' )*Function ('f' )(Symbol ('x' )))"),
    ('e', 'E '),
    ('a+b+c+d+e', "Symbol ('a' )+Symbol ('b' )+Symbol ('c' )+Symbol ('d' )+Symbol ('e' )"),
    ('i', 'I '),
    ('Beta(1, 1)', 'beta (Integer (1 ),Integer (1 ))'),
    ('Gamma(1)', 'gamma (Integer (1 ))'),
    ('delta(1)', 'DiracDelta (Integer (1 ))'),
    ('theta(1)', 'Heaviside (Integer (1 ))'),
]


@pytest.mark.parametrize('expression, expected', cases)
def test(expression: str, expected: str):
    assert SymPyGamma(expression).parsed == expected
