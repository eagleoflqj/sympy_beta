from api import eval_latex_input


def test():
    assert eval_latex_input(R'\frac{1}{3}')['result'] == '1/3'
