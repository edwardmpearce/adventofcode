#!/usr/bin/env python3
"""
--- Day 4: Security Through Obscurity ---
https://adventofcode.com/2016/day/4
Part 1: Text parsing, frequency analysis, checksum validation
Part 2: Caesar cipher decryption

References
- Regular expressions for pattern matching and substiution
  - https://docs.python.org/3/library/re.html
  - https://docs.python.org/3/howto/regex.html#regex-howto
- Counter class to find most common letters in string
  - https://docs.python.org/3/library/collections.html
- Built-in functions for sorting; shifting characters with `ord` and `chr`
  - https://docs.python.org/3/library/functions.html
- https://en.wikipedia.org/wiki/Caesar_cipher
"""
import os
from dataclasses import dataclass
from typing import Self
import re
from collections import Counter


DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Parse puzzle input file into list of RoomData class instances
    # consisting of an encrypted room name, a sector ID, and a checksum
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        rooms: list[RoomData] = [RoomData.from_string(line) for line in file]

    print(f"Part 1: The sum of sector IDs across the real (not decoy) rooms is {sum(room.sector_id for room in rooms if room.is_valid())}")

    for room in rooms:
        if room.is_valid() and "north" in room.decrypt():
            print(f"Part 2: North Pole objects are stored in the room '{room.decrypt()}' with sector ID {room.sector_id}")


@dataclass(frozen=True)
class RoomData:
    encrypted_name: str
    sector_id: int
    checksum: str

    @classmethod
    def from_string(cls, data: str) -> Self:
        """Extract room data from a formatted string.
        Each room consists of an encrypted name (lowercase letters separated by dashes) followed by a dash, a sector ID, and a checksum in square brackets.
        """
        m = re.match(r"([a-z-]+)-([0-9]+)\[([a-z]+)\]", data)
        if not m:
            raise ValueError(f"Could not parse room data string '{data}'")
        return cls(encrypted_name=m[1], sector_id=int(m[2]), checksum=m[3])

    def is_valid(self) -> bool:
        """A room is real (not a decoy) if the checksum is the five most common letters in the encrypted name, in order, with ties broken by alphabetization."""
        return top_5_letters(self.encrypted_name) == self.checksum

    def decrypt(self) -> str:
        """To decrypt a room name, rotate each letter forward through the alphabet a number of times equal to the room's sector ID."""
        return "".join([" " if char == "-" else right_shift_char(char, self.sector_id) for char in self.encrypted_name])


def top_5_letters(text: str) -> str:
    """Return the five most common letters in the input string (case-insensitive), in order, with ties broken by alphabetization."""
    letters = re.sub(r"[^a-z]", "", text.lower()) # Remove characters which are not letters
    # Sort letters by frequency (descending), with ties broken by alphabetization (ascending).
    sorted_letter_counts = sorted(Counter(letters).items(), key=lambda char_count: (-char_count[1], char_count[0]))
    # Convert to string and truncate to top 5 chars
    return "".join([char for char, count in sorted_letter_counts])[:5]


def right_shift_char(char: str, shift: int ) -> str:
    """Rotate the input lowercase letter forward through the alphabet a number of times equal to the shift parameter."""
    return chr(ord('a') + (ord(char) - ord('a') + shift) % 26)


if __name__ == "__main__":
    main()
