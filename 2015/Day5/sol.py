#!/usr/bin/env python3
"""
--- Day 5: Doesn't He Have Intern-Elves For This? ---
https://adventofcode.com/2015/day/5
Themes include logical operations and parallel iteration

References
- https://docs.python.org/3/library/functions.html#zip
"""
import os


DIRPATH = os.path.dirname(__file__)


def main():
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        string_list: list[str] = [line for line in file]

    print(f"Part 1: The number of nice strings in the file is {sum(is_nice_1(s) for s in string_list)}")
    print(f"Part 2: Under the new rules, the number of nice strings in the file is {sum(is_nice_2(s) for s in string_list)}")


def is_nice_1(s: str) -> bool:
    vowel_count = sum(char in 'aeiou' for char in s)
    has_double_letter = any(char1 == char2 for char1, char2 in zip(s, s[1:]))
    bad_pairs = (("a", "b"), ("c", "d"), ("p", "q"), ("x", "y"))
    has_bad_letter_pair = any(pair in bad_pairs for pair in zip(s, s[1:]))

    return vowel_count >= 3 and has_double_letter and not has_bad_letter_pair


def is_nice_2(s: str) -> bool:
    has_spaced_repeating_letter = any(char1 == char2 for char1, char2 in zip(s, s[2:]))

    # Indicates whether a string contains a pair of any two letters that appears at least twice in the string without overlapping
    has_repeating_pair = any(
        pair1 == pair2
        for i, pair1 in enumerate(zip(s, s[1:])) # First loop through consecutive letter pairs
        for pair2 in zip(s[i+2:], s[i+3:]) # Next loop through subsequent letter pairs which don't overlap
    )

    return has_spaced_repeating_letter and has_repeating_pair


if __name__ == "__main__":
    main()
