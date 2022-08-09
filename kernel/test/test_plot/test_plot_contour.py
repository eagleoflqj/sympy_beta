import hashlib

import pytest

from api import eval_card

cases = [
    ('x + y', b'nr=6wJj9\x05\xa6\xd4O\x9chd\x91'),
]


@pytest.mark.parametrize('func, expected', cases)
def test_card(func: str, expected: bytes):
    actual = eval_card('plot_contour', func, None, None)['svg']
    assert hashlib.md5(actual.encode()).digest() == expected
