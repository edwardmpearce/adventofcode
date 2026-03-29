"""Testing functions for 2015 Day 4

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from sol import find_smallest_valid_nonce


@pytest.mark.parametrize(
    "key,difficulty,expected",
    [
        ("abcdef", 5, 609043),
        ("pqrstuv", 5, 1048970),
    ]
)
def test_find_smallest_valid_nonce(key: str, difficulty: int, expected: int):
    assert find_smallest_valid_nonce(key, difficulty) == expected
