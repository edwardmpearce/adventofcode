#!/usr/bin/env python3
"""
--- Day 3: Squares With Three Sides ---
https://adventofcode.com/2016/day/3
"""
import os

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        data: list[tuple[int, int, int]] = [tuple(map(int, line.strip().split())) for line in file]

    print(f"Part 1: The answer is {sum(is_valid_triangle(sides) for sides in data)}")

    part_2_answer: int = sum(
        is_valid_triangle(sides)
        for col in zip(*data)
        for sides in zip(col[::3], col[1::3], col[2::3])
    )
    print(f"Part 2: The answer is {part_2_answer}")


def is_valid_triangle(sides: tuple[int, int, int]) -> bool:
    """Determine whether the input triple of 3 integers can form the side lengths of a non-degenerate triangle
    The sum of the two short sides must be greater than the remaining longest side.
    """
    l0, l1, l2 = sorted(sides)
    return l0 + l1 > l2


if __name__ == "__main__":
    main()
