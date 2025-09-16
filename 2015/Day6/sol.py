#!/usr/bin/env python3
"""
--- Day 6: Probably a Fire Hazard ---
https://adventofcode.com/2015/day/6
Commentary
For me, the main theme of today's puzzle is abstraction (benefits and drawbacks, which abstractions to make).
I wonder whether two concrete implementations of a light grid class (for part 1, 2, respectively)
with common method names for the 'turn on', turn off', and 'toggle' operations, both potentially inheriting
from a partially abstracted parent class would be better for readability, maintainability, flexibility.
This would depend on the hypothetical wider context within which the puzzle/project lives.
I find the disconnect in part 2 between the phrases 'turn on', turn off', and 'toggle' and their
implementation meanings ('turn up', 'turn down', and 'turn up twice') somewhat irksome
due the naming confusion/unintuitive behaviour it would cause in a real setting.
"""
from __future__ import annotations
from collections.abc import Callable
import os


DIRPATH = os.path.dirname(__file__)


class LightGrid:
    """2D array (list of lists) of integers, representing the state of a light grid.
    For part 1, a lights value has the meaning 1 = On, 0 = Off.
    For part 2, the values represent an individual light's brightness setting.
    """
    def __init__(self, n_rows: int=1000, n_cols: int=1000):
        """Create a LightGrid of the specified size. The lights all start turned off.
        By default, creates an array of one million lights in a 1000x1000 grid.
        """
        self.state: list[list[bool]] = [[0 for _ in range(n_cols)] for _ in range(n_rows)]

    def set_brightness_single(self, brightness: int, i: int, j: int):
        self.state[i][j] = brightness

    def increase_brightness_single(self, brightness: int, i: int, j: int):
        self.state[i][j] += brightness

    def decrease_brightness_single(self, brightness: int, i: int, j: int):
        """Decrease the brightness of the light at position i,j, to a minimum of zero"""
        self.state[i][j] = max(self.state[i][j] - brightness, 0)

    def array_operation(self, element_op: Callable[[LightGrid, int, int]], start: tuple[int, int], end: tuple[int, int]):
        """Execute an elementwise operation on an inclusive range given as coordinate pairs.
        Each coordinate pair represents opposite corners of a rectangle, inclusive.
        """
        for i in range(start[0], end[0]+1):
            for j in range(start[1], end[1]+1):
                element_op(self, i,j)

    def total_brightness(self) -> int:
        return sum(sum(row) for row in self.state)


def parse_array_switch_instruction(instruction: str) -> tuple[str, tuple[int, int], tuple[int, int]]:
    # Separate string components
    rest, _, end_s = instruction.partition(" through ")
    rest, start_j = rest.split(",")
    op_name, start_i = rest.rsplit(" ", maxsplit=1)

    # Convert to return types
    start_coords: tuple[int, int] = int(start_i), int(start_j)
    end_coords: tuple[int, int] = tuple(map(int, end_s.split(",")))

    return op_name, start_coords, end_coords


def main():
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        instructions: list[str] = [line for line in file]

    operations: dict[str, dict[str, Callable[[LightGrid, int, int]]]] = {
        "Part 1": {
            "turn on": lambda light_grid, i, j : LightGrid.set_brightness_single(light_grid, 1, i, j),
            "turn off": lambda light_grid, i, j : LightGrid.set_brightness_single(light_grid, 0, i, j),
            "toggle": lambda light_grid, i, j : LightGrid.set_brightness_single(light_grid, 1 - light_grid.state[i][j], i, j)
        },
        "Part 2": {
            "turn on": lambda light_grid, i, j : LightGrid.increase_brightness_single(light_grid, 1, i, j),
            "turn off": lambda light_grid, i, j : LightGrid.decrease_brightness_single(light_grid, 1, i, j),
            "toggle": lambda light_grid, i, j : LightGrid.increase_brightness_single(light_grid, 2, i, j)
        }
    }
    light_grids = {"Part 1": LightGrid(), "Part 2": LightGrid()}

    for instruction in instructions:
        op_name, start_coords, end_coords = parse_array_switch_instruction(instruction)
        for part, light_grid in light_grids.items():
            operation = operations[part][op_name]
            light_grid.array_operation(operation, start_coords, end_coords)

    print(f"Part 1: After the light display, {light_grids['Part 1'].total_brightness()} lights are lit.")
    print(f"Part 2: After the light display, the total brightness is {light_grids['Part 2'].total_brightness()}.")


if __name__ == "__main__":
    main()
