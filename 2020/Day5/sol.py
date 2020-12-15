#!/usr/bin/env python3
"""
--- Day 5: Binary Boarding ---
https://adventofcode.com/2020/day/5
Part 1: Convert binary space partitioning into a pair of decimal indices, then linearize into unique ID
        Effectively involves implementing an algorithm to traverse a binary search tree
Part 2: Find the missing number in an arithmetic sequence
"""


def main():
    # Read through input file and store as a list of pairs of strings
    with open("input.txt", 'r') as file:
        # Row number determined by first 7 characters, column by last 3 characters (ignore newline)
        boarding_passes = [(line[0:7], line[7:10]) for line in file]

    # Iterate through the list of boarding passes and convert to seat ID
    # Calculate the row and column number by converting partition strings to numerical indices
    # Combine the row and column indices into unique seat ID
    seat_ids = [8 * partition_to_index(row) + partition_to_index(col) for row, col in boarding_passes]

    # Determine the highest seat ID on a boarding pass in the input file
    max_seat_id = max(seat_ids)
    print(f"Part 1: The highest seat ID on a boarding pass was {max_seat_id}")

    # An arithmetic sequence of consecutive integers (common difference 1) from `min` to `max` inclusive
    # contains `min - max + 1` numbers, and has sum equal to `(max + min) * (max - min + 1) / 2`
    # As we know one boarding pass is missing, the length of our list will be one less, and
    # the missing seat ID is the difference between the expected sum and the actual sum
    assert min(seat_ids) == max_seat_id - len(seat_ids)
    expected_seat_id_sum = (2 * max_seat_id - len(seat_ids)) * (len(seat_ids) + 1) // 2
    missing_seat_id = expected_seat_id_sum - sum(seat_ids)
    print(f"Part 2: The seat ID of the missing boarding pass is {missing_seat_id}")
    # We could alternatively create a set of the expected seat IDs (ints from min to max inclusive)
    # and iterate through the boarding passes to find any missing values. This uses more space
    # and runtime to find one missing value, but is preferred when searching for multiple missing vals
    return 0


def partition_to_index(partition):
    """
    Convert a binary string of length n into an integer between 0 and 2^n - 1 inclusive.
    The binary string should contain only two types of characters: {F, B} or {L, R}, which
    act as instructions for a binary search through the list [0, ..., 2^n - 1].
    The characters F, L indicate that the output integer lies in the lower half of the range, whilst
    the chars B, R indicate that the output integer lies in the upper half.
    """
    # Initialise the search range containing the seat's row/column from 0 to 2^len(partition) - 1
    low, high = 0, (1 << len(partition)) - 1
    # Implement binary search-like algorithm with char check condition for moving left/right
    for c in partition:
        midpoint = low + (high - low) // 2
        if c in {'F', 'L'}:
            high = midpoint
        elif c in {'B', 'R'}:
            low = midpoint + 1
    # Check that we have narrowed down the search space to a single element (no unexpected characters)
    assert low == high
    # Return the search output
    return low


if __name__ == "__main__":
    main()
