#!/usr/bin/env python3
"""
--- Day 3: Perfectly Spherical Houses in a Vacuum ---
https://adventofcode.com/2015/day/3
Part 1: Count distinct points visited on a path in a 2D grid
Part 1: Count distinct points visited by a pair of paths in a 2D grid

Commentary
Today's puzzle can be considered an extension of the ideas from 2015 Day 1 into 2-dimensional space
Useful ideas: Customizing loops (different starting point, step size); use of `set` type to get unique values
"""
import os
from dataclasses import dataclass
from collections.abc import Iterator

DIRPATH = os.path.dirname(__file__)


@dataclass(frozen=True)
class Vector:
    i: int
    j: int

    def __add__(self, other):
        return Vector(self.i + other.i, self.j + other.j)

    def __sub__(self, other):
        return Vector(self.i - other.i, self.j - other.j)


def generate_travel_path(instructions: str) -> Iterator[Vector]:
    directions: dict[str, Vector] = {
        '^': Vector(0,1),
        'v': Vector(0,-1),
        '>': Vector(1,0),
        '<': Vector(-1,0),
    }

    location: Vector = Vector(0,0)
    yield location
    for char in instructions:
        location += directions[char]
        yield location


def solution_part_1(instructions: str):
    num_distinct_locations_visited: int = len(set(generate_travel_path(instructions)))
    print(f"Part 1: The number of distinct locations visited is {num_distinct_locations_visited}")
    

def solution_part_2(instructions: str):
    """Part 2: Distinct locations visited by two agents with same starting location
    One agent follows instructions with odd index and the other follows instructions with even index
    """
    houses_santa_visits = set(generate_travel_path(instructions[::2]))
    houses_robo_santa_visits = set(generate_travel_path(instructions[1::2]))
    houses_visited = houses_santa_visits | houses_robo_santa_visits
    print(f"Part 2: The number of distinct locations visited is {len(houses_visited)}")


def main():
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        instructions = file.read()

    solution_part_1(instructions)
    solution_part_2(instructions)


if __name__ == "__main__":
    main()
