from sympy import Integer

from api.data_type import ChineseNumeral
from extension.util import take_int_input
from gamma.dispatch import DICT
from gamma.result_card import FakeResultCard

normal_chars = ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
normal_units = ['百', '千', '万', '亿']
financial_chars = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖', '拾']
financial_units = ['佰', '仟', '萬', '億']

MAX = 9999999999999999


def not_too_big(components: DICT) -> bool:
    n = components['input_evaluated']
    return isinstance(n, Integer) and 0 <= n <= MAX


def int_to_normal(n: int) -> str:
    def tens(t: int) -> str:
        return normal_chars[1] if 10 <= t <= 19 else ''

    if n <= 10:
        return normal_chars[n]
    if n <= 19:
        return normal_chars[10] + normal_chars[n - 10]
    if n <= 99:
        shi, ge = divmod(n, 10)
        return normal_chars[shi] + normal_chars[10] + (normal_chars[ge] if ge else '')
    if n <= 999:
        bai, shis = divmod(n, 100)
        leading = normal_chars[bai] + normal_units[0]
        if shis == 0:
            return leading
        if shis <= 9:
            leading += normal_chars[0]
        else:
            leading += tens(shis)
        return leading + int_to_normal(shis)
    if n <= 9999:
        qian, bais = divmod(n, 1000)
        lead = normal_chars[qian] + normal_units[1]
        if bais == 0:
            return lead
        if bais <= 99:
            lead += normal_chars[0]
            lead += tens(bais)
        return lead + int_to_normal(bais)
    if n <= 99999999:
        wan, qians = divmod(n, 10000)
        lead = int_to_normal(wan) + normal_units[2]
        if qians == 0:
            return lead
        if qians <= 999:
            lead += normal_chars[0]
            lead += tens(qians)
        return lead + int_to_normal(qians)
    yi, wans = divmod(n, 100000000)
    lead = int_to_normal(yi) + normal_units[3]
    if wans == 0:
        return lead
    if wans <= 9999999:
        lead += normal_chars[0]
        lead += tens(wans // 10000)
    return lead + int_to_normal(wans)


@take_int_input
def int_to_chinese_numeral(n: int) -> tuple[str, str]:
    normal = int_to_normal(n)
    financial = financial_chars[1] if normal[0] == normal_chars[10] else ''
    for c in normal:
        financial += financial_units[normal_units.index(c)] if c in normal_units \
            else financial_chars[normal_chars.index(c)]
    return normal, financial


def format_output(output: tuple[str, str], parameters: None):
    return ChineseNumeral(normal=output[0], financial=output[1])


chinese_numeral_card = FakeResultCard("Chinese numeral", None, None, eval_method=int_to_chinese_numeral,
                                      format_output=format_output, applicable=not_too_big)
