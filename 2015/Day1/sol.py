#!/usr/bin/env python3
"""
--- Day 1: Not Quite Lisp ---
https://adventofcode.com/2015/day/1

Commentary
For part 1, the floor reached by following the instructions can be determined either by
calculating the floor number at each step in the path through the instruction set directly
or counting the number of 'up' and 'down' operations and taking the difference.
Both methods require reading the entire instruction set, and the latter requires
slightly more memory and operations whilst providing different information about the inputs.

For part 2, we define a generator function which yields the path through the floors
made by following a set of up/down instructions indicated by '(' and ')' characters, respectively.
When the path first enters the basement (floor `-1`), we print the corresponding character position
and then break out of the loop so that it is not necesary to read the entire instruction set.

It is possible to find the solutions to part 1 and part 2 in a single loop through the instruction string
by using an additional boolean `visited_basement` variable and additional comparison operations in each iteration.

References
- https://docs.python.org/3/tutorial/classes.html#generators
"""
import os
from collections import Counter
from collections.abc import Iterator

DIRPATH = os.path.dirname(__file__)


def main():
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        instructions = file.read()

    direction_counts = Counter(instructions)
    print(f"Part 1: Following the instructions results in floor {direction_counts['('] - direction_counts[')']}")

    for pos, floor in enumerate(generate_floor_path(instructions), 1):
        if floor < 0:
            print(f"Part 2: Basement first entered at position {pos}")
            break
    else:
        print("Part 2: Floor path from instruction set does not enter basement")

    print(f"Floors climbed: {direction_counts['(']}, Floors descended: {direction_counts[')']}")
    print(f"Highest floor visited: {max(generate_floor_path(instructions))}, Lowest floor visited: {min(generate_floor_path(instructions))}")


def generate_floor_path(instructions: str) -> Iterator[int]:
    current_floor = 0
    for char in instructions:
        if char == '(':
            current_floor += 1
        elif char == ')':
            current_floor -= 1
        yield current_floor


if __name__ == "__main__":
    main()
