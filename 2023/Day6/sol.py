#!/usr/bin/env python3
"""
--- Day 6: Wait For It ---
https://adventofcode.com/2023/day/6
Part 1: Set of integer inputs to quadratic function with positive output
Part 2: Repeat for large input. Lesson on complexity/performance.

References
- https://en.wikipedia.org/wiki/Computational_complexity_of_mathematical_operations
- https://en.wikipedia.org/wiki/Methods_of_computing_square_roots
- https://mathoverflow.net/questions/99421/computational-complexity-of-calculating-the-nth-root-of-a-real-number
"""
import math


def main():
    with open("input.txt", 'r') as file:
        time_data: str = file.readline().removeprefix("Time:")
        distance_data: str = file.readline().removeprefix("Distance:")
    ways_to_win_part1 = [
        calculate_ways_to_win(race_time, distance_record)
        for race_time, distance_record in zip(map(int, time_data.split()), map(int, distance_data.split()))
    ]
    print(f"Part 1: The number of ways you can beat the records across all races is {math.prod(ways_to_win_part1)}.")

    ways_to_win_part2 = calculate_ways_to_win(
        int(time_data.replace(" ", "")),
        int(distance_data.replace(" ", "")),
        allow_sqrt=True
    )
    print(f"Part 2: The number of ways you can beat the longer race is {ways_to_win_part2}.")

    return 0


def calculate_ways_to_win(race_time: int, distance_record: int, allow_sqrt=False) -> int:
    if allow_sqrt:
        # Find shortest_winning_press_time using the quadratic formula. 
        # This approach is O(log(race_time)) complexity from calculating the square root. See references for more details.
        shortest_winning_press_time = int((race_time - math.sqrt(race_time * race_time - 4 * distance_record)) / 2 + 1)
    else:
        # Find the shortest winning press-time using a for loop. This approach has O(race_time) time complexity.
        for press_time in range(1, race_time):
            if press_time * (race_time - press_time) - distance_record > 0:
                shortest_winning_press_time = press_time
                break
    return race_time - 2 * shortest_winning_press_time + 1


if __name__ == "__main__":
    main()
