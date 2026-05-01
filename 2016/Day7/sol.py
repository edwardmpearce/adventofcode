#!/usr/bin/env python3
"""
--- Day 7: Internet Protocol Version 7 ---
https://adventofcode.com/2016/day/7
String pattern matching

References
- https://docs.python.org/3/library/re.html
"""
import os
import re

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        addresses: list[str] = [line.strip() for line in file]

    print(f"Part 1: The answer is {sum(supports_tls(address) for address in addresses)}")
    print(f"Part 2: The answer is {sum(supports_ssl(address) for address in addresses)}")


def supports_tls(address: str) -> bool:
    """Identify whether an IP address supports TLS (transport-layer snooping).
    An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA.
    An ABBA is any four-character sequence which consists of a pair of two different characters followed by the reverse of that pair, such as xyyx or abba. 
    However, the IP also must not have an ABBA within any hypernet sequences, which are contained by square brackets.
    """
    sequences: list[str] = re.split(r"[[\]]", address)
    return any(has_abba(seq) for seq in sequences[::2]) and not any(has_abba(seq) for seq in sequences[1::2])


def has_abba(sequence: str) -> bool:
    """An ABBA is any four-character sequence which consists of a pair of two different characters followed by the reverse of that pair, such as xyyx or abba."""
    pattern = re.compile(r"([a-z])([a-z])\2\1")
    return any(pattern.match(sequence[i:i+4]) and (sequence[i] != sequence[i+1]) for i in range(len(sequence) - 3))


def supports_ssl(address: str) -> bool:
    """Identify whether an IP address supports SSL (super-secret listening).
    An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in the supernet sequences (outside any square bracketed sections),
    and a corresponding Byte Allocation Block, or BAB, anywhere in the hypernet sequences. 
    An ABA is any three-character sequence which consists of the same character twice with a different character between them, such as xyx or aba. 
    A corresponding BAB is the same characters but in reversed positions: yxy and bab, respectively.
    """
    sequences: list[str] = re.split(r"[[\]]", address)
    supernet_abas = {aba for seq in sequences[::2] for aba in find_aba_sequences(seq)}
    hypernet_babs = {bab for seq in sequences[1::2] for bab in find_aba_sequences(seq)}
    corresponding_babs = {aba[1] + aba[0] + aba[1] for aba in supernet_abas}
    return bool(corresponding_babs & hypernet_babs)


def find_aba_sequences(sequence: str) -> set[str]:
    """Return the set of unique substrings matching the pattern ABA (or equivalently BAB) within a text sequence (such ABA subsequences may overlap within the larger string).
    An ABA is any three-character sequence which consists of the same character twice with a different character between them, such as xyx or aba.
    """
    return {sequence[i:i+3] for i in range(len(sequence) - 2) if (sequence[i] == sequence[i+2]) and (sequence[i] != sequence[i+1])}


if __name__ == "__main__":
    main()
