import pytest

from gamma.logic import SymPyGamma

cases = [
    ('242/33',
     [{'title': 'SymPy', 'input': '242/33',
       'output': {'type': 'Tex', 'tex': '\\frac{22}{3}', 'numeric': True, 'expression': '22/3',
                  'approximation': '7.33333333333333'}},
      {'card': 'float_approximation', 'variable': 'None', 'title': 'Floating-point approximation',
       'input': '(22/3).evalf()', 'pre_output': '', 'parameters': ['digits']}]),
    ('12',
     [{'title': 'SymPy', 'input': '12', 'output': {'type': 'Tex', 'tex': '12'}},
      {'card': 'digits', 'variable': 'None', 'title': 'Digits in base-10 expansion of number',
       'input': 'len(str(12))', 'pre_output': '', 'parameters': []},
      {'card': 'factorization', 'variable': 'None', 'title': 'Factors less than 100',
       'input': 'factorint(12, limit=100)', 'pre_output': '', 'parameters': []},
      {'card': 'factorizationDiagram', 'variable': 'None', 'title': 'Factorization Diagram',
       'input': 'factorint(12, limit=256)', 'pre_output': '', 'parameters': []}]),
    ('sin(2*x)',
     [{'title': 'SymPy', 'input': 'sin(2*x)', 'output': {'type': 'Tex', 'tex': '\\sin{\\left(2 x \\right)}'},
       'num_variables': 1, 'variables': ['x'], 'variable': 'x'},
      {'card': 'trig_alternate', 'variable': 'x', 'title': 'Alternate forms', 'input': None, 'pre_output': '',
       'parameters': []}, {'card': 'plot', 'variable': 'x', 'title': 'Plot', 'input': None, 'pre_output': '',
                           'parameters': ['xmin', 'xmax', 'tmin', 'tmax', 'pmin', 'pmax']},
      {'card': 'roots', 'variable': 'x', 'title': 'Roots', 'input': 'solve(sin(2*x), x)', 'pre_output': 'x',
       'parameters': []}, {'card': 'diff', 'variable': 'x', 'title': 'Derivative', 'input': 'diff(sin(2*x), x)',
                           'pre_output': '\\frac{d}{d x} \\sin{\\left(2 x \\right)}', 'parameters': []},
      {'card': 'integral_alternate', 'variable': 'x', 'title': 'Antiderivative forms', 'input': None, 'pre_output': '',
       'parameters': []},
      {'card': 'series', 'variable': 'x', 'title': 'Series expansion around 0', 'input': 'series(sin(2*x), x, 0, 10)',
       'pre_output': '', 'parameters': []}]),
]

g = SymPyGamma()


@pytest.mark.parametrize('case', cases)
def test(case):
    input_str, expected = case
    actual = g.eval(input_str)
    assert actual == expected
