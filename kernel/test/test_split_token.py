import pytest

from gamma.evaluator import token_splittable

split_cases = [
    'aBc',
    'xyz',
]


@pytest.mark.parametrize('token', split_cases)
def test_split(token: str):
    assert token_splittable(token) is True


non_split_cases = [
    'Alpha',
    't0',
    'velocity',
]


@pytest.mark.parametrize('token', non_split_cases)
def test_non_split(token: str):
    assert token_splittable(token) is False
