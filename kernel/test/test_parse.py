import pytest

from api import SymPyGamma

cases = [
    ('(x*f(x))', "(Symbol ('x' )*Function ('f' )(Symbol ('x' )))"),
    ('e', 'E '),
    ('a+b+c+d+e', "Symbol ('a' )+Symbol ('b' )+Symbol ('c' )+Symbol ('d' )+Symbol ('e' )"),
    ('i', 'I '),
]


@pytest.mark.parametrize('expression, expected', cases)
def test(expression: str, expected: str):
    assert SymPyGamma(expression).parsed == expected
