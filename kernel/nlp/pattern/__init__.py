from .calculus import entries as calculus_entries
from .ntheory import entries as ntheory_entries
from .util import ENTRY

entries: list[ENTRY] = ntheory_entries \
    + calculus_entries
