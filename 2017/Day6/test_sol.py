"""Testing functions for 2017 Day 6

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from sol import redistribute, solve_part_1, solve_part_2


@pytest.mark.parametrize(
    "memory_banks,expected",
    [
        ((0, 2, 7, 0), (2, 4, 1, 2)),
        ((2, 4, 1, 2), (3, 1, 2, 3)),
        ((3, 1, 2, 3), (0, 2, 3, 4)),
        ((0, 2, 3, 4), (1, 3, 4, 1)),
        ((1, 3, 4, 1), (2, 4, 1, 2)),
    ]
)
def test_redistribute(memory_banks: tuple[int], expected: tuple[int]):
    """Part 1 Test Cases"""
    assert redistribute(memory_banks) == expected


def test_solve_part_1():
    """Part 1 Test Case"""
    assert solve_part_1(initial_config=(0, 2, 7, 0)) == 5


def test_solve_part_2():
    """Part 2 Test Case"""
    assert solve_part_2(initial_config=(0, 2, 7, 0)) == 4
