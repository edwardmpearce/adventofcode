#!/usr/bin/env python3
"""
--- Day 1: No Time for a Taxicab ---
https://adventofcode.com/2016/day/1
Part 1: Follow instructions to move along a 2D grid of city streets
Part 2: Find the first location visited twice (not only including intersections for turning)
"""
import os
from dataclasses import dataclass

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        instructions = parse_puzzle_input(file.read())

    print(f"Part 1: The answer is {solve_part_1(instructions)}")
    print(f"Part 2: The answer is {solve_part_2(instructions)}")


def parse_puzzle_input(puzzle_input: str) -> list[tuple[str, int]]:
    """Parse puzzle input string into list of pairs of turn directions and travel distances (number of blocks to walk)"""
    return [(instruction[0], int(instruction[1:])) for instruction in puzzle_input.split(", ")]


def solve_part_1(instructions: list[tuple[str, int]]) -> int:
    """Follow the instructions to reach the destination, then return the length of the shortest path to the destination from the origin (L1 taxicab metric)"""
    taxi = Taxi()
    for direction, distance in instructions:
        taxi.turn(direction)
        taxi.drive(distance)
    return abs(taxi.position)


def solve_part_2(instructions: list[tuple[str, int]]) -> int:
    """Following the instructions moving one unit distance at a time, return the length of the shortest path from the origin
    to the first location that is visited twice (L1 taxicab metric)
    """
    taxi = Taxi()
    visited: set[Vector] = {taxi.position}
    for direction, distance in instructions:
        taxi.turn(direction)
        # Drive distince in one unit intervals, recording visited positions
        for _ in range(distance):
            taxi.drive(1)
            if taxi.position in visited:
                return abs(taxi.position)
            visited.add(taxi.position)
    return abs(taxi.position)


@dataclass(frozen=True)
class Vector:
    i: int
    j: int

    def __add__(self, other):
        return Vector(self.i + other.i, self.j + other.j)

    def __mul__(self, scalar: int):
        return Vector(self.i * scalar, self.j * scalar)

    def __rmul__(self, scalar: int):
        """Swap order of operands to re-use implementation of __mul__
        https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types
        """
        return self * scalar

    def __abs__(self):
        return abs(self.i) + abs(self.j)


# List of unit vectors representing the cardinal directions on a 2D grid
CARDINAL_DIRECTIONS: list[Vector] = [
    Vector(0,1), # North
    Vector(1,0), # East
    Vector(0,-1), # South
    Vector(-1,0) # West
]


@dataclass
class Taxi:
    """Taxi which can move along a 2D grid of streets
    The `facing` attribute represents the number of quarter-turns clockwise from North
    i.e. North = 0, East = 1, South = 2, West = 3
    """
    position: Vector = Vector(0,0)
    facing: int = 0

    def turn(self, direction: str):
        """Turn left (L) or right (R) to change direction"""
        self.facing = (self.facing + {"R": 1, "L": -1}[direction]) % 4

    def drive(self, distance: int):
        """Drive forward in the direction of travel by a given distance"""
        self.position += CARDINAL_DIRECTIONS[self.facing % 4] * distance


if __name__ == "__main__":
    main()
