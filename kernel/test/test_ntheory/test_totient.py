import pytest

from gamma.logic import SymPyGamma

card_cases = [
    (1, R'1\text{ is coprime to itself}'),
    (2, R'2\text{ is prime}\\\\\\'
        R'\text{For }\text{prime }p\text{, we have }\phi(p^n) = (p-1) \cdot p^{n-1}\text{, so }\\\\\\'
        R'\phi(2^{1}) = (2 - 1) \cdot 2^{1 - 1} = 1\\\\\\'
        R'\text{As a result, }\phi(2) = 1'),
    (4, R'4 = 2^{2}\\\\\\'
        R'\text{For }\text{prime }p\text{, we have }\phi(p^n) = (p-1) \cdot p^{n-1}\text{, so }\\\\\\'
        R'\phi(2^{2}) = (2 - 1) \cdot 2^{2 - 1} = 2\\\\\\'
        R'\text{As a result, }\phi(4) = 2'),
    (6, R'6 = 2^{1} \cdot 3^{1}\\\\\\'
        R'\text{For }(a,b)=1\text{, we have }\phi(a \cdot b) = \phi(a) \cdot \phi(b)\text{, '
        R'so }\phi(6) = \phi(2^{1})\cdot\phi(3^{1})\\\\\\'
        R'\text{For }\text{prime }p\text{, we have }\phi(p^n) = (p-1) \cdot p^{n-1}\text{, so }\\\\\\'
        R'\phi(2^{1}) = (2 - 1) \cdot 2^{1 - 1} = 1\\\\\\'
        R'\phi(3^{1}) = (3 - 1) \cdot 3^{1 - 1} = 2\\\\\\'
        R'\text{As a result, }\phi(6) = 2'),
]


@pytest.mark.parametrize('n, expected', card_cases)
def test_card(n: int, expected: str):
    g = SymPyGamma(f'totient({n})', None)
    actual = g.eval_card('totient', None)['tex']
    assert actual == expected
