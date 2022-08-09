import hashlib

import pytest

from api import eval_card

cases = [
    ('sin(z)', b'/Hlf\xe7\xda.@\xef \xca\xaag\xf6\xd7\xa4'),
]


@pytest.mark.parametrize('func, expected', cases)
def test_card(func: str, expected: bytes):
    actual = eval_card('plot_complex', func, None, None)['svg']
    assert hashlib.md5(actual.encode()).digest() == expected
