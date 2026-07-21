"""Testing functions for 2017 Day 2

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from sol import solve_part_1, find_quotient, solve_part_2


def test_solve_part_1():
    """Part 1 Test Case"""
    assert solve_part_1([[5, 1, 9, 5], [7, 5, 3], [2, 4, 6, 8]]) == 18


@pytest.mark.parametrize(
    "nums,expected",
    [
        ([5, 9, 2, 8], 4),
        ([9, 4, 7, 3], 3),
        ([3, 8, 6, 5], 2),
    ]
)
def test_find_quotient(nums: str, expected: int):
    """Part 2 Test Cases"""
    assert find_quotient(nums) == expected


def test_solve_part_2():
    """Part 2 Test Case"""
    assert solve_part_2([[5, 9, 2, 8], [9, 4, 7, 3], [3, 8, 6, 5]]) == 9
