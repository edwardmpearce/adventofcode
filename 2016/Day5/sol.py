#!/usr/bin/env python3
"""
--- Day 5: How About a Nice Game of Chess? ---
https://adventofcode.com/2016/day/5
Introduction to cryptographic hashing applications, MD5 algorithm, hexademical
Other possible themes include utilizing third-party code, unit testing
Compare and contrast with 2015 Day 4

References
- https://en.wikipedia.org/wiki/MD5
- https://en.wikipedia.org/wiki/Hexadecimal
- https://www.google.com/search?q=python+md5
- https://docs.python.org/3/library/hashlib.html
- https://www.reddit.com/r/adventofcode/comments/18oki0y/2015_day_4_would_you_roll_your_own_md5/
- https://www.geeksforgeeks.org/python/md5-hash-python/
- https://en.wikipedia.org/wiki/Cryptographic_nonce
- https://cryptopals.com/
- https://docs.python.org/3/library/itertools.html#itertools.islice
"""
import os
from collections.abc import Iterator
import itertools
import hashlib


DIRPATH = os.path.dirname(__file__)


def main():
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        door_id = file.read()

    print(f"Part 1: The answer is {solve_part_1(door_id, difficulty=5, password_length=8)}")
    print(f"Part 2: The answer is {solve_part_2(door_id, difficulty=5, password_length=8)}")


def solve_part_1(door_id: str, difficulty: int, password_length: int) -> str:
    """Find the password to a part-1 door given its Door ID.

    The password for the door is generated one character at a time by finding the MD5 hash of the input Door ID with an increasing integer index (starting with 0).
    A hash indicates the next character in the password if its hexadecimal representation starts with n zeroes, where n is the `difficulty`.
    If it does, the (n+1)-th character in the hash is the next character of the password.
    """
    if not (isinstance(difficulty, int) and 0 <= difficulty <= 31):
        raise ValueError("Difficulty must be an integer between 0 and 31")
    if not (isinstance(password_length, int) and password_length >= 0):
        raise ValueError("Password length must be an integer greater than or equal to 0")

    return "".join([digest[difficulty] for digest in itertools.islice(generate_valid_md5_hash(door_id, difficulty), password_length)])


def solve_part_2(door_id: str, difficulty: int, password_length: int) -> str:
    """Find the password to a part-2 door given its Door ID.

    The password for the door is generated one character at a time by finding the MD5 hash of the input Door ID with an increasing integer index (starting with 0).
    A hash indicates the next character in the password if its hexadecimal representation starts with n zeroes, where n is the `difficulty`.
    If it does, the (n+1)-th character represents a character position in the password, and (n+2)-th character is the character to put in that position.
    Uses only the first result for each position, and ignores invalid positions.
    If the (n+1)-th character does not indicate a valid position in the password (between 0 and `password_length - 1`), then proceed to the next valid hash.
    """
    if not (isinstance(difficulty, int) and 0 <= difficulty <= 30):
        raise ValueError("Difficulty must be an integer between 0 and 30")
    if not (isinstance(password_length, int) and 0 <= password_length <= 10):
        raise ValueError("Password length must be an integer between 0 and 10")
    if password_length == 0:
        return ""

    password_chars: list[tuple[str, str]] = []
    valid_positions: set[str] = {str(i) for i in range(password_length)}
    for candidate_hash in generate_valid_md5_hash(door_id, difficulty):
        position: str = candidate_hash[difficulty]
        if position in valid_positions:
            password_chars.append((position, candidate_hash[difficulty+1]))
            valid_positions.remove(position)
        if not valid_positions:
            # All password characters have been found. Sort by position and join to return.
            return "".join([char for pos, char in sorted(password_chars)])


def generate_valid_md5_hash(key: str, difficulty: int) -> Iterator[str]:
    """Yield hashes of the input key concatenated with an increasing integer index (starting with 0)
    where the hash's hexadecimal representation starts with n zeroes, for some difficulty parameter `n`.

    An arbitrary upper bound is used for the size of the search space to prevent the hypothetical risk of an infinite loop
    """
    if not (isinstance(difficulty, int) and 0 <= difficulty <= 32):
        raise ValueError("Difficulty must be an integer between 0 and 32")

    for i in range(0, 1 << 32):
        message = key + str(i)
        md5_hash = hashlib.md5(message.encode())
        message_digest = md5_hash.hexdigest()
        if message_digest.startswith("0" * difficulty):
            yield message_digest


if __name__ == "__main__":
    main()
