import re
from typing import cast

from nlp.dispatcher import dispatch
from nlp.parser import parse


def translate(nl: str) -> str:
    nl = cast(re.Match, re.fullmatch(r'(.*?)[\s.?]*', nl)).group(1)  # remove trailing .?
    terms = nl.split()  # remove extra space
    entry = dispatch(terms)
    if entry is None:
        raise SyntaxError
    result = parse(entry, ' '.join(terms))
    if result is None:
        raise ValueError
    return result
