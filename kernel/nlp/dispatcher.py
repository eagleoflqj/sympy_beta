from nlp.pattern import ENTRY, entries

lex_id = 0
lex_id_map: dict[str, int] = {}
rules: list[list[int]] = []

for pattern, target, applicable in entries:
    terms = pattern.split()
    rule = []
    for term in terms:
        if term == R'\expr':
            continue
        _id = lex_id_map.get(term)
        if _id is None:
            _id = lex_id
            lex_id += 1
            lex_id_map[term] = _id
        rule.append(_id)
    rules.append(rule)


def rule_match(rule: list[int], ids: list[int]) -> bool:
    # subsequence matching
    i = -1
    try:
        for _id in rule:
            i = ids.index(_id, i + 1)
    except ValueError:
        return False
    return True


def dispatch(terms: list[str]) -> list[ENTRY]:
    patterns = []
    ids = [lex_id_map.get(term.lower(), -1) for term in terms]
    for rule, pattern in zip(rules, entries):
        if rule_match(rule, ids):
            patterns.append(pattern)
    return patterns
