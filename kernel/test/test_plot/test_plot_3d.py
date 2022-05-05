import hashlib

import pytest

from api import eval_card

cases = [
    ('x + y', b"\x16J\xeb#R-\xf7\x0b\x97$'\x08\x0e7\x8e\x1c"),
]


@pytest.mark.parametrize('func, expected', cases)
def test_card(func: str, expected: bytes):
    actual = eval_card('plot_3d', func, None, None)['svg']
    assert hashlib.md5(actual.encode()).digest() == expected
