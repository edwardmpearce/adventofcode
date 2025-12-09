#!/usr/bin/env python3
"""
--- Day 2: Gift Shop ---
https://adventofcode.com/2025/day/2
Calculate the sum of all invalid IDs within the ranges defined by the puzzle input string
Part 1: An invalid ID is any ID which is made only of some sequence of digits repeated twice.
    So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.
Part 2: An invalid ID is any ID which is made only of some sequence of digits repeated at least twice.
    So, 12341234 (1234 two times), 123123123 (123 three times), 1212121212 (12 five times), and 1111111 (1 seven times) are all invalid IDs.
"""
from solution.helpers import get_puzzle_input
from solution.part_1 import solve_part_1
from solution.part_2 import solve_part_2


def main():
    puzzle_input: str = get_puzzle_input()
    print(f"Part 1: The answer is {solve_part_1(puzzle_input)}")
    print(f"Part 2: The answer is {solve_part_2(puzzle_input)}")


if __name__ == "__main__":
    main()
