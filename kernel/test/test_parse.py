import pytest

from api import SymPyGamma

cases = [
    ('(x*f(x))', "(Symbol ('x' )*Function ('f' )(Symbol ('x' )))")
]


@pytest.mark.parametrize('expression, expected', cases)
def test(expression: str, expected: str):
    assert SymPyGamma(expression).parsed == expected
