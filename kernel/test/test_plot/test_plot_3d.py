import hashlib

import pytest

from api import eval_card

cases = [
    ('x + y', b'\x91\xd7\xe0\xc2\xb6+{\x12\xe0[\xe6\xd4\x89\xee\xbb\xd5'),
]


@pytest.mark.parametrize('func, expected', cases)
def test_card(func: str, expected: bytes):
    actual = eval_card('plot_3d', func, None, None)['svg']
    assert hashlib.md5(actual.encode()).digest() == expected
