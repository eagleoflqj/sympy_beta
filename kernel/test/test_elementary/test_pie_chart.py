import hashlib

import pytest

from api import eval_card

cases = [
    ('2/3', b'N\xa2\xd6\x10\xcc\xa5\xd5M\x06\xd8\xd27\xa7\x17\xeb1'),
    ('1.2', b"\xfd\x05\xc0\x0c\x9a~88\x83+=-T!('"),
    ('2.1', b'SC\xaaN\xb0U\x13m\xf7\x97\x9c\xce\xcd\x93%\xf4'),
]


@pytest.mark.parametrize('num, expected', cases)
def test_card(num: str, expected: bytes):
    actual = eval_card('pie_chart', num, None, None)['svg']
    assert hashlib.md5(actual.encode()).digest() == expected
