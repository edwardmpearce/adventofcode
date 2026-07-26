"""Testing functions for 2017 Day 3

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from sol import solve_part_1, solve_part_2


@pytest.mark.parametrize(
    "num,expected",
    [
        (1, 0),
        (2, 1),
        (3, 2),
        (4, 1),
        (5, 2),
        (6, 1),
        (7, 2),
        (8, 1),
        (9, 2),
        (10, 3),
        (11, 2),
        (12, 3),
        (23, 2),
        (25, 4),
        (1024, 31),
    ]
)
def test_solve_part_1(num: int, expected: int):
    """Part 1 Test Cases"""
    assert solve_part_1(num) == expected


@pytest.mark.parametrize(
    "num,expected",
    [
        (1, 2),
        (2, 4),
        (3, 4),
        (4, 5),
        (5, 10),
        (15, 23),
        (60, 122),
        (150, 304),
        (297, 304),
        (750, 806),
        (900, 931),
    ]
)
def test_solve_part_2(num: int, expected: int):
    """Part 2 Test Cases"""
    assert solve_part_2(num) == expected
