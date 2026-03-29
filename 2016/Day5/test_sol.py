"""Testing functions for 2016 Day 5"""
from sol import solve_part_1, solve_part_2


def test_solve_part_1():
    """Part 1 Test Case"""
    assert solve_part_1(door_id="abc", difficulty=5, password_length=8) == "18f47a30"


def test_solve_part_2():
    """Part 2 Test Case"""
    assert solve_part_2(door_id="abc", difficulty=5, password_length=8) == "05ace8e3"
