import pytest

from api import eval_card
from extension.elementary.chinese_numeral import MAX

cases = [
    (0, '〇', '零'),
    (11, '十一', '壹拾壹'),
    (20, '二十', '贰拾'),
    (34, '三十四', '叁拾肆'),
    (500, '五百', '伍佰'),
    (607, '六百〇七', '陆佰零柒'),
    (891, '八百九十一', '捌佰玖拾壹'),
    (1000, '一千', '壹仟'),
    (1012, '一千〇一十二', '壹仟零壹拾贰'),
    (10000, '一万', '壹萬'),
    (10357, '一万〇三百五十七', '壹萬零叁佰伍拾柒'),
    (100000000, '一亿', '壹億'),
    (102304567, '一亿〇二百三十万四千五百六十七', '壹億零贰佰叁拾萬肆仟伍佰陆拾柒'),
    (
        MAX,
        '九千九百九十九万九千九百九十九亿九千九百九十九万九千九百九十九',
        '玖仟玖佰玖拾玖萬玖仟玖佰玖拾玖億玖仟玖佰玖拾玖萬玖仟玖佰玖拾玖'
    )
]


@pytest.mark.parametrize('n, expected_normal, expected_financial', cases)
def test_card(n: int, expected_normal: str, expected_financial: str):
    actual = eval_card('chinese_numeral', str(n), None, None)
    assert actual['normal'] == expected_normal
    assert actual['financial'] == expected_financial
