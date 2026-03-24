#!/usr/bin/env python3
"""
--- Day 2: Bathroom Security ---
https://adventofcode.com/2016/day/2
Part 1: Simulate pressing buttons on a numeric keypad with digits 1-9
Part 2: Simulate pressing buttons on a diamond shaped keypad with digits from 1-9, A-D

References
- https://realpython.com/instance-class-and-static-methods-demystified/#when-to-use-class-methods
"""
import os
from dataclasses import dataclass
from typing import Self

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        instructions: list[str] = [line.strip() for line in file]

    print(f"Part 1: The answer is {Keypad.simple().find_key_sequence(start=(1, 1), instructions=instructions)}")
    print(f"Part 2: The answer is {Keypad.diamond_hex().find_key_sequence(start=(2, 0), instructions=instructions)}")


@dataclass(frozen=True)
class Keypad:
    keys: dict[tuple[int, int], str]

    def is_valid_position(self, x: int, y: int) -> bool:
        """Returns True if (x, y) is a valid position on the keypad"""
        return (x, y) in self.keys

    def validate_position(self, x: int, y: int) -> tuple[int, int]:
        """Returns (x, y) if it is a valid position on the keypad, else raises ValueError"""
        if not self.is_valid_position(x, y):
            raise ValueError(f"{(x, y)} is not a valid position on the keypad")
        return (x, y)

    def press(self, x: int, y: int) -> str:
        """Return the value on the key at position (x, y), if valid, else raise ValueError."""
        self.validate_position(x, y)
        return self.keys[(x, y)]

    def find_key_sequence(self, start: tuple[int, int], instructions: list[str]) -> str:
        """Return a sequence of key values obtained by following a set a instructions for moving between adjacent buttons.

        Each button to be pressed can be found by starting on the previous button and moving to adjacent buttons on the keypad:
        U moves up, D moves down, L moves left, and R moves right.
        Each line of instructions corresponds to one button, starting at the previous button; press whatever button you're on at the end of each line.
        If a move doesn't lead to a button, ignore it.
        """
        x, y = self.validate_position(*start)
        sequence: str = ""
        for instruction in instructions:
            for char in instruction:
                match char:
                    case "U":
                        new_x, new_y = x - 1, y
                    case "L":
                        new_x, new_y = x, y - 1
                    case "D":
                        new_x, new_y = x + 1, y
                    case "R":
                        new_x, new_y = x, y + 1
                if self.is_valid_position(new_x, new_y):
                    x, y = new_x, new_y
            sequence += self.press(x, y)
        return sequence

    @classmethod
    def simple(cls) -> Self:
        """Simple numeric keypad for numbers 1-9 as [[1, 2, 3], [4, 5, 6], [7, 8, 9]]"""
        return cls({(x, y): str(x * 3 + y + 1) for x in range(3) for y in range(3)})

    @classmethod
    def diamond_hex(cls) -> Self:
        """Diamond shaped keypad with 13 keys from 1-9, A-D"""
        numeric_keys: dict[tuple[int, int], str] = {(i, 2 - i + j): str(i*i + j + 1) for i in range(3) for j in range(2*i+1)}
        alphabetical_keys: dict[tuple[int, int], str] = {(3, 1): "A", (3, 2): "B", (3, 3): "C", (4, 2): "D", }
        return cls(numeric_keys | alphabetical_keys)


def validate_test_setup(keypad: Keypad, start: tuple[int, int]) -> tuple[Keypad, tuple[int, int]]:
    """Tests start on the "5" button"""
    start_value = keypad.press(*start)
    assert start_value == "5", f"Key at position {start} has value {start_value}. Expected:'5'"
    return keypad, start


def test_solve_part_1():
    """Part 1 Test Case"""
    instructions: list[str] = ["ULL", "RRDDD", "LURDL", "UUUUD"]
    keypad, start = validate_test_setup(Keypad.simple(), (1, 1))
    actual_result = keypad.find_key_sequence(start, instructions)
    assert actual_result == "1985", f"Actual: {actual_result}, Expected '1985'"


def test_solve_part_2():
    """Part 2 Test Case"""
    instructions: list[str] = ["ULL", "RRDDD", "LURDL", "UUUUD"]
    keypad, start = validate_test_setup(Keypad.diamond_hex(), (2, 0))
    actual_result = keypad.find_key_sequence(start, instructions)
    assert actual_result == "5DB3", f"Actual: {actual_result}, Expected '5DB3'"


if __name__ == "__main__":
    test_solve_part_1()
    test_solve_part_2()
    main()
