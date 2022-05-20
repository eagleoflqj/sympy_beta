import hashlib

import pytest

from api import eval_card

cases = [
    ('sin(z)', b'[\xb7\xbfav\x98u\xe7U\xe4]\xb1Q\xb1\x15\xc2'),
]


@pytest.mark.parametrize('func, expected', cases)
def test_card(func: str, expected: bytes):
    actual = eval_card('plot_complex', func, None, None)['svg']
    assert hashlib.md5(actual.encode()).digest() == expected
