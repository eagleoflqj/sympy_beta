import hashlib
import json

import pytest

from api import eval_card

cases = [
    (('digits', '12', None, None),
     {'tex': '2', 'type': 'Tex'}),
    (('factorization', '12', None, None),
     {'rows': [['2', '2'], ['3', '1']], 'titles': ('Factor', 'Times'), 'type': 'Table'}),
    (('factorizationDiagram', '12', None, None),
     {'primes': [3, 2, 2], 'type': 'FactorDiagram'}),
    (('float_approximation', '242/33', None, {'digits': 15}),
     {'tex': '7.33333333333333', 'type': 'Tex'}),
    (('approximator', '22/3', 'x', {'digits': 25}),
     {'approximation': '7.333333333333333333333333', 'expression': '22/3',
      'numeric': True, 'tex': '\\frac{22}{3}', 'type': 'Tex'}),
    (('diffsteps', 'x', 'x', None),
     {'answer': {'block': '1'}, 'type': 'StepContainer',
      'content': {'level': [{'step': [{'p': (
          {'text': 'Apply the power rule: '},
          {'inline': 'x'},
          {'text': ' goes to '},
          {'inline': '1'})}]}]}}),
    (('integral_alternate', 'x', 'x', None),
     {'results': [{'input': 'integrate(x, x)', 'output': {'tex': '\\frac{x^{2}}{2}', 'type': 'Tex'}}],
      'type': 'MultiResult'}),
    (('integral_alternate_fake', 'integrate(tan(x))', 'x', None),
     {'results': [{'input': 'integrate(tan(x), x)',
                   'output': {'tex': R'- \ln{\left(\cos{\left(x \right)} \right)}', 'type': 'Tex'}}],
      'type': 'MultiResult'}),
    (('truth_table', '(x | y) & (x | ~y) & (~x | y)', 'y', None),
     {'rows': [['True', 'True', 'True'],
               ['True', 'False', 'False'],
               ['False', 'True', 'False'],
               ['False', 'False', 'False']], 'titles': ['x', 'y', 'Values'], 'type': 'TruthTable'}),
    (('function_docs', 'factorial2', None, None),
     {'type': 'Document',
      'html': '<div class="document">\n<p>The double factorial <cite>n!!</cite>, not to be confused with <cite>(n!)!'
              '</cite></p>\n<p>The double factorial is defined for nonnegative integers and for odd\nnegative '
              'integers as:</p>\n<div class="formula">\n<i>n</i>!!\u2009=\u2009<span class="array">'
              '<span class="arrayrow"><span class="bracket align-l">⎧</span></span><span class="arrayrow">'
              '<span class="bracket align-l">⎪</span></span><span class="arrayrow"><span class="bracket align-l">⎪'
              '</span></span><span class="arrayrow"><span class="bracket align-l">⎨</span></span>'
              '<span class="arrayrow"><span class="bracket align-l">⎪</span></span><span class="arrayrow">'
              '<span class="bracket align-l">⎪</span></span><span class="arrayrow"><span class="bracket align-l">⎩'
              '</span></span></span><span class="bracketcases">\n<span class="arrayrow">\n<span class="case align-l">'
              '\n1\u2003\n</span>\n<span class="case align-l">\n<i>n</i>\u2009=\u20090\u2003\n</span>\n\n</span>\n'
              '<span class="arrayrow">\n<span class="case align-l">\n\u2005\u2003\n</span>\n<span class="case align-l">'
              '\n\u2005\u2003\n</span>\n\n</span>\n<span class="arrayrow">\n<span class="case align-l">\n<i>n</i>'
              '(<i>n</i>\u2009−\u20092)(<i>n</i>\u2009−\u20094)⋯1\u2003\n</span>\n<span class="case align-l">\n<i>n'
              '</i> <span class="text">positive odd</span>\u2003\n</span>\n\n</span>\n<span class="arrayrow">\n'
              '<span class="case align-l">\n\u2005\u2003\n</span>\n<span class="case align-l">\n\u2005\u2003\n</span>'
              '\n\n</span>\n<span class="arrayrow">\n<span class="case align-l">\n<i>n</i>(<i>n</i>\u2009−\u20092)'
              '(<i>n</i>\u2009−\u20094)⋯2\u2003\n</span>\n<span class="case align-l">\n<i>n</i> <span class="text">'
              'positive even</span>\u2003\n</span>\n\n</span>\n<span class="arrayrow">\n<span class="case align-l">'
              '\n\u2005\u2003\n</span>\n<span class="case align-l">\n\u2005\u2003\n</span>\n\n</span>\n'
              '<span class="arrayrow">\n<span class="case align-l">\n(<i>n</i>\u2009+\u20092)!!\u2009⁄\u2009'
              '(<i>n</i>\u2009+\u20092)\u2003\n</span>\n<span class="case align-l">\n<i>n</i> <span class="text">'
              'negative odd</span>\u2003\n</span>\n\n</span>\n\n</span>\n\n</div>\n'
              '<div class="section" id="references">\n<h1>References</h1>\n'
              '<table class="docutils footnote" frame="void" id="footnote-1" rules="none">\n<colgroup>'
              '<col class="label" /><col /></colgroup>\n<tbody valign="top">\n<tr><td class="label">[1]</td><td>'
              '<a class="reference external" href="https://en.wikipedia.org/wiki/Double_factorial">'
              'https://en.wikipedia.org/wiki/Double_factorial</a></td></tr>\n</tbody>\n</table>\n</div>\n'
              '<div class="section" id="examples">\n<h1>Examples</h1>\n<pre class="doctest-block">\n&gt;&gt;&gt; '
              'from sympy import factorial2, var\n&gt;&gt;&gt; n = var(\'n\')\n&gt;&gt;&gt; n\nn\n&gt;&gt;&gt; '
              'factorial2(n + 1)\nfactorial2(n + 1)\n&gt;&gt;&gt; factorial2(5)\n15\n&gt;&gt;&gt; factorial2(-1)\n1\n'
              '&gt;&gt;&gt; factorial2(-5)\n1/3\n</pre>\n</div>\n<div class="section" id="see-also">\n<h1>See Also'
              '</h1>\n<p>factorial, RisingFactorial, FallingFactorial</p>\n</div>\n</div>\n'}
     ),
]


@pytest.mark.parametrize('args, expected', cases)
def test(args: tuple, expected: dict):
    card_name, expression, variable, parameters = args
    actual = eval_card(card_name, expression, variable, parameters)
    assert actual == expected


def test_plot():
    actual = eval_card('plot', 'x', 'x', {'xmin': 10, 'xmax': 30})
    assert actual['type'] == 'Plot'
    graph = actual['graphs'][0]
    assert graph['points']['x'][0] == 10
    assert graph['points']['x'][-1] == 30


integrate_step_cases = [
    ('tan(x)', b'\x0f \xf5<\xad\x0c}\x9br\xf6\x95\tVY\x90\x95'),  # todo: fix sympy#23348
    ('exp(x)/(1+exp(2*x))', b'\x8cX\xd4\xeb\x0e\x0f\xec\xdb\x1c\x1e\xda\xf1\x11I\xb6\xa7'),
    ('1/(x*(x+1))', b'\x05\xb4\xadsy\x8dM~z\xb9\x05\x8a\xff>\xf6\x87'),  # todo: too complicated
    ('1/sqrt(1-x**2)', b'{\xda,\xff\xc9\xbb\x98\xae\xc0\xc3\xcdHuo\xaa\x13'),
    ('1/(x**2+1)', b'\xe2\xe9\xd8\xf3\x1a\xf8\x8e5\xde[\xc4\xb4\xa6\x83a\xf6'),
    ('1/sqrt(x**2+1)', b'\xf0#C\xb7G\xec\x142\x01\xd1\xde.\xb1Z\xfe\x95'),
    ('Derivative(f(x), x)', b',eaB\x9c\x10\xed|\xa0\xcdk:\xe6X\x8aN'),
    ('Heaviside(x)', b'\x9c\x86\x91es\xb8\xa5/y\xd3\xa2T\x11u\x83\xe2'),
    ('(x**2+1)**(-3/2)', b'\x15\x8d\xc0\xf7\xb3~#Oy\xf0\x0c\xae\x9b\xf8V\xcb'),
    ('x*sin(x)', b'\xc4\xaf\x84$"\x03\xb2\xf6\xb5\x9c\xf2T\xcd\xa3\x90\xeb'),
    ('exp(x)*sin(x)', b'\x0b4\x15\xd3\x0fR\xf0\xb9\x90\x7f\x06~\xe1\x8c\xe4\xa3'),
]


@pytest.mark.parametrize('expr, expected', integrate_step_cases)
def test_integrate_step(expr: str, expected: bytes):
    actual = eval_card('intsteps', f'integrate({expr})', 'x', None)
    assert hashlib.md5(json.dumps(actual).encode()).digest() == expected
