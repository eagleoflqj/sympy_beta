from api import eval_card


def test():
    assert eval_card('quadratic_residue', '7', None, None) == {'type': 'Text', 'text': '0, 1, 2, 4'}
