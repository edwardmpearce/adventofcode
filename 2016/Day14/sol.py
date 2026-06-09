#!/usr/bin/env python3
"""
--- Day 14: One-Time Pad ---
https://adventofcode.com/2016/day/14

Themes:
- Introduction to cryptographic hashing applications, MD5 algorithm, hexademical
- Regular expressions, caching, unit testing

Compare and contrast with 2015 Day 4, 2016 Day 5

References
- https://en.wikipedia.org/wiki/MD5
- https://en.wikipedia.org/wiki/Hexadecimal
- https://www.google.com/search?q=python+md5
- https://docs.python.org/3/library/hashlib.html
- https://www.reddit.com/r/adventofcode/comments/18oki0y/2015_day_4_would_you_roll_your_own_md5/
- https://www.geeksforgeeks.org/python/md5-hash-python/
- https://en.wikipedia.org/wiki/Cryptographic_nonce
- https://cryptopals.com/
- https://docs.python.org/3/library/functools.html

"""
import os
from typing import Iterator, Callable
import functools
import hashlib
import re

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        salt = file.read()

    print(f"Part 1: The answer is {solve_part_1(salt=salt)}")
    print(f"Part 2: The answer is {solve_part_2(salt=salt)}")


def solve_part_1(salt: str) -> int:
    """"""
    key_generator = generate_one_time_pad_keys(salt=salt)
    one_time_pad_keys = [next(key_generator) for _ in range(64)]
    return one_time_pad_keys[63][0]


def solve_part_2(salt: str) -> int:
    """"""
    key_generator = generate_one_time_pad_keys(salt=salt, hash_function=stretched_md5_message_digest)
    one_time_pad_keys = [next(key_generator) for _ in range(64)]
    return one_time_pad_keys[63][0]


@functools.cache
def md5_message_digest(salt: str, idx: int) -> str:
    """"""
    message = salt + str(idx)
    md5_hash = hashlib.md5(message.encode())
    return md5_hash.hexdigest()


def generate_one_time_pad_keys(salt: str, hash_function: Callable[[str, int], str]=md5_message_digest) -> Iterator[tuple[int, str]]:
    """Generate a given number of one-time pad keys from a pre-arranged salt
    A hash/message digest is a key only if:
    - It contains three of the same character in a row, like 777. Only consider the first such triplet in a hash.
    - One of the next 1000 hashes in the stream contains that same character five times in a row, like 77777.
    """
    for i in range(0, 1 << 32):
        candidate_key = hash_function(salt=salt, idx=i)
        m = re.search(r"(\w)\1\1", candidate_key)
        if m:
            repeated_char = m.group(1)
            for offset in range(1, 1001):
                message_digest = hash_function(salt, idx=i+offset)
                if re.search(repeated_char + r"{5}", message_digest):
                    yield i, candidate_key
                    break


@functools.cache
def stretched_md5_message_digest(salt: str, idx: int) -> str:
    """
    To implement key stretching, whenever you generate a hash, before you use it, you first find the MD5 hash of that hash, then the MD5 hash of that hash, and so on, a total of 2016 additional hashings.
    Always use lowercase hexadecimal representations of hashes.
    In the end, you find the original hash (one use of MD5), then find the hash-of-the-previous-hash 2016 times, for a total of 2017 uses of MD5.
    """
    message_digest = md5_message_digest(salt=salt, idx=idx)
    for _ in range(2016):
        message_digest = hashlib.md5(message_digest.encode()).hexdigest()
    return message_digest


if __name__ == "__main__":
    main()
