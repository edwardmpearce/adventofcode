"""Testing functions for 2017 Day 5"""
from sol import solve_part_1, solve_part_2


def test_solve_part_1():
    """Part 1 Test Case"""
    assert solve_part_1(dict(enumerate([0, 3, 1, 0, -3]))) == 5


def test_solve_part_2():
    """Part 2 Test Case"""
    assert solve_part_2(dict(enumerate([0, 3, 1, 0, -3]))) == 10
