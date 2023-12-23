#!/usr/bin/env python3
"""
--- Day 3: Gear Ratios ---
https://adventofcode.com/2023/day/3
Part 1: Boundary box pixel parsing
Part 2: List entities adjacent to a point
"""
from collections import defaultdict


def main():
    # Scan through the schematic file to locate the numbers and symbols
    schematic_numbers, symbols = parse_input_for_numbers_and_symbols("input.txt")

    # Any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. 
    # Periods (.) do not count as a symbol
    part1_total = sum(
        schematic_number["value"]
        for row_idx, row in schematic_numbers.items() for schematic_number in row
        if count_adjacent_symbols(row_idx, schematic_number["col_start"], schematic_number["col_end"], symbols) > 0
    )
    print(f"Part 1: The sum of all of the part numbers in the engine schematic is {part1_total}.")

    # A gear is any * symbol that is adjacent to exactly two part numbers.
    # Its gear ratio is the result of multiplying those two numbers together.
    part2_total = 0
    for (row, col), symbol in symbols.items():
        if symbol == '*':
            adjacent_part_numbers = find_adjacent_part_numbers(row, col, schematic_numbers)
            if len(adjacent_part_numbers) == 2:
                part2_total += adjacent_part_numbers[0] * adjacent_part_numbers[1]

    print(f"Part 2: The sum of all of the gear ratios in the engine schematic is {part2_total}.")

    return 0


def parse_input_for_numbers_and_symbols(filename):
    """Scan through a schematic file to locate numbers and symbols
    schematic_numbers is a dictionary from row indices to lists of schematic numbers (position and value data)
    symbols is a dictionary from (row, col) positions to symbol characters
    """
    with open(filename, 'r') as file:
        schematic_numbers : dict[int, list[dict[str, int]]] = defaultdict(list)
        symbols : dict[tuple[int, int], str] = {}

        for row_idx, row in enumerate(file):
            digit_buffer = []
            for col_idx, char in enumerate(row):
                if char.isdigit():
                    digit_buffer.append(char)
                elif char not in {'.', '\n'}:
                    # Found a symbol (non-digit, non-period character)
                    symbols[(row_idx, col_idx)] = char

                if digit_buffer and not char.isdigit():
                    # End of a schematic number (symbol or period)
                    # Here value = int(schematic[row_idx][col_start:col_end])
                    schematic_numbers[row_idx].append({
                        "value": int("".join(digit_buffer)),
                        "row": row_idx,
                        "col_start": col_idx - len(digit_buffer),
                        "col_end": col_idx
                    })
                    # Clear the digit buffer ready for a new schematic number
                    digit_buffer = []

    return schematic_numbers, symbols


def count_adjacent_symbols(i: int, j_start: int, j_end: int, symbols):
    """Scan boundary box around cells [i][j_start:j_end] for symbols"""
    num_adjacent_symbols = 0
    # Check for symbols to the immediate left and right of the location
    num_adjacent_symbols += (i, j_start - 1) in symbols
    num_adjacent_symbols += (i, j_end) in symbols
    # Scan rows above and below
    for j in range(j_start - 1, j_end + 1):
        num_adjacent_symbols += (i - 1, j) in symbols
        num_adjacent_symbols += (i + 1, j) in symbols
    return num_adjacent_symbols


def find_adjacent_part_numbers(i: int, j: int, schematic_numbers):
    """Return a list of all schematic numbers adjacent to position (i,j)"""
    adjacent_part_numbers = []
    # Check for part numbers to the immediate left and right of the symbol
    for schematic_number in schematic_numbers[i]:
        if schematic_number["col_start"] > j + 1:
            # Skip rest of numbers in the row as too far to the right (since numbers are listed left to right)
            break
        elif schematic_number["col_end"] == j or schematic_number["col_start"] == j + 1:
            # Part number is adjacent to symbol on the same row
            adjacent_part_numbers.append(schematic_number["value"])
    # Scan rows above and below
    for row in (schematic_numbers[i - 1], schematic_numbers[i + 1]):
        for schematic_number in row:
            if schematic_number["col_start"] > j + 1:
                # Skip rest of numbers in the row as too far to the right (since numbers are listed left to right)
                break
            if schematic_number["col_end"] >= j:
                # Part number col_start <= j+1 and last_char_col >= j-1, so there is overlap with the boundary around the symbol
                adjacent_part_numbers.append(schematic_number["value"])
    return adjacent_part_numbers


if __name__ == "__main__":
    main()
