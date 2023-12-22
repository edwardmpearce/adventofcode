#!/usr/bin/env python3
"""
--- Day 1: Report Repair ---
https://adventofcode.com/2020/day/1
Part 1: Variation of TwoSum problem.
Find two distinct integers in a list which add to the target number, then print their product
Part 2: Variation of ThreeSum problem.
Find three distinct integers in a list which add to the target number, then print their product
"""


def main():
    # Load input file as a list of ints
    with open("input.txt", 'r') as file:
        nums = list(map(int, file))

    # Find the two entries in the input file that sum to 2020
    x, y = two_sum(nums, 2020)
    # Print the two entries and their product
    print(f"Part 1: x = {x}, y = {y}, xy = {x * y}")

    # Find the three entries in the input file that sum to 2020
    x, y, z = three_sum(nums, 2020)
    # Print the three entries and their product
    print(f"Part 2: x = {x}, y = {y}, z = {z}, xyz = {x * y * z}")


def two_sum(nums, target):
    diffs = set()
    for x in nums:
        if x in diffs:
            return x, target - x
        else:
            diffs.add(target - x)
    # No pair found whose sum equals to target
    return False


def three_sum(nums, target):
    # First sort the list in O(n log(n)) time
    for i, x in enumerate(sorted(nums)):
        # For each entry x in the sorted list, search forward through the list
        # for a pair completing a triple containing x which sums to the target
        # This takes n(n+1)/2 steps for an overall runtime of O(n^2)
        result = two_sum(nums[i:], target - x)
        if result:
            return x, result[0], result[1]
    # No triple found whose sum equals to target
    return False


if __name__ == "__main__":
    main()
