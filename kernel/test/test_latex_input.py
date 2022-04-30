import pytest

from api import eval_input, eval_latex_input

cases = [
    (R'\frac{1}{3}', '1/3'),
    ('x_1', 'x_1'),
]


@pytest.mark.parametrize('expression, expected', cases)
def test(expression: str, expected: str):
    actual = eval_latex_input(expression)['result']
    assert actual == expected


e2e_cases = [
    (R'\int xdx',
     [{'title': 'SymPy', 'input': 'integrate(x,x)',
       'output': {'type': 'Tex', 'tex': '\\int x\\, dx'}},
      {'name': 'integral_alternate_fake', 'title': 'Antiderivative forms', 'variable': 'x', 'pre_output': ''},
      {'name': 'intsteps', 'title': 'Integral Steps', 'input': 'integrate(x, x)', 'variable': 'x'}]),
]


@pytest.mark.parametrize('expression, expected', e2e_cases)
def test_e2e(expression: str, expected: list[dict]):
    python_input = eval_latex_input(expression)['result']
    actual = eval_input(python_input)['result']
    assert actual == expected
