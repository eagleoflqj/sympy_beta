from sympy import Integer, factorint, floor, latex, primerange, sqrt

from extension.ntheory.util import cross_mul, is_positive_integer, is_prime_from_factor_dict, pow_list_from_factor_dict
from extension.util import Latex, format_latex, take_int_input
from gamma.result_card import FakeResultCard


@take_int_input
def is_prime_step(n: int) -> str:
    L = Latex()
    if n == 1:
        L.a(1).t(' is not considered prime')
    else:
        factor_dict: dict[Integer, Integer] = factorint(n)
        pows = pow_list_from_factor_dict(factor_dict)
        if n <= 20:
            if is_prime_from_factor_dict(factor_dict):
                L.t('You should remember all prime numbers within 20: ').n()\
                    .a('2, 3, 5, 7, 11, 13, 17, 19')
            else:
                L.eq(n, cross_mul(*pows)).t(', so ').a(n).t(' is not prime')
        elif n % 2 == 0 or n % 5 == 0:
            L.t('The last digit of ').a(n).t(' is ').a(n % 10).\
                t(' , so ').a(n).t(' is a multiple of ').a(2 if n % 2 == 0 else 5)
        elif n % 3 == 0:
            m = n
            while m >= 20:
                if m != n:
                    L.n()
                digits = list(int(d) for d in str(m))
                sum_of_digits = sum(digits)
                L.t('The sum of digits of ').a(m).t(' is ').eq('+'.join(str(m)), sum_of_digits)
                m = sum_of_digits
            L.t(', which is a multiple of 3').n()
            L.t('So ').a(n).t(' is a multiple of 3')
        else:
            square_root = sqrt(n)
            if square_root.is_Integer:
                L.eq(n, f'{square_root}^2').t(', so ').a(n).t(' is a multiple of ').a(square_root)
            else:
                floor_of_sqrt = floor(square_root)
                L.a(latex(sqrt(n, evaluate=False)), R'\approx', square_root.round(3))\
                    .t(', so trying primes up to ').a(floor_of_sqrt).t(' suffices').n()
                for p in primerange(floor_of_sqrt + 1):
                    q, r = divmod(n, p)
                    L.a(n, '=', cross_mul(q, p))
                    if r == 0:
                        L.n().t('So ').a(n).t(' is a multiple of ').a(q)
                        break
                    else:
                        L.a('+', r).n()
                else:
                    L.t('So ').a(n).t(' is prime')
    return L.f()


is_prime_card = FakeResultCard("Step", "isprime(%s)", None, eval_method=is_prime_step, format_output=format_latex,
                               applicable=is_positive_integer)
