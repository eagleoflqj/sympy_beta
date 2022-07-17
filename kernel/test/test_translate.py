import pytest

from nlp import translate

corner_cases = [
    (' is  2 even ', '(2).is_even'),  # extra space
    ('Is 2 even', '(2).is_even'),  # capital letter
    ('is 2 even.', '(2).is_even'),  # period
    ('is 2 even??', '(2).is_even'),  # question mark
]

ntheory_cases = [
    ('is 2 even', '(2).is_even'),
    ('is 3 odd', '(3).is_odd'),
    ('is 5 prime', 'isprime(5)'),
    ('is 5 a prime number', 'isprime(5)'),
    ('is 6 a multiple of 3', '(6) % (3) == 0'),
]

calculus_cases = [
    ('integrate xy^2 with respect to y', 'integrate((xy^2), (y))'),
    ('integrate x', 'integrate(x)'),
]

cases = corner_cases \
    + ntheory_cases \
    + calculus_cases


@pytest.mark.parametrize('nl, expected', cases)
def test(nl: str, expected: str):
    actual = translate(nl)
    assert actual == expected
