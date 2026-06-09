#!/usr/bin/env python3
"""
--- Day 12: Leonardo's Monorail ---
https://adventofcode.com/2016/day/12
Emulate assembly code operations which incrementally
calculate integer sums, products, and Fibonacci numbers

References
- Structural Pattern Matching
  - https://peps.python.org/pep-0636/
"""
import os

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        instructions = file.read().splitlines()

    computer = Computer()
    computer.run_program(instructions)
    print(f"Part 1: The answer is {computer.registers}")

    computer = Computer(c=1)
    computer.run_program(instructions)
    print(f"Part 2: The answer is {computer.registers}")


class Computer:
    def __init__(self, **kwargs):
        """Initialise the four registers (a, b, c, and d) to start at 0
        with option to set initial values by keyword argument
        """
        self.registers: dict[str, int] = {char: 0 for char in "abcd"}
        for key, val in kwargs.items():
            if key in self.registers:
                self.registers[key] = val

    def run_program(self, instructions: list[str], pointer: int=0) -> None:
        """"""
        # Split each instruction into operands
        split_instructions = [instruction.split() for instruction in instructions]

        # Convert integer literals from string to integer data type before the execution loop
        for instruction in split_instructions:
            # Skip attempted conversion of the first word in an instruction
            # as this should be an operator name and not an integer literal
            for i, operand in enumerate(instruction[1:], 1):
                try:
                    instruction[i] = int(operand)
                except ValueError:
                    pass

        while 0 <= pointer < len(split_instructions):
            match split_instructions[pointer]:
                # `cpy x y` copies `x` (either an integer or the value of a register) into register `y`
                case ["cpy", x, y]: self.registers[y] = self._parse_operand(x)
                case ["inc", x]: self.registers[x] += 1 # `inc x` increases the value of register `x` by one.
                case ["dec", x]: self.registers[x] -= 1 # `dec x` decreases the value of register x by one.
                case ["jnz", x, y]: # jump-if-not-zero
                    # `jnz x y` jumps to an instruction `y` away (positive means forward; negative means backward),
                    # but only if `x` is not zero, otherwise increment pointer as usual.
                    if self._parse_operand(x) != 0:
                        # The `jnz` instruction moves relative to itself:
                        # an offset of -1 would continue at the previous instruction,
                        # while an offset of 2 would skip over the next instruction.
                        pointer += self._parse_operand(y)
                        continue
            pointer += 1

    def _parse_operand(self, val: str | int) -> int:
        """Lookup value of a register if the input is a reference/not an integer literal)"""
        return val if isinstance(val, int) else self.registers[val]


if __name__ == "__main__":
    main()
