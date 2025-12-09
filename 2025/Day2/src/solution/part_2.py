#!/usr/bin/env python3
"""
--- Day 2: Gift Shop ---
https://adventofcode.com/2025/day/2
Calculate the sum of all invalid IDs within the ranges defined by the puzzle input string
Part 1: An invalid ID is any ID which is made only of some sequence of digits repeated twice.
    So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.
Part 2: An invalid ID is any ID which is made only of some sequence of digits repeated at least twice.
    So, 12341234 (1234 two times), 123123123 (123 three times), 1212121212 (12 five times), and 1111111 (1 seven times) are all invalid IDs.

Insights
- For a string `seq` and a composite number `n = a * b`, then `seq * n = (seq * a) * b = (seq * b) * a`.
- An ID is invalid iff it can be represented as repeat(seq, p) for some sequence of digits `seq` and prime factor `p` of the number of digits in the ID
- Range endpoints in the puzzle input go up to 10 digits
"""
from solution.helpers import parse_ranges, is_repeated_sequence, next_id_with_n_repeats, prime_factors


def solve_part_2(puzzle_input: str) -> int:
    ranges: list[tuple[int, int]] = parse_ranges(puzzle_input)
    return sum(sum(find_invalid_ids(start, end)) for start, end in ranges)


def find_invalid_ids(start: int, end: int) -> list[int]:
    """Return a sorted list of all invalid IDs between `start` and `end` inclusive."""
    invalid_ids: set[int] = {start} if is_invalid_id(start) else set()

    multiple_to_check: set[int] = prime_factors_of_numbers_in_range(len(str(start)), len(str(end)))

    for p in multiple_to_check:
        candidate = next_id_with_n_repeats(start, p)
        while candidate <= end:
            invalid_ids.add(candidate)
            candidate = next_id_with_n_repeats(candidate, p)

    return sorted(invalid_ids)


def is_invalid_id(num: int) -> bool:
    """An invalid ID is any ID which is made only of some sequence of digits repeated at least twice.
    So, 12341234 (1234 two times), 123123123 (123 three times), 1212121212 (12 five times), and 1111111 (1 seven times) are all invalid IDs.
    """
    assert num >= 0
    num_str = str(num)
    num_digits = len(num_str)
    return any(is_repeated_sequence(num_str, p) for p in set(prime_factors(num_digits)))


def prime_factors_of_numbers_in_range(start: int, end: int) -> set[int]:
    """Return a set containing all prime factors of each number `n` between `start` and `end` inclusive."""
    relevant_factors: set[int] = set()
    for n in range(start, end + 1):
        relevant_factors.update(prime_factors(n))
    return relevant_factors
