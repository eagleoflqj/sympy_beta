import pytest

from api import eval_card

card_cases = [
    (1, R'1\text{ is not considered prime}'),
    (2, R'\text{You should remember all prime numbers within 20: }\\\\\\'
        R'2, 3, 5, 7, 11, 13, 17, 19'),
    (4, R'4=2^{2}\text{, so }4\text{ is not prime}'),
    (22, R'\text{The last digit of }22\text{ is }2\text{ , so }22\text{ is a multiple of }2'),
    (23, R'\sqrt{23}\approx4.796\text{, so trying primes up to }4\text{ suffices}\\\\\\'
         R'23=11\times2+1\\\\\\'
         R'23=7\times3+2\\\\\\'
         R'\text{So }23\text{ is prime}'),
    (25, R'\text{The last digit of }25\text{ is }5\text{ , so }25\text{ is a multiple of }5'),
    (49, R'49=7^2\text{, so }49\text{ is a multiple of }7'),
    (77, R'\sqrt{77}\approx8.775\text{, so trying primes up to }8\text{ suffices}\\\\\\'
         R'77=38\times2+1\\\\\\'
         R'77=25\times3+2\\\\\\'
         R'77=15\times5+2\\\\\\'
         R'77=11\times7\\\\\\'
         R'\text{So }77\text{ is a multiple of }7'),
    (399, R'\text{The sum of digits of }399\text{ is }3+9+9=21\\\\\\'
          R'\text{The sum of digits of }21\text{ is }2+1=3\text{, which is a multiple of 3}\\\\\\'
          R'\text{So }399\text{ is a multiple of 3}'),
]


@pytest.mark.parametrize('n, expected', card_cases)
def test_card(n: int, expected: str):
    actual = eval_card('is_prime', f'isprime({n})', None, None)['tex']
    assert actual == expected
