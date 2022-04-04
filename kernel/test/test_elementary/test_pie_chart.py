import hashlib

import pytest

from api import eval_card

cases = [
    ('2/3', b'xNb\x01\xd0b\x84L\xfd\xf3\xb4\xfb\x88\xf2G\n'),
    ('1.2', b'\x17A6\x9c\x12\x9b\xe0\xda\x9a\x98\xc0\x8e\xa8\xe1\x0f:'),
    ('2.1', b'\x93F\x98\xb4\xa3S\x10Yo\x8aWJ\x9c\xea\xeb\xa4'),
]


@pytest.mark.parametrize('num, expected', cases)
def test_card(num: str, expected: bytes):
    actual = eval_card('pie_chart', num, None, None)['svg']
    assert hashlib.md5(actual.encode()).digest() == expected
