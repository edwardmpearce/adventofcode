#!/usr/bin/env python3
"""
--- Day 2: Gift Shop ---
https://adventofcode.com/2025/day/2
Part 1: Calculate the sum of all invalid IDs within the ranges defined by the puzzle input string
An invalid ID is any ID which is made only of some sequence of digits repeated twice.
    So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.

Insights
- Shortcut for determining whether an ID is invalid by checking the parity (odd or even) of the number of digits
  - Invalid IDs will necessarily have an even number of digits
  - IDs with an odd number of digits are always valid and never invalid
- Due to the repetitive structure of invalid IDs, it is possible to analytically determine the smallest invalid ID greater than any given number.
  - This way we can find all invalid IDs within a given range more quickly than checking exhaustively by incrementing the prospective ID by one each time.
"""
from collections.abc import Iterator

from solution.helpers import parse_ranges, is_repeated_sequence, next_id_with_n_repeats


def solve_part_1(puzzle_input: str) -> int:
    ranges: list[tuple[int, int]] = parse_ranges(puzzle_input)
    return sum(sum(find_invalid_ids(start, end)) for start, end in ranges)


def find_invalid_ids(start: int, end: int) -> Iterator[int]:
    """Yield all invalid IDs between `start` and `end` inclusive."""
    candidate: int = start if is_invalid_id(start) else next_id_with_n_repeats(start, repeats=2)
    while candidate <= end:
        yield candidate
        candidate = next_id_with_n_repeats(candidate, repeats=2)


def is_invalid_id(num: int) -> bool:
    """An invalid ID is any ID which is made only of some sequence of digits repeated twice.
    So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.
    """
    assert num >= 0
    return is_repeated_sequence(str(num), repeats=2)
