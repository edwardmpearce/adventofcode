"""Test the utility functions for Advent of Code 2017 Day 3 (Spiral Memory)

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from spiral import (
    NeighbourSumSpiralFunction,
    Vector,
    generate_spiral_adjacent_sum_sequence,
    half_line_embedding,
)


@pytest.mark.parametrize(
    "num,expected",
    [
        (1, Vector(0,0)),
        (2, Vector(1,0)),
        (3, Vector(1,1)),
        (4, Vector(0,1)),
        (5, Vector(-1,1)),
        (6, Vector(-1,0)),
        (7, Vector(-1,-1)),
        (8, Vector(0,-1)),
        (9, Vector(1,-1)),
        (10, Vector(2,-1)),
        (11, Vector(2,0)),
        (12, Vector(2,1)),
        (13, Vector(2,2)),
        (14, Vector(1,2)),
        (15, Vector(0,2)),
        (16, Vector(-1,2)),
        (17, Vector(-2,2)),
        (18, Vector(-2,1)),
        (19, Vector(-2,0)),
        (20, Vector(-2,-1)),
        (21, Vector(-2,-2)),
        (22, Vector(-1,-2)),
        (23, Vector(0,-2)),
        (24, Vector(1,-2)),
        (25, Vector(2,-2)),
        (26, Vector(3,-2)),
        (27, Vector(3,-1)),
        (36, Vector(-2,3)),
        (49, Vector(3,-3)),
        (64, Vector(-3,4)),
        (81, Vector(4,-4)),
        (100, Vector(-4,5)),
        (121, Vector(5,-5)),
    ]
)
def test_half_line_embedding(num: int, expected: Vector):
    """Part 1 Test Cases"""
    assert half_line_embedding(num) == expected


def test_generate_spiral_adjacent_sum_sequence():
    """Part 2 Test Cases"""
    val_gen = generate_spiral_adjacent_sum_sequence()
    assert [next(val_gen) for _ in range(25)] == [
        1, 1, 2, 4, 5, 10, 11, 23, 25,
        26, 54, 57, 59, 122, 133, 142, 147,
        304, 330, 351, 362, 747, 806, 880, 931
    ]


@pytest.mark.parametrize(
    "num,expected",
    [
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 4),
        (5, 5),
        (9, 25),
        (8, 23),
        (7, 11),
        (6, 10),
        (10, 26),
        (11, 54),
        (12, 57),
        (13, 59),
        (25, 931),
        (24, 880),
        (17, 147),
        (19, 330),
        (23, 806),
    ]
)
def test_neighour_sum_spiral_function(num: int, expected: int):
    """Part 2 Test Cases"""
    spiral_func = NeighbourSumSpiralFunction()
    assert spiral_func(num) == expected
