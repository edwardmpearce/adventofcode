#!/usr/bin/env python3
"""
--- Day 11: Cosmic Expansion ---
https://adventofcode.com/2023/day/11
Part 1: Sum of L1 distances between all pairs of points
Part 2: Stress-testing for memory-efficient implementation
"""
from dataclasses import dataclass


def main():
    # Locate galaxies and expanding space in the input telescope image
    galaxies, space_rows, space_columns = locate_galaxies_and_expanding_space("input.txt")

    for i, expansion_factor in [(1, 2), (2, 1000000)]:
        total = sum_pair_distances(expand_space_between_galaxies(galaxies, space_rows, space_columns, expansion_factor))
        print(f"Part {i}: After expanding empty space by a factor of {expansion_factor}, the sum of distances between every pair of galaxies is {total}")
    return 0


def locate_galaxies_and_expanding_space(filename) -> tuple[list[tuple[int, int]], list[int], list[int]]:
    """Locate galaxies and expanding space in an input telescope image"""
    with open(filename, 'r') as file:
        galaxy_rows, galaxy_columns = set(), set()
        galaxies: list[Vector] = []
        for i, line in enumerate(file):
            for j, char in enumerate(line.strip()):
                if char == '#':
                    galaxies.append(Vector(i,j))
                    galaxy_rows.add(i)
                    galaxy_columns.add(j)

    space_rows = set(range(i+1)) - galaxy_rows
    space_columns = set(range(j+1)) - galaxy_columns
    return galaxies, space_rows, space_columns


def expand_space_between_galaxies(galaxies: list[tuple[int, int]], space_rows: list[int], space_columns: list[int], expansion_factor: int) -> list[tuple[int, int]]:
    """Returns a list of galaxies with new coordinates after expanding empty rows/columns between galaxies by the expansion factor"""
    extra_space = expansion_factor - 1
    shifted_galaxies = [
        galaxy + Vector(
            extra_space * sum(galaxy.i > space_row_i for space_row_i in space_rows),
            extra_space * sum(galaxy.j > space_column_j for space_column_j in space_columns)
        )
        for galaxy in galaxies
    ]
    return shifted_galaxies


def sum_pair_distances(my_list) -> int:
    """Return the sum of distances between all unordered pairs of items in a list"""
    return sum(abs(a - b) for idx, a in enumerate(my_list) for b in my_list[:idx])


@dataclass
class Vector:
    i: int
    j: int

    def __add__(self, other):
        return Vector(self.i + other.i, self.j + other.j)

    def __sub__(self, other):
        return Vector(self.i - other.i, self.j - other.j)

    def __abs__(self):
        return abs(self.i) + abs(self.j)


if __name__ == "__main__":
    main()
