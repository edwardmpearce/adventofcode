#!/usr/bin/env python3
"""
--- Day 1: Secret Entrance ---
https://adventofcode.com/2025/day/1
Part 1: Modular arithmetic (remainders)
Part 2: Quotients and remainders, edge cases

References
- https://docs.python.org/3/tutorial/classes.html#generators
- https://docs.python.org/3/library/functions.html#divmod
- https://en.wikipedia.org/wiki/Rotary_combination_lock
"""
import os
from collections.abc import Iterator


DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    safe_dial: RotataryDial = RotataryDial(num_positions=100, start_position=50)
    ends_on_zero_count: int = 0
    clicks_at_zero_total: int = 0

    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        for direction, distance in parse_rotation_instructions(file):
            dial_position, clicks_at_zero_count = safe_dial.rotate(direction, distance)
            if dial_position == 0:
                ends_on_zero_count += 1
            clicks_at_zero_total += clicks_at_zero_count

    print(f"Part 1: The number of times the dial is left pointing at 0 after any rotation in the sequence is {ends_on_zero_count}")
    print(f"Part 2: The number of times the dial points at 0 during the rotation sequence is {clicks_at_zero_total}")


def parse_rotation_instructions(instructions: Iterator[str]) -> Iterator[tuple[int, int]]:
    """Convert instructions for rotating a dial on a safe a distance to the left or right into integers to be added to the current dial position"""
    directions = {'L': -1, 'R': 1}
    for instruction in instructions:
        direction: int = directions[instruction[0]]
        distance: int = int(instruction[1:])
        yield direction, distance


class RotataryDial:
    def __init__(self, num_positions: int, start_position: int):
        self.num_positions: int = num_positions
        self.current_position: int = start_position
    
    def rotate(self, direction: int, distance: int) -> tuple[int, int]:
        """Update dial position and return together with the number of times any click causes the dial to point at 0, 
        regardless of whether it happens during a rotation or at the end of one.
        """
        assert direction in {-1,1} and distance > 0
        complete_turns, relative_distance = divmod(distance, self.num_positions)
        relative_rotation: int = direction * relative_distance
        new_position = self.current_position + relative_rotation
        # If starting from position 0, no relative rotation would cause a further click at 0
        # Otherwise, check whether the relative rotation causes the dial to pass or end on position 0
        clicks_at_zero_count = complete_turns if (self.current_position == 0 or 0 < new_position < self.num_positions) else complete_turns + 1
        self.current_position = new_position % self.num_positions
        return self.current_position, clicks_at_zero_count


if __name__ == "__main__":
    main()
