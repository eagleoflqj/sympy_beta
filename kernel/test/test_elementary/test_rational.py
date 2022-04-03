from api import eval_card


def test():
    assert eval_card('rational', '2.1', None, None) == {'type': 'Tex', 'tex': R'\frac{21}{10}'}
