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
    ('tan(x)', b'P\x06z2\xb3&\xc4\x8eJ\x11\xc2\x01)\x8bG\x01'),  # todo: fix sympy#23348
    ('exp(x)/(1+exp(2*x))', b'\xa1\xe0\x93\xc1\xb6\xb9Ei\xb3g%\x1c\xd5\x97TG'),
    ('1/(x*(x+1))', b'\x81\xbel\xf3\x10T\xdf[\xb9\xb5[\x01\x04{j['),
]


@pytest.mark.parametrize('expr, expected', integrate_step_cases)
def test_integrate_step(expr: str, expected: bytes):
    actual = eval_card('intsteps', expr, 'x', None)
    assert hashlib.md5(json.dumps(actual).encode()).digest() == expected
