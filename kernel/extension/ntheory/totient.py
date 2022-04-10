from sympy import Integer, factorint, latex

from extension.ntheory.util import cross_mul, is_positive_integer, is_prime_from_factor_dict, pow_list_from_factor_dict
from extension.util import Latex, format_latex, t, take_int_input
from gamma.result_card import ResultCard


@take_int_input
def totient_step(n: int) -> str:
    L = Latex()
    if n == 1:
        L.a(1).t(' is coprime to itself')
    else:
        factor_dict: dict[Integer, Integer] = factorint(n)
        pows = pow_list_from_factor_dict(factor_dict)
        if is_prime_from_factor_dict(factor_dict):
            L.a(n).t(' is prime')
        else:
            L.eq(n, cross_mul(*pows))
        L.n()
        if len(pows) > 1:
            L.for_we_have_so([R'(a,b)=1'], [R'\phi(a \cdot b) = \phi(a) \cdot \phi(b)'],
                             [R'\phi(%s) = %s' % (n, R'\cdot'.join(R'\phi(%s)' % latex(_pow) for _pow in pows))])
        L.for_we_have_so([t('prime ') + 'p'], [R'\phi(p^n) = (p-1) \cdot p^{n-1}'], [])
        res = 1
        for _pow in pows:
            b, e = _pow.base, _pow.exp
            part = (b - 1) * b ** (e - 1)  # type: ignore
            res *= part
            L.a(R'\phi(%s) = (%s - 1) \times %s^{%s - 1} = %s' % (latex(_pow), b, b, e, part)).n()
        L.as_a_result([R'\phi(%s) = %s' % (n, res)])
    return L.f()


totient_card = ResultCard("Step", None, eval_method=totient_step, format_output=format_latex,
                          applicable=is_positive_integer, wiki="Euler's_totient_function")
