from api import eval_card


def test():
    assert eval_card('binary_form', '1231', None, None)['tex'] == '10011001111_2'
