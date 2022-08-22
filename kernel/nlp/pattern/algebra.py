from nlp.pattern.util import ENTRY, is_expr

entries: list[ENTRY] = [
    (R'expand \expr', 'expand($0)', is_expr),
    (R'factorize \expr', 'factor($0)', is_expr),
]
