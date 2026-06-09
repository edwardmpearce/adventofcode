#!/usr/bin/env python3
"""
--- Day 12: Leonardo's Monorail ---
https://adventofcode.com/2016/day/12
More performant implementations of the puzzle input assembunny instructions through
interpretation and assumptions on programme structure and intention
to calculate integer sums, products, and Fibonacci numbers

References
- https://en.wikipedia.org/wiki/Fibonacci_sequence
"""
import os
from dataclasses import dataclass
from typing import Self

DIRPATH = os.path.dirname(__file__)


@dataclass
class ControlParameters:
    c_key: int
    d_key: int

    @classmethod
    def extract_from_instructions(cls, instructions: str) -> Self:
        operands: list[list[str]] = [line.split() for line in instructions.splitlines()]
        # Extract values assigned to c, d registers on lines 17, 18, respectively
        c_key, d_key = int(operands[16][1]), int(operands[17][1])
        return cls(c_key=c_key, d_key=d_key)


class ControlProgram:
    def __init__(self, instructions: str):
        self.control_params = ControlParameters.extract_from_instructions(instructions)

    def implementation_1(self, c0: int=0) -> dict[str, int]:
        """Interpretation
        - jumps backward whilst decrementing a variable and iterative loop
        - Iterative/repeated incrementation as addition
        - Iterative/repeated addition as multiplication
        """
        a, b, c, d = 1, 1, c0, 26 # Lines 1-3
        # Lines 4-9: Set d = 26 + 7 = 33 if the initial value of c is nonzero
        if c != 0: # Lines 4-5
            c = 7 # Line 6
            d, c = d+c, 0 # Lines 7-9
        # Lines 10-16: Calculate Fibonacci numbers by iterating over d and using c as a temporary variable
        for _ in range(d):
            c = a
            a, b = a+b, 0
            b = c
        d = 0
        # Lines 17, 18
        c, d = self.control_params.c_key, self.control_params.d_key
        # Lines 19-23
        a, c, d = a + c*d, 0, 0
        return {"a": a, "b": b, "c": c, "d": d}


    def implementation_2(self, c0: int=0) -> dict[str, int]:
        """Combine lines used for (conditional) variable assignment which are subsequently overwritten"""
        a, b, c, d = 1, 1, 0, 26 if c0 == 0 else 33 # Lines 1-9
        # Lines 10-16: Calculate Fibonacci numbers by iterating over d
        for _ in range(d):
            a, b = a+b, a
        c, d = b, 0
        # Lines 17, 18
        c, d = self.control_params.c_key, self.control_params.d_key
        # Lines 19-23
        a, c, d = a + c*d, 0, 0
        return {"a": a, "b": b, "c": c, "d": d}


    def implementation_3(self, c0: int=0) -> dict[str, int]:
        """Use hardcoded values for required Fibonnacci numbers"""
        registers: dict[str, int] = {
            "a": 317_811, "b": 196_418 # F_28, F_27
        } if c0 == 0 else {
            "a": 9_227_465, "b": 5_702_887 # F_35, F_34
        }
        registers.update({"c": 0, "d": 0})
        registers["a"] += self.control_params.c_key * self.control_params.d_key
        return registers


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        instructions = file.read()

    control_program = ControlProgram(instructions)

    results: list[dict[int, dict[str, int]]] = []
    for i in range(1, 4):
        results.append({
            1: getattr(control_program, f'implementation_{i}')(c0=0),
            2: getattr(control_program, f'implementation_{i}')(c0=1)
        })
    assert all(output == results[0] for output in results)
    for part_idx, output in results[-1].items():
        print(f"Part {part_idx}: {output}")


if __name__ == "__main__":
    main()
