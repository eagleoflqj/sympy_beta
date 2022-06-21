import hashlib

import pytest

from api import eval_card

cases = [
    ('x + y', b'\xffRz\t%\xc9{\xcf\x10q\xf4\xce\xd5\xa1HX'),
]


@pytest.mark.parametrize('func, expected', cases)
def test_card(func: str, expected: bytes):
    actual = eval_card('plot_contour', func, None, None)['svg']
    assert hashlib.md5(actual.encode()).digest() == expected
