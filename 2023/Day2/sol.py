#!/usr/bin/env python3
"""
--- Day 2: Cube Conundrum ---
https://adventofcode.com/2023/day/2
Part 1: String parsing and integer comparison
Part 2: Minimum of integers across categories
"""
import math


def main():
    part1_total, part2_total = 0, 0
    reference_bag = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    # Read and parse each line in the input file
    with open("input.txt", 'r') as file:
        for line in file:
            game_name, game_data = line.strip().split(": ")
            part1_total += int(game_name.removeprefix("Game ")) if is_game_possible(game_data, reference_bag) else 0
            part2_total += math.prod(minimum_possible_cube_set(game_data).values())
    print(f"Part 1: The sum of the IDs of possible games is {part1_total}")
    print(f"Part 2: The sum of the powers of the minimum possible set of cubes for each game is {part2_total}")


def is_game_possible(game_data: str, reference_bag: dict[str, int]) -> bool:
    for revealed_cube_set in game_data.split("; "):
        for cube_data in revealed_cube_set.split(", "):
            cube_count, cube_colour = cube_data.split(" ")
            # Impossible game check
            if int(cube_count) > reference_bag[cube_colour]:
                return False
    # All revealed cube sets possible with reference bag
    return True


def minimum_possible_cube_set(game_data: str) -> dict[str, int]:
    minimal_set = {
        "red": 0,
        "green": 0,
        "blue": 0
    }
    for revealed_cube_set in game_data.split("; "):
        for cube_data in revealed_cube_set.split(", "):
            cube_count, cube_colour = cube_data.split(" ")
            minimal_set[cube_colour] = max(int(cube_count), minimal_set[cube_colour])
    return minimal_set


if __name__ == "__main__":
    main()
