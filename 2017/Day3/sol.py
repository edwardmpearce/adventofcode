#!/usr/bin/env python3
"""
--- Day 3: Spiral Memory ---
https://adventofcode.com/2017/day/3
Part 1: Mathematics, Symmetry, Modular Arithmetic
Part 2: Sequence generation
"""
import os

from spiral import generate_spiral_adjacent_sum_sequence

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        num = int(file.read())

    print(f"Part 1: The answer is {solve_part_1(num)}")
    print(f"Part 2: The answer is {solve_part_2(num)}")


def solve_part_1(num: int) -> int:
    """The positive integers are arranged incrementally spiralling outwards from the origin.
    Calculate the Manhattan (L1) distance of a given number to the origin.

    Consider the bijection f: ZZ>0 -> ZZ^2, n |-> (x,y) described by this incremental spiralling,
    then this algorithm should return abs(x) + abs(y).

    Note the embedded spiralling half-line is arranged into a nested sequence of odd-length squares
    with the value (2k+1)^2 in the same corner direction extending outwards (i.e. 1, 9, 25, 49, ...).
    Consider the boundary of the square with odd side length 2k+1 which contains the input number n,
    then k = max(abs(x),abs(y)) is the perpendicular distance from the origin to side of the odd square containing n.
    We can exploit the (D4) rotational and reflectional symmetry to subsequently determine
    the remaining distance min(abs(x),abs(y)) = abs(k - ((num - (2k-1)^2) % (2k))) along the edge of the square.
    Finally, we can use modular arithmetic to simplify the formula to abs(k - ((num - 1) % 2k))
    """
    # Determine the smallest odd square containing the input
    k: int = 0
    while num > (2*k+1)**2:
        k += 1
    if k == 0:
        return 0
    return k + abs(k - ((num - 1) % (2*k)))


def solve_part_2(num: int) -> int:
    """Following the outward spiralling half-line embedding order, starting with Square 1 with the value 1,
    sequentially store the sum of previously assigned values in all adjacent squares, including diagonals.
    Once a square is written, its value does not change.
    Return the first (i.e. lowest) value written that is larger than the given input.
    """
    value_generator = generate_spiral_adjacent_sum_sequence()
    sequence_value: int = next(value_generator)
    while sequence_value <= num:
        sequence_value = next(value_generator)
    return sequence_value


if __name__ == "__main__":
    main()
