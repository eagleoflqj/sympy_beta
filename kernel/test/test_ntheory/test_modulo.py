from api import eval_card


def test():
    assert eval_card('modulo', '1231', None, None) == {'type': 'Table',
                                                       'titles': ['m', '2', '3', '4', '5', '6', '7', '8', '9'],
                                                       'rows': [['1231 mod m', '1', '1', '3', '1', '1', '6', '7', '7']]}
