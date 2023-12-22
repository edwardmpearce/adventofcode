#!/usr/bin/env python3
"""
--- Day 9: Encoding Error ---
https://adventofcode.com/2020/day/9
Part 1: Variation on TwoSum problem.
        Find (first) integer in list which doesn't have a TwoSum pair of distinct integers among the
        25 numbers which precede it.
Part 2: Find a contiguous set of at least two numbers in a list which sum to a target number
"""


def main():
    # Read the list of line-separated integers into memory
    with open("input.txt", 'r') as file:
        data = list(map(int, file))

    # Find the first number in the list which cannot be expressed as the sum of two distinct
    # integers among the 25 numbers preceding it.
    # The pair of numbers in the preamble set must have distinct values (and hence distinct indices)
    invalid_num = first_invalid_num(data, 25)

    # Get start and end indices of a contiguous subsequence (of length at least 2) in the input list
    # whose sum is the previously calculated invalid number
    start, end = find_sum_subseq(data, invalid_num)
    subseq = data[start:end]
    assert sum(subseq) == invalid_num

    print(f"Part 1: The first invalid number in the list is {invalid_num}.")
    print(f"Part 2: The encryption weakness is {min(subseq) + max(subseq)}.")
    return 0


def first_invalid_num(nums, len_preamble):
    """
    Find the first number in the input list `nums` which cannot be expressed as the sum of
    two distinct integers among the `len_preamble` numbers preceding it. Starts checking validity
    from the number at index `len_preamble` in `nums` so that we have enough preceding numbers.
    Returns `None` if no such invalid number is found in the list, or if len(nums) <= len_preamble.
    """
    for i, target in enumerate(nums[len_preamble:]):
        # By maintaining `preamble` as a set, we remove duplicates, avoiding nondistinct sums to target
        preamble = set(nums[i:i+len_preamble])
        # Check whether we can express `target` as the sum of a distinct pair from the preamble set
        if not two_sum(preamble, target):
            # Target value not valid in the sequence
            return target
    # Otherwise, no invalid numbers in the `nums` sequence
    return None


def find_sum_subseq(nums, target):
    """
    Let `nums` be a list of positive integers and let `target` be a positive integer
    Find a contiguous subsequence (of length at least 2) in `nums` whose sum is `target`
    and return the subsequence indices for slicing if exists, else return False

    We slide a variable sized window across the `nums` array and track the cumulative sum of array vals
    ensuring the window always has length at least 2. As `nums` contains only positive integers,
    adding an element to the end of the window always increases the array sum, whilst removing an
    element from the start of the window always decreases the array sum.
    """
    low, high = 0, 2
    cum_sum = nums[0] + nums[1]
    while high < len(nums):
        # Check if the current subsequence (of length at least 2) sums to `target`
        if cum_sum == target:
            return low, high
        # If the cumulative sum is too low or our subsequence has length 2, add another element
        elif cum_sum < target or high - low == 2:
            cum_sum += nums[high]
            high += 1
        # Otherwise the cumulative sum exceeds the target and we can remove an element
        else:
            cum_sum -= nums[low]
            low += 1
    # Check if we found a suitable subsequence on the last iteration
    return (low, high) if cum_sum == target else False


def two_sum(nums, target):
    diffs = set()
    for x in nums:
        if x in diffs:
            return x, target - x
        else:
            diffs.add(target - x)
    # No pair found whose sum equals to target
    return False


if __name__ == "__main__":
    main()
