from nlp.pattern.util import ENTRY, is_expr, is_symbol

entries: list[ENTRY] = [
    (R'integrate \expr (for|with respect to) \expr', 'integrate(($0), ($1))',
     lambda expr, x: is_expr(expr) and is_symbol(x)),
    (R'integrate \expr', 'integrate($0)', is_expr),
]
