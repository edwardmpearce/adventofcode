#!/usr/bin/env python3
"""
--- Day 3: Toboggan Trajectory ---
https://adventofcode.com/2020/day/3
Part 1: Draw a line of rational slope on a cylindrical grid and count the number of marked points 
        that the line passes through (for a given grid map containing marked points and line slope)
Part 2: Repeat for a selection of slopes and compute the product of number of trees encountered

Also implemented: Find the line of rational slope which minimizes intersection with the marked point set
"""


def main():
    # Load input file into local variable (list of strings)
    with open("input.txt", 'r') as file:
        # Don't forget to remove the newline character
        grid_map = [line.strip() for line in file]

    # Print the number of trees (represented by `#`) that would be encountered by 
    # starting at the top-left corner of the map and following a slope of right 3 and down 1.
    print(f"Part 1: {collisions(grid_map, 1, 3)} trees encountered for rise:run = 1:3.")

    test_cases = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    product = 1
    for rise, run in test_cases:
        product *= collisions(grid_map, rise, run)
    print(f"Part 2: Product of trees encountered over test cases is {product}.")

    # # Calculate the period at which the map repeats horizontally (like wrapping around a cylinder)
    # period = len(grid_map[0])
    # # Calculate the slope angle which minimises the number of trees encountered when sledding downhill
    # optimal_slope = min(range(period), key=lambda run : collisions(grid_map, 1, run))
    # min_collisions = collisions(grid_map, 1, optimal_slope)
    # print(f"Optimal slope is rise:run = 1:{optimal_slope}, with {min_collisions} trees encountered.")
    return 0


def collisions(grid_map, rise, run):
    """
    Count the number of trees (represented by `#`) encountered by moving along the path 
    (i * rise, i * run) through the grid starting from i = 0 (at (0,0)) to i = height - 1.
    """
    period = len(grid_map[0])
    return sum(row[i * run % period] == '#' for i, row in enumerate(grid_map[::rise]))


if __name__ == "__main__":
    main()
