#!/usr/bin/env python3
"""
--- Day 10: Adapter Array ---
https://adventofcode.com/2020/day/10
Part 1: Sort a list of integers and count occurences of differences between consecutive elements
Part 2: Count all possible paths from source to sink in directed acyclic graph with 98 nodes
"""

# Standard library imports
from collections import Counter


def main():
    # Read the list of line-separated integers into memory
    with open("input.txt", 'r') as file:
        data = list(map(int, file))

    # Part 1
    # Sort the adapters so that we can connect each one in turn
    # Include an effective joltage rating of 0 for the charging outlet
    # Add the device's built-in joltage adapter rated for 3 jolts higher
    # than the highest-rated adapter in your bag (`data`)
    device_rating = max(data) + 3
    ordered_adapters = [0] + sorted(data) + [device_rating]
    jolt_diffs = count_consecutive_differences(ordered_adapters)

    # Part 2
    # Could create directed acyclic graph structure with adapters as nodes each with up to 3 children
    # Then count all paths from source at 0 (charging outlet) to sink at device joltage adapter.
    # Rather than count paths recursively in this way, we work backwards with recurrence relation
    ratings_set = set(ordered_adapters)

    # The value at index i will contain the number of arrangements of adapters from rating i to device
    # Once populated, the value of interest is `count_arrangements_from[0]`
    count_arrangements_from = [0 for i in range(device_rating + 1)]

    # Count trivial arrangement/path from the device to itself
    count_arrangements_from[device_rating] = 1

    # Implement recurrence relation: a_{i} = a_{i+1} + a_{i+2} + a_{i+3} if i in ratings_set else 0
    # with initial condition a_{device_rating} = 1, a_{i} = 0 for i > device_rating
    for i in reversed(range(device_rating)):
        # No paths to device unless we have an adapter with rating `i`
        if i in ratings_set:
            # We make an path from `i` to the end by prepending it to
            # any path from one of its children adapters to the end
            count_arrangements_from[i] = sum(count_arrangements_from[i+1:i+4])

    print(f"Part 1: When using every adapter the jolt difference counts are {jolt_diffs}.")
    print("Part 2: Total distinct adapter arrangements from charging outlet to device is {}.".format(
        count_arrangements_from[0])
        )
    return 0


def count_consecutive_differences(nums):
    return Counter(x1 - x0 for x0, x1 in zip(nums, nums[1:]))


if __name__ == "__main__":
    main()
