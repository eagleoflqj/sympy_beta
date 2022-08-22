import re
from typing import cast

from nlp.dispatcher import dispatch
from nlp.parser import parse


def translate(nl: str) -> str:
    nl = cast(re.Match, re.fullmatch(r'(.*?)[\s.?]*', nl)).group(1)  # remove trailing .?
    terms = nl.split()  # remove extra space
    entries = dispatch(terms)
    if not entries:
        raise SyntaxError
    for entry in entries:
        result = parse(entry, ' '.join(terms))
        if result:
            return result
    raise ValueError
