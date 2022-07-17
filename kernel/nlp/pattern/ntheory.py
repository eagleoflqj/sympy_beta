from nlp.pattern.util import ENTRY, is_integer, is_non_zero_integer

entries: list[ENTRY] = [
    (R'is \expr even', '($0).is_even', is_integer),
    (R'is \expr odd', '($0).is_odd', is_integer),
    (R'is \expr a prime number', 'isprime($0)', is_integer),
    (R'is \expr prime', 'isprime($0)', is_integer),
    (R'is \expr a multiple of \expr', '($0) % ($1) == 0', lambda a, b: is_integer(a) and is_non_zero_integer(b)),
]
