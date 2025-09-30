#!/usr/bin/env python3
"""
--- Day 11: Corporate Policy ---
https://adventofcode.com/2015/day/11
Possible themes: 
- Breaking down problems into smaller pieces
- Program design and optimization
- String slicing and padding
- Unicode code points
- Modular arithmetic in base 26

Main Functions
- main: Calculate and print the puzzle answers
  - find_next_valid_password: Find a new password by incrementing an old password string repeatedly until it is valid
    - next_password_candidate: Increment to next candidate in order or skip past forbidden letters if present to reduce the number of iterations
      - increment_password: Increment a string of lowercase ASCII letters in lexicographic order, maintaining a fixed string length and cycling from highest to lowest
    - is_valid_password: Determine whether the given string meets the applicable password policy requirements

Extras
- PasswordStatus: enum.Flag class to indicate which password requirements are satisfied
- validate_password: Validate the input string against a predefined set of password requirements
- longest_increasing_straight: Find the length of the longest substring of incrementally increasing characters (by unicode code point value) within the input string
- distinct_repeated_letter_pairs: Find the set of repeated pairs of letters, like 'aa', 'bb', or 'zz', present within the input string
- from_base_digits: Converts a list of digits in the given base to an integer
- to_base_digits: Converts a non-negative number to a list of digits in the given base
- from_base26_repr: Interpret a string of lowercase letters a-z as an integer in base 26 where a -> 0, ..., z -> 25
- to_base26_repr: Return a base 26 representation of the input nonnegative integer where the digits are a -> 0, ..., z -> 25

References
- https://docs.python.org/3/library/functions.html
- https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/
- https://mathspp.com/blog/base-conversion-in-python
"""
import os
import enum

DIRPATH = os.path.dirname(__file__)

FORBIDDEN_LETTERS: str = "iol"


def main():
    """Calculate and print the puzzle answers"""
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        puzzle_input = file.read()

    next_pass = find_next_valid_password(puzzle_input)
    next_next_pass = find_next_valid_password(next_pass)
    print(f"The next two valid passwords after the initial string are {next_pass} and {next_next_pass}")
    n0, n1, n2 = map(from_base26_repr, (puzzle_input, next_pass, next_next_pass))
    print(f"The number of increments required for each part was {n1 - n0} and {n2 - n1}, respectively.")


def find_next_valid_password(s: str) -> str:
    """Find a new password by incrementing an old password string repeatedly until it is valid
    Apply a shortcut to skip past forbidden letters to reduce the number of iterations
    """
    candidate = next_password_candidate(s)
    while not is_valid_password(candidate):
        candidate = next_password_candidate(candidate)
    return candidate


def next_password_candidate(s: str) -> str:
    """Increment to next candidate in order or skip past forbidden letters if present to reduce the number of iterations"""
    forbidden_letter_set = set(FORBIDDEN_LETTERS)
    for idx, c in enumerate(s):
        if c in forbidden_letter_set:
            return s[:idx] + chr(ord(c) + 1) + ("a" * (len(s) - (idx + 1)))
    return increment_password(s)


def increment_password(s: str) -> str:
    """Increment a string of lowercase ASCII letters in lexicographic order, maintaining a fixed string length and cycling from highest to lowest.
    Increase the rightmost letter one step; if it was z, it wraps around to a, and repeat with the next letter to the left until one doesn't wrap around.
    """
    for idx, c in enumerate(s[::-1], 1):
        if c != "z":
            return s[:len(s)-idx] + chr(ord(c) + 1) + ("a" * (idx-1))
    return "a" * len(s)


def is_valid_password(s: str) -> str:
    """Determine whether the given string meets the applicable password policy requirements.
    Optimized somewhat for computational efficiency at the expense of simplicity/decoupling by combining loops and breaking early where possible

    Checks the input string for an increasing straight of at least three letters, like 'abc', 'bcd', 'cde', and so on, up to 'xyz'.
    Checks whether the input string contains at least two different, non-overlapping pairs of letters, like 'aa', 'bb', or 'zz'.
    Note that the requirement that the repeated letter pairs consist of different (repeated) letters implies that they would be non-overlapping.
    """
    forbidden_letter_set = set(FORBIDDEN_LETTERS)
    repeated_letters = set()
    longest_straight, current_straight = 1, 1
    for c1, c2 in zip(s, s[1:]):
        if c1 in forbidden_letter_set:
            return False
        if ord(c2) - ord(c1) == 1:
            current_straight += 1
        else:
            longest_straight, current_straight = max(longest_straight, current_straight), 1
            if c1 == c2:
                repeated_letters.add(c1)
    return (max(longest_straight, current_straight) >= 3) and (len(repeated_letters) >= 2)


class PasswordStatus(enum.Flag):
    """enum.Flag class to indicate which password requirements are satisfied"""
    NO_REQUIREMENTS_SATISIFIED = 0
    STRAIGHT_OF_THREE = enum.auto()
    NO_FORBIDDEN_LETTERS = enum.auto()
    TWO_PAIR = enum.auto()
    VALID = STRAIGHT_OF_THREE | NO_FORBIDDEN_LETTERS | TWO_PAIR


def validate_password(s: str) -> PasswordStatus:
    """Validate the input string against a predefined set of password requirements, returning an `enum.Flag` object 
    which indicates which requirements are satisfied and whether the password is valid overall
    """
    status = PasswordStatus(0)
    if not any(c in s for c in FORBIDDEN_LETTERS):
        status |= PasswordStatus.NO_FORBIDDEN_LETTERS    
    # Check the input string for an increasing straight of at least three letters, like 'abc', 'bcd', 'cde', and so on, up to 'xyz'
    if longest_increasing_straight(s) >= 3:
        status |= PasswordStatus.STRAIGHT_OF_THREE
    # Check whether the input string contains at least two different, non-overlapping pairs of letters, like 'aa', 'bb', or 'zz'.
    # Note that the requirement that the repeated letter pairs consist of different (repeated) letters implies that they would be non-overlapping.
    if len(distinct_repeated_letter_pairs(s)) >= 2:
        status |= PasswordStatus.TWO_PAIR
    return status


def longest_increasing_straight(s: str) -> int:
    """Find the length of the longest substring of incrementally increasing characters (by unicode code point value) within the input string"""
    if len(s) == 0:
        return 0
    longest_straight, current_straight = 1, 1
    for c1, c2 in zip(s, s[1:]):
        if ord(c2) - ord(c1) == 1:
            # Increasing straight continues
            current_straight += 1
        else:
            # Current straight has ended. Update longest straight if needed and start a new straight.
            longest_straight, current_straight = max(longest_straight, current_straight), 1
    # Check whether last straight in the string is the longest
    return max(longest_straight, current_straight)


def distinct_repeated_letter_pairs(s: str) -> set[str]:
    """Find the set of repeated pairs of letters, like 'aa', 'bb', or 'zz', present within the input string."""
    repeated_letters = set()
    for c1, c2 in zip(s, s[1:]):
        if c1 == c2:
            repeated_letters.add(c1 + c2)
    return repeated_letters


def from_base_digits(digits: list[int], base: int):
    """Converts a list of digits in the given base to an integer.
    The first digit is the most significant and the base is assumed to be an integer greater than or equal to 2.
    Alternative (less compute efficient) implementation: return sum(digit * (26 ** exp) for exp, digit in enumerate(reversed(digits)))
    """
    number, power = 0, 1
    for digit in reversed(digits):
        number += power * digit
        power *= base
    return number


def to_base_digits(n: int, base: int) -> list[int]:
    """Converts a non-negative number to a list of digits in the given base.
    The base must be an integer greater than or equal to 2 and the first digit in the list of digits is the most significant one.
    """
    if n == 0:
        return [0]

    digits = []
    while n:
        digits.append(n % base)
        n //= base
    return list(reversed(digits))


def from_base26_repr(s: str) -> int:
    """Interpret a string of lowercase letters a-z as an integer in base 26 where a -> 0, ..., z -> 25
    Note: ord('a') == 97, ord('z') == 122
    """
    if not s.isascii() and s.islower():
        raise ValueError("Expected a string of lowercase ASCII letters [a-z]")
    return from_base_digits([ord(c) - 97 for c in s], 26)


def to_base26_repr(n: int) -> str:
    """Return a base 26 representation of the input nonnegative integer where the digits are a -> 0, ..., z -> 25
    Note: chr(97) == 'a', chr(122) == 'z'
    """
    return "".join(chr(digit + 97) for digit in to_base_digits(n, 26))


if __name__ == "__main__":
    main()
