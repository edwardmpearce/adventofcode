#!/usr/bin/env python3
"""
--- Day 2: Corruption Checksum ---
https://adventofcode.com/2017/day/2
Themes: Iteration, sorting, integer division, runtime performance/complexity
"""
import os

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        data: list[list[int]] = [list(map(int, line.split())) for line in file]

    print(f"Part 1: The answer is {solve_part_1(data)}")
    print(f"Part 2: The answer is {solve_part_2(data)}")


def solve_part_1(data: list[list[int]]) -> int:
    """Calculate the checksum of a spreadsheet of data.
    For each row, determine the difference between the largest value and the smallest value;
    the checksum is the sum of all of these differences.

    Note: It is possible to calculate the max and min of each row of numbers in a single iteration to
    reduce the required number of operations and potentially improve runtime performance
    """
    return sum(max(row) - min(row) for row in data)


def solve_part_2(data: list[list[int]]) -> int:
    """Given a table of integers where each row contains a unique pair of distinct numbers
    where one is an integer multiple of the other, return the sum of these integer quotients.
    """
    return sum(find_quotient(row) for row in data)


def find_quotient(nums: list[int]) -> int:
    """In a list of integers containing a unique pair of distinct elements
    where one is a multiple of the other, return their quotient"""
    # Sort the list of numbers first so that they can be compared efficiently in order
    nums = sorted(nums)
    for i, x in enumerate(nums):
        for y in nums[i+1:]:
            if y % x == 0:
                return y // x


if __name__ == "__main__":
    main()
