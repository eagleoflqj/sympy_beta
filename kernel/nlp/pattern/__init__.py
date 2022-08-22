import re

from .algebra import entries as algebra_entries
from .calculus import entries as calculus_entries
from .ntheory import entries as ntheory_entries
from .util import ENTRY


def expand(entry: ENTRY) -> list[ENTRY]:
    pattern, target, applicable = entry
    match = re.search(r'\((.*?)\)', pattern)
    if match:
        branches = match.group(1).split('|')
        start, end = match.span()
        head, tail = pattern[:start], pattern[end:]
        return [expanded_entry for branch in branches
                for expanded_entry in expand((head + branch + tail, target, applicable))]
    return [entry]


entries: list[ENTRY] = [expanded_entry for entries in (
    ntheory_entries,
    algebra_entries,
    calculus_entries
) for entry in entries for expanded_entry in expand(entry)]
