#!/usr/bin/env python3
"""
--- Day 8: Two-Factor Authentication ---
https://adventofcode.com/2016/day/8
Simulate a small pixelated LCD screen

References
- Structural Pattern Matching
  - https://peps.python.org/pep-0636/
- Regular Expressions
  - https://docs.python.org/3/library/re.html
  - https://docs.python.org/3/howto/regex.html
"""
import os
from dataclasses import dataclass
import re
import time

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        instructions: list[str] = file.read().splitlines()

    screen = Screen(height=6, width=50)
    screen.simulate_display_instructions(instructions)
    print(f"Part 1: After following the instructions, the number of lit pixels is {sum(px for row in screen.pixels for px in row)}.")


@dataclass
class Screen:
    """Dataclass representing a small LCD screen of pixels"""
    height: int
    width: int

    def __post_init__(self):
        """Create a grid of binary pixels, all of which start turned off"""
        if self.height <= 0 or self.width <= 0:
            raise ValueError("Screen height and width must be positive integers")
        self.pixels: list[list[int]] = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def display(self, on: str = '#', off: str = '.') -> str:
        """Convert pixel grid values to string for printing, with option to configure how 'on' and 'off' states are displayed"""
        return "\n".join(["".join([{0: off, 1: on}[px] for px in row]) for row in self.pixels])

    def rect_on(self, rect_width: int, rect_height: int) -> None:
        """Turn on all of the pixels in a rectangle at the top-left of the screen which is A wide and B tall"""
        for row in self.pixels[:rect_height]:
            row[:rect_width] = [1 for _ in range(rect_width)]

    def rotate_row(self, row_idx: int, shift: int) -> None:
        """Shift all of the pixels in a row right by a given number of pixels.
        Pixels that would fall off the right end appear at the left end of the row.
        """
        self.pixels[row_idx] = rotate_list(self.pixels[row_idx], shift)

    def rotate_column(self, col_idx: int, shift: int) -> None:
        """Shift all of the pixels in a column down by a given number of pixels.
        Pixels that would fall off the bottom appear at the top of the column.
        """
        for row, val in zip(self.pixels, rotate_list([row[col_idx] for row in self.pixels], shift)):
            row[col_idx] = val

    def parse_and_apply_instruction(self, instruction: str) -> None:
        """Parse an instruction string and apply the specified operation"""
        pattern = re.compile(r"(rect|rotate row|rotate column)\D+(\d+)\D+(\d+)")
        m = pattern.match(instruction)
        if not m:
            raise ValueError(f"Could not parse instruction '{instruction}'")
        match m.groups():
            case ("rect", A, B):
                self.rect_on(rect_width=int(A), rect_height=int(B))
            case ("rotate row", A, B):
                self.rotate_row(row_idx=int(A), shift=int(B))
            case ("rotate column", A, B):
                self.rotate_column(col_idx=int(A), shift=int(B))

    def simulate_display_instructions(self, instructions: list[str], delay: float=0.5) -> None:
        """Animate applying a series of instructions by displaying screen state after each operation with a small delay"""
        for instruction in instructions:
            # Clear the terminal/console before each iteration to create an animated visual effect
            # https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
            print(chr(27) + "[2J")
            print(instruction)
            self.parse_and_apply_instruction(instruction)
            # Display lit pixels by the large green circle unicode character and use double spacing for unlit pixels for visual alignment
            print(self.display(off='  ', on="\U0001F7E2"))
            time.sleep(delay)


def rotate_list(l: list, shift: int) -> list:
    """Cyclically shift all of the elements in a list to the right by a given index."""
    split_idx: int = len(l) - shift
    return l[split_idx:] + l[:split_idx]


if __name__ == "__main__":
    main()
