import re

from gamma.logic import SymPyGamma
from nlp.pattern import ENTRY


def parse(entry: ENTRY, nl: str) -> str | None:
    pattern, template, applicable = entry
    re_pattern = pattern.replace(R'\expr', '(.*)')
    match = re.fullmatch(re_pattern, nl, re.IGNORECASE)
    if match is None:
        return None
    groups = match.groups()
    if len(groups) != template.count('$'):
        return None
    parsed = [SymPyGamma(group).evaluated for group in groups]
    if applicable and not applicable(*parsed):
        return None
    result = template
    for i in range(len(groups)):
        result = result.replace(f'(${i})', f'({groups[i]})')
    return result
