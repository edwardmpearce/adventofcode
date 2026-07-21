"""Testing functions for 2017 Day 1

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from sol import solve_part_1, solve_part_2


@pytest.mark.parametrize(
    "digits,expected",
    [
        ("1122", 3),
        ("1111", 4),
        ("1234", 0),
        ("91212129", 9),
    ]
)
def test_solve_part_1(digits: str, expected: int):
    """Part 1 Test Cases"""
    assert solve_part_1(digits) == expected


@pytest.mark.parametrize(
    "digits,expected",
    [
        ("1212", 6),
        ("1221", 0),
        ("123425", 4),
        ("123123", 12),
        ("12131415", 4),
    ]
)
def test_solve_part_2(digits: str, expected: int):
    """Part 2 Test Cases"""
    assert solve_part_2(digits) == expected
