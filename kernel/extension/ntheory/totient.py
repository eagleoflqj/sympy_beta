from sympy import factorint, latex, Mul, Pow

from gamma.result_card import FakeResultCard
from extension.util import Latex, t, format_latex


def totient_step(n: int):
    L = Latex()
    if n == 1:
        L.a(1, t(' is coprime to itself'))
    else:
        factor_dict: dict[int, int] = factorint(n)
        pows = [Pow(b, e, evaluate=False) for b, e in factor_dict.items()]
        if len(pows) == 1 and pows[0].exp == 1:
            L.a(n, t(' is prime'))
        else:
            L.eq(n, Mul(*pows, evaluate=False))
        L.n()
        if len(pows) > 1:
            L.for_we_have_so([R'(a,b)=1'], [R'\phi(a \cdot b) = \phi(a) \cdot \phi(b)'],
                             [R'\phi(%s) = %s' % (n, R'\cdot'.join(R'\phi(%s)' % latex(_pow) for _pow in pows))])
        L.for_we_have_so([t('prime ') + 'p'], [R'\phi(p^n) = (p-1) \cdot p^{n-1}'], [])
        res = 1
        for _pow in pows:
            b, e = _pow.base, _pow.exp
            part = (b - 1) * b ** (e - 1)
            res *= part
            L.a(R'\phi(%s) = (%s - 1) \cdot %s^{%s - 1} = %s' % (latex(_pow), b, b, e, part))
            L.n()
        L.as_a_result([R'\phi(%s) = %s' % (n, res)])
    return L.f()


def eval_totient(components, parameters=None):
    n = int(components['input_evaluated'])
    return totient_step(n)


totient_card = FakeResultCard("Step", "totient(%s)", None, eval_method=eval_totient, format_output=format_latex)
