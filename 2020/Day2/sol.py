#!/usr/bin/env python3
"""
--- Day 2: Password Philosophy ---
https://adventofcode.com/2020/day/2
Part 1: Count occurences of a character within a string and verify it lies within a given range
Part 2: Check whether a test character appears exactly once in a pair of positions in a string
"""


def main():
    password_policies = [valid1, valid2]
    valid_passes = [0 for _ in password_policies]

    # Read and parse each line in the input file, then check whether the password on that line
    # satisfies each password policy
    with open("input.txt", 'r') as file:
        for line in file:
            # Parse line into separate variables
            rest, password = line.split(": ")
            rest, test_char = rest.split(" ")
            a, b = map(int, rest.split("-"))

            for i, validity_check in enumerate(password_policies):
                valid_passes[i] += validity_check(password, test_char, a, b)

    for i, count in enumerate(valid_passes, 1):
        print(f"Part {i}: {count} valid passwords")


def valid1(s, c, low, high):
    """
    Returns True or False depending on whether the number of occurences of the character `c`
    in the string `s` is between the integers `low` and `high` inclusive
    """
    return low <= s.count(c) <= high


def valid2(s, c, pos1, pos2):
    """
    From the string `s` extract the characters at (1-indexed) positions `pos1` and `pos2`.
    Return True when exactly one of these characters matches the test character `c`, otherwise False
    """
    return (s[pos1 - 1] == c) ^ (s[pos2 - 1] == c)


if __name__ == "__main__":
    main()
