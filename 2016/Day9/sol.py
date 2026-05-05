#!/usr/bin/env python3
"""
--- Day 9: Explosives in Cyberspace ---
https://adventofcode.com/2016/day/9
Decompress a text file containing markers indicating repeated subsequences

References
- https://docs.python.org/3/library/re.html
- https://docs.python.org/3/howto/regex.html
"""
import os
from collections.abc import Iterator
import re

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        compressed_text = file.read().strip()

    print(f"Part 1: The answer is {len(decompress(compressed_text))}")
    print(f"Part 2: The answer is {calculate_recursive_decompressed_length(compressed_text)}")


def decompress(compressed_text: str) -> str:
    """Decompress a text sequence containing markers of the form (kxn) which indicate the repetition of the k characters after the marker for n times.
    Then, continue reading the file after the repeated data. The marker itself is not included in the decompressed output.
    If parentheses or other characters appear within the data referenced by a marker, treat it like normal data, not a marker, and then resume looking for markers after the decompressed section.
    """
    return "".join(find_all_decompressed_sequences(compressed_text))


def find_all_decompressed_sequences(compressed_text: str) -> Iterator[str]:
    """Yield all decompressed components of a text sequence containing markers of the form (kxn) which indicate the repetition of the k characters after the marker for n times.
    Then, continue reading the file after the repeated data. The marker itself is not included in the decompressed output.
    If parentheses or other characters appear within the data referenced by a marker, treat it like normal data, not a marker, and then resume looking for markers after the decompressed section.
    """
    ptr: int = 0
    pattern = re.compile(r"\((\d+)x(\d+)\)")

    while dupe_marker := pattern.search(compressed_text, pos=ptr):
        # Yield any non-duplicated characters between the pointer and the next marker
        yield compressed_text[ptr:dupe_marker.start()]
        # Parse the marker data and yield n repetitions of the k characters following the end of the marker
        seq_length, n_repeats = map(int, dupe_marker.groups())
        yield compressed_text[dupe_marker.end():dupe_marker.end()+seq_length] * n_repeats
        # Move the pointer to the end of the repeated subsequence
        ptr = dupe_marker.end() + seq_length
    # No duplication markers remain between the pointer and the end of string
    yield compressed_text[ptr:len(compressed_text)]
    ptr = len(compressed_text)


def calculate_recursive_decompressed_length(compressed_text: str) -> int:
    """Calculate the length of a decompressed text sequence.
    Where the input text contains markers of the form (kxn), we take the subsequent k characters after the marker and repeat them n times.
    Then, continue reading the file after the repeated data. The marker itself is not included in the decompressed output.
    Markers within decompressed data are decompressed.
    """
    decompressed_length: int  = 0
    ptr: int = 0
    pattern = re.compile(r"\((\d+)x(\d+)\)")

    while dupe_marker := pattern.search(compressed_text, pos=ptr):
        # Count any non-duplicated characters between the pointer and the next marker
        decompressed_length += dupe_marker.start() - ptr
        # Parse the marker data
        seq_length, n_repeats = map(int, dupe_marker.groups())
        # Count n repetitions of the result of decompressing the k characters following the end of the marker
        decompressed_length += n_repeats * calculate_recursive_decompressed_length(compressed_text[dupe_marker.end():dupe_marker.end()+seq_length])
        # Move the pointer to the end of the repeated subsequence
        ptr = dupe_marker.end() + seq_length
    # Count the remaining characters between the pointer and the end of string
    decompressed_length += len(compressed_text) - ptr
    ptr = len(compressed_text)
    return decompressed_length


if __name__ == "__main__":
    main()
