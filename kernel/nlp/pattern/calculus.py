from nlp.pattern.util import ENTRY, expr_and_symbol, is_expr

entries: list[ENTRY] = [
    (R'(derivative|differentiation) of \expr with respect to \expr', 'diff(($0), ($1))', expr_and_symbol),
    (R'(derivative|differentiation) of \expr', 'diff($0)', is_expr),
    (R'integrate \expr (for|with respect to) \expr', 'integrate(($0), ($1))', expr_and_symbol),
    (R'integrate \expr', 'integrate($0)', is_expr),
]
