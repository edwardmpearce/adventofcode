#!/usr/bin/env python3
"""
--- Day 6: Trash Compactor ---
https://adventofcode.com/2025/day/6
Transposing tabular data with zip
"""
import os
import math

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        puzzle_input: str = file.read()
        cols, _ = parse_puzzle_input_horizontally(puzzle_input)
        problems, ops = parse_puzzle_input_vertically(puzzle_input)

    part_1_answers = solve_math_problems(cols, ops)
    print(f"Part 1: The sum of all answers is {sum(part_1_answers)}")

    part_2_answers = solve_math_problems(problems, ops)
    print(f"Part 2: The sum of all answers is {sum(part_2_answers)}")


def parse_puzzle_input_horizontally(puzzle_input: str) -> tuple[list[list[int]], list[str]]:
    """Parse puzzle input string into two variables: a table of numbers (list of columns) and the reduction operator for each column."""
    data: list[list[str]] = [line.split() for line in puzzle_input.splitlines()]
    number_rows: list[list[int]] = [list(map(int, row)) for row in data[:-1]]
    # Each problem consists of a column of numbers
    problems: list[list[int]] = list(zip(*number_rows))
    ops: list[str] = data[-1]
    return problems, ops


def solve_math_problems(problems: list[list[int]], ops: list[str]) -> list[int]:
    """Return a list of answers to math problems by applying an aggregation/reduction operator to a collection of numbers.
    The list of problems (collections of numbers to be aggregated) is expected to be of equal length as the list of operators.
    """
    operator_mapping = {'+': sum, '*': math.prod}
    answers = [operator_mapping[op](col) for col, op in zip(problems, ops)]
    return answers


def parse_puzzle_input_vertically(puzzle_input: str) -> tuple[list[list[int]], list[str]]:
    """Parse puzzle input string into two variables: a list of lists of numbers (read vertically from top to bottom) and a reduction operator to apply to each set of numbers."""
    lines = puzzle_input.splitlines()
    ops: list[str] = lines[-1].split() # Split last line by whitespace
    # Each number is a vertical column of digits
    cols: list[str] = ["".join(col_tuple).strip() for col_tuple in zip(*lines[:-1])]
    # Here we use problem to refer to a collection of numbers to be aggregated
    problems: list[list[int]] = []
    problem: list[int] = []
    for col in cols:
        if col:
            problem.append(int(col))
        else:
            # Problems are separated by a full column of only spaces.
            problems.append(problem)
            problem: list[int] = []
            
    # Add last problem to list
    if problem:
        problems.append(problem)
    
    return problems, ops


if __name__ == "__main__":
    main()
