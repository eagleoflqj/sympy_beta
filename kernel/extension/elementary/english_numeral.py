# License: GPL-3.0-or-later
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.
# Copyright (c) 2022, Qijia Liu

from collections import OrderedDict
from typing import Union

from sympy import Integer

from extension.util import DICT, format_text, take_int_input
from gamma.result_card import ResultCard

TEMP = list[Union[tuple[str, int], 'TEMP']]


class Num2Word:
    def __init__(self):
        lows = ["non", "oct", "sept", "sext", "quint", "quadr", "tr", "b", "m"]
        units = ["", "un", "duo", "tre", "quattuor", "quin", "sex", "sept", "octo", "novem"]
        tens = ["dec", "vigint", "trigint", "quadragint", "quinquagint",
                "sexagint", "septuagint", "octogint", "nonagint"]
        self.high_numwords = ["cent"] + self.gen_high_numwords(units, tens, lows)
        self.mid_numwords = [(1000, "thousand"), (100, "hundred"), (90, "ninety"), (80, "eighty"), (70, "seventy"),
                             (60, "sixty"), (50, "fifty"), (40, "forty"), (30, "thirty")]
        self.low_numwords = ["twenty", "nineteen", "eighteen", "seventeen", "sixteen", "fifteen", "fourteen",
                             "thirteen", "twelve", "eleven", "ten", "nine", "eight", "seven", "six", "five", "four",
                             "three", "two", "one", "zero"]
        self.cards: OrderedDict[int, str] = OrderedDict()
        self.set_numwords()
        self.MAXVAL = 1000 * list(self.cards.keys())[0]

    @staticmethod
    def gen_high_numwords(units: list[str], tens: list[str], lows: list[str]):
        out = [u + t for t in tens for u in units]
        out.reverse()
        return out + lows

    def set_numwords(self):
        self.set_high_numwords(self.high_numwords)
        self.set_mid_numwords(self.mid_numwords)
        self.set_low_numwords(self.low_numwords)

    def set_high_numwords(self, high: list[str]):
        max = 3 + 3 * len(high)
        for word, n in zip(high, range(max, 3, -3)):
            self.cards[10 ** n] = word + "illion"

    def set_mid_numwords(self, mid: list[tuple[int, str]]):
        for key, val in mid:
            self.cards[key] = val

    def set_low_numwords(self, numwords: list[str]):
        for word, n in zip(numwords, range(len(numwords) - 1, -1, -1)):
            self.cards[n] = word

    def splitnum(self, value: int) -> TEMP:
        elem = next(e for e in self.cards if e <= value)

        out: TEMP = []
        if value == 0:
            div, mod = 1, 0
        else:
            div, mod = divmod(value, elem)

        if div == 1:
            out.append((self.cards[1], 1))
        else:
            out.append(self.splitnum(div))

        out.append((self.cards[elem], elem))

        if mod:
            out.append(self.splitnum(mod))

        return out

    def to_cardinal(self, value: int) -> str:
        val = self.splitnum(value)
        words, num = self.clean(val)
        return words

    def merge(self, lpair: tuple[str, int], rpair: tuple[str, int]) -> tuple[str, int]:
        ltext, lnum = lpair
        rtext, rnum = rpair
        if lnum == 1 and rnum < 100:
            return rtext, rnum
        elif 100 > lnum > rnum:
            return "%s-%s" % (ltext, rtext), lnum + rnum
        elif lnum >= 100 > rnum:
            return "%s and %s" % (ltext, rtext), lnum + rnum
        elif rnum > lnum:
            return "%s %s" % (ltext, rtext), lnum * rnum
        return "%s, %s" % (ltext, rtext), lnum + rnum

    def clean(self, val: TEMP) -> tuple[str, int]:
        out = val
        while len(val) != 1:
            out = []
            left, right = val[:2]
            if isinstance(left, tuple) and isinstance(right, tuple):
                out.append(self.merge(left, right))
                if val[2:]:
                    out.append(val[2:])
            else:
                for elem in val:
                    if isinstance(elem, list):
                        if len(elem) == 1:
                            out.append(elem[0])
                        else:
                            out.append(self.clean(elem))
                    else:
                        out.append(elem)
            val = out
        return out[0]  # type: ignore


en = Num2Word()


def not_too_big(components: DICT) -> bool:
    n = components['input_evaluated']
    return isinstance(n, Integer) and 0 <= n < en.MAXVAL


@take_int_input
def int_to_english_numeral(n: int) -> str:
    return en.to_cardinal(n)


english_numeral_card = ResultCard("English numeral", None, eval_method=int_to_english_numeral, wiki='English_numerals',
                                  format_output=format_text, applicable=not_too_big)
