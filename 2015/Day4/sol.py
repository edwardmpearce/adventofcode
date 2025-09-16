#!/usr/bin/env python3
"""
--- Day 4: The Ideal Stocking Stuffer ---
https://adventofcode.com/2015/day/4
Introduction to cryptographic hashing applications, MD5 algorithm, hexademical
Other possible themes include utilizing third-party code, unit testing

References
- https://en.wikipedia.org/wiki/MD5
- https://en.wikipedia.org/wiki/Hexadecimal
- https://www.google.com/search?q=python+md5
- https://docs.python.org/3/library/hashlib.html
- https://www.reddit.com/r/adventofcode/comments/18oki0y/2015_day_4_would_you_roll_your_own_md5/
- https://www.geeksforgeeks.org/python/md5-hash-python/
- https://en.wikipedia.org/wiki/Cryptographic_nonce
- https://cryptopals.com/
"""
import os
import hashlib


DIRPATH = os.path.dirname(__file__)


def main():
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        secret_key = file.read()

    print(f"Part 1: The answer is {find_smallest_valid_nonce(secret_key, 5)}")
    print(f"Part 2: The answer is {find_smallest_valid_nonce(secret_key, 6)}")


def find_smallest_valid_nonce(key: str, difficulty: int) -> int:
    """Returns the lowest positive integer which, when concatenated with the input key,
    yields an MD5 hash with a certain number of leading zeroes (the `difficulty`) when represented in hexadecimal.
    The 128-bit (16-byte) MD5 hashes (also termed message digests) are typically represented as a sequence of 32 hexadecimal digits.
    An arbitrary upper bound is used for the size of the search space to prevent the hypothetical risk of an infinite loop
    """
    if not isinstance(difficulty, int) or difficulty < 0:
        raise ValueError("Difficulty must be a non-negative integer")
    elif difficulty == 0:
        return 0

    for i in range(1, 1 << 32):
        message = key + str(i)
        md5_hash = hashlib.md5(message.encode())
        message_digest = md5_hash.hexdigest()
        if message_digest.startswith("0" * difficulty):
            return i


def test_find_smallest_valid_nonce():
    """Part 1 Test Cases"""
    assert find_smallest_valid_nonce("abcdef", 5) == 609043
    assert find_smallest_valid_nonce("pqrstuv", 5) == 1048970


if __name__ == "__main__":
    main()
