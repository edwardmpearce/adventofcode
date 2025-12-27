#!/usr/bin/env python3
"""
--- Day 5: Cafeteria ---
https://adventofcode.com/2025/day/5
Part 1: Membership within a closed/inclusive range
Part 2: Representing union of integer ranges as a minimal disjoint union
"""
import os

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        raw_fresh_ranges, ingredient_ids = parse_puzzle_input(file.read())

    fresh_ranges = sort_and_combine_overlapping_ranges(raw_fresh_ranges)
    print(f"The original set of {len(raw_fresh_ranges)} ranges can be simplified into a minimal equivalent list of {len(fresh_ranges)} ranges.")

    part_1_answer = sum(is_fresh(ingredient_id, fresh_ranges) for ingredient_id in ingredient_ids)
    print(f"Part 1: There are {len(ingredient_ids)} ingredients, of which {part_1_answer} are fresh.")

    part_2_answer = sum(b - a + 1 for a, b in fresh_ranges)
    print(f"Part 2: The fresh ingredient ID ranges contain a total of {part_2_answer} ingredient IDs.")


def parse_puzzle_input(puzzle_input: str) -> tuple[list[tuple[int, int]], list[int]]:
    """Parse puzzle input string into lists of fresh ingredient ID ranges and available ingredient IDs."""
    ranges_input, _, ingredients_input = puzzle_input.partition("\n\n")
    fresh_ranges: list[tuple[int, int]] = [tuple(map(int, line.split('-'))) for line in ranges_input.splitlines()]
    ingredient_ids: list[int] = list(map(int, ingredients_input.splitlines()))
    return fresh_ranges, ingredient_ids


def sort_and_combine_overlapping_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Return a minimal list of ranges in ascending order which describes the same set of integers as the input.
    To do this we sort the ranges and repeatedly combine where endpoints overlap or meet.
    """
    if not ranges:
        return ranges
    new_ranges: list[tuple[int, int]] = []
    ranges.sort()
    start, end = ranges[0]
    for a, b in ranges[1:]:
        if end + 1 >= a:
            # End of temp range meets or surpasses start of range (a,b) so the two ranges can be combined.
            # Extend end of temp range if possible. We already know start <= a by sorting.
            end = max(end, b)
        else:
            # No overlapping with temp range, so add to new ranges and update temp range
            new_ranges.append((start, end))
            start, end = a, b

    # Save last temp range to list of new ranges
    new_ranges.append((start, end))

    return new_ranges


def is_fresh(ingredient_id: int, fresh_ranges: list[tuple[int, int]]) -> bool:
    """An ingredient ID is fresh if it is in any fresh ingredient ID range (endpoints inclusive)."""
    return any((start <= ingredient_id <= end) for start, end in fresh_ranges)


if __name__ == "__main__":
    main()
