#!/usr/bin/env python3
"""
--- Day 4: High-Entropy Passphrases ---
https://adventofcode.com/2017/day/4
Themes and Ideas
- Duplication, Uniqueness, Sets; Hashing, Mutability, and Serialization
- Anagrams, Equivalence Relations and Class Representatives
"""
import os

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        passphrases: list[str] = [line.strip() for line in file]

    print(f"Part 1: The number of passphrases with no duplicate words is {sum(no_duplicate_words(passphrase) for passphrase in passphrases)}")
    print(f"Part 2: The number of passphrases with no anagrams is {sum(no_anagram_words(passphrase) for passphrase in passphrases)}")


def has_no_duplicates(l: list) -> bool:
    """Indicates whether an iterable of hashable objects contains no duplicates"""
    seen_elements = set()
    for element in l:
        if element in seen_elements:
            return False
        seen_elements.add(element)
    return True


def no_duplicate_words(passphrase: str) -> bool:
    """Returns True if a series of words separated by spaces contains no duplicate words, and False otherwise"""
    return has_no_duplicates(passphrase.split())


def no_anagram_words(passphrase: str) -> bool:
    """Return True if the input string contains no two words that are anagrams of each other, and False otherwise.

    An anagram is determined by a set of letters with multiplicities.
    Each word is an anagram to the 'word' consisting of its letters sorted lexicographically in ascending order.
    """
    return has_no_duplicates("".join(sorted(word)) for word in passphrase.split())


if __name__ == "__main__":
    main()
