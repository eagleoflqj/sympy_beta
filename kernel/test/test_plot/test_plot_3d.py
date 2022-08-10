import hashlib

import pytest

from api import eval_card

cases = [
    ('x + y', b'\x8c{d\xb7\xfb\xe3\xd7\xf76J\xcc\xf2`\xe7W\x1c'),
]


@pytest.mark.parametrize('func, expected', cases)
def test_card(func: str, expected: bytes):
    actual = eval_card('plot_3d', func, None, None)['svg']
    assert hashlib.md5(actual.encode()).digest() == expected
