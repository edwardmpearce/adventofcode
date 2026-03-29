#!/usr/bin/env python3
"""
--- Day 6: Signals and Noise ---
https://adventofcode.com/2016/day/6
Error correction, decoding a repetition code

References
- https://en.wikipedia.org/wiki/Repetition_code
- https://docs.python.org/3/library/collections.html#collections.Counter
"""
import os
from collections import Counter

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        messages: list[str] = [line.strip() for line in file]

    print(f"Part 1: The answer is {decode_repetition_code_by_most_common(messages)}")
    print(f"Part 2: The answer is {decode_repetition_code_by_least_common(messages)}")


def decode_repetition_code_by_most_common(messages: list[str]) -> str:
    """Find the most frequent character for each position in a list of messages (assumed equal length), join and return."""
    return "".join([Counter(col).most_common()[0][0] for col in zip(*messages)])


def decode_repetition_code_by_least_common(messages: list[str]) -> str:
    """Find the least common character for each position in a list of messages (assumed equal length), join and return."""
    return "".join([Counter(col).most_common()[-1][0] for col in zip(*messages)])


if __name__ == "__main__":
    main()
