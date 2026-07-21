#!/usr/bin/env python3
"""
--- Day 1: Inverse Captcha ---
https://adventofcode.com/2017/day/1
Themes: Iteration, indices, and modular arithmetic
Additional Themes: Testing, Runtime Performance, Input Validation
"""
import os

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        digits = file.read().strip()

    print(f"Part 1: The answer is {solve_part_1(digits)}")
    print(f"Part 2: The answer is {solve_part_2(digits)}")


def solve_part_1(digits: str) -> int:
    """Given a sequence of digits, find the sum of all digits that match the next digit in the list.
    The list is circular, so the digit after the last digit is the first digit in the list.
    """
    n = len(digits)
    return sum(
        int(digit)
        for idx, digit in enumerate(digits)
        if digit == digits[(idx + 1) % n]
    )


def solve_part_2(digits: str) -> int:
    """Given a sequence of digits of length 2n, find the sum of
    all digits that match the digit halfway around the circular list.
    """
    n = len(digits) // 2
    if n == 0:
        return 0

    return 2 * sum(
        int(digits[i])
        for i in range(n)
        if digits[i] == digits[i + n]
    )


if __name__ == "__main__":
    main()
