#!/usr/bin/env python3
"""
--- Day 3: Lobby ---
https://adventofcode.com/2025/day/3
Themes: max and argmax, pointers, string concatenation
"""
import os

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        data = [line.strip() for line in file]

    print(f"Part 1: The answer is {sum(find_max_joltage(bank, num_batteries=2) for bank in data)}")
    print(f"Part 2: The answer is {sum(find_max_joltage(bank, num_batteries=12) for bank in data)}")


def find_max_joltage(bank: str, num_batteries: int) -> int:
    """Return the maximum value that can be obtained by concatenating n (num_batteries) digits/characters taken from the input (bank)
    whilst retaining the ordering of digits from the original input
    """
    selected_batteries: str = ""
    search_start: int = 0
    for remaining_batteries in range(num_batteries, 0, -1):
        search_end: int = len(bank) + 1 - remaining_batteries
        max_seen, relative_idx = find_max_value(bank[search_start:search_end])
        selected_batteries += max_seen
        # The search space for the next battery starts at the index after the latest battery was found
        search_start += relative_idx + 1
    return int(selected_batteries)


def find_max_value(bank: str) -> tuple[str, int]:
    """Return the max value from the input together with the first position it appears"""
    max_seen: str = "0"
    max_pos: int = -1
    for idx, val in enumerate(bank):
        if val > max_seen:
            max_seen, max_pos = val, idx
    return max_seen, max_pos


if __name__ == "__main__":
    main()
