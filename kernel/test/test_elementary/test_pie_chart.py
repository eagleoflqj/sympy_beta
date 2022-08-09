import hashlib

import pytest

from api import eval_card

cases = [
    ('2/3', b'(\x9c\x17\xba\xaf\xca\xd6\xbezA\xd6\x87\xd9\xa2\xe6\x89'),
    ('1.2', b'3+\xa8>\xe2\xd6\xd1\x84C\xd07\xb2\x18\x9e\x07\x7f'),
    ('2.1', b'h0\xc6\xe0<\x8e\xb8\xd1\xceaT\xda\xbe\xac\xfb\xf5'),
]


@pytest.mark.parametrize('num, expected', cases)
def test_card(num: str, expected: bytes):
    actual = eval_card('pie_chart', num, None, None)['svg']
    assert hashlib.md5(actual.encode()).digest() == expected
