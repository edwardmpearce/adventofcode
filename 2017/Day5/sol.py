#!/usr/bin/env python3
"""
--- Day 5: A Maze of Twisty Trampolines, All Alike ---
https://adventofcode.com/2017/day/5
Themes: Data structures, temporary variables, execution order
"""
import os
from collections.abc import Callable

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        # instructions: dict[int, int] = dict(enumerate(map(int, file)))
        instructions: dict[int, int] = {i: int(line) for i, line in enumerate(file)}

    print(f"Part 1: The answer is {solve_part_1(instructions)}")
    print(f"Part 2: The answer is {solve_part_2(instructions)}")


def jump_program_with_update_rule(instructions: dict[int, int], update_rule: Callable[[int], int]) -> int:
    """Return the number of steps required to exit a list of relative offset jump instructions with a post-jump rule.
    After each jump instruction is executed, its offset will be increased by an amount following a rule based on
    the current offset value.
    """
    n_steps: int = 0
    position: int = 0
    while position in instructions:
        # Get current offset, update offset at current position, then jump position
        offset: int = instructions[position]
        instructions[position] += update_rule(offset)
        position += offset
        n_steps += 1
    return n_steps


def solve_part_1(instructions: dict[int, int]) -> int:
    """Return the number of steps required to exit a list of relative offset jump instructions.
    After each jump instruction is executed, its offset value is increased by 1.
    """
    def constant_increment(offset: int) -> int:
        return 1
    return jump_program_with_update_rule(instructions.copy(), update_rule=constant_increment)


def solve_part_2(instructions: dict[int, int]) -> int:
    """Return the number of steps required to exit a list of relative offset jump instructions with a post-jump rule.
    After executing a jump instruction, the offset value is incremented if less than 3, else decremented.
    """
    def offset_update_rule(offset: int) -> int:
        """If the offset is three or more, decrease it by 1. Otherwise, increase it by 1."""
        return 1 if offset < 3 else -1
    return jump_program_with_update_rule(instructions.copy(), update_rule=offset_update_rule)


if __name__ == "__main__":
    main()
