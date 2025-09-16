#!/usr/bin/env python3
"""
--- Day 7: Some Assembly Required ---
https://adventofcode.com/2015/day/7
Themes: Bitwise operations, dependency tree when expanding nested logical/binary expressions

Commentary
This puzzle provides a great opportunity to show the power of
1. Recursion, and caching intermediate results
2. Structural pattern matching with Python's match-case syntax

If recursion must be avoided (e.g. to avoid hitting stack depth limits),
another way to incrementally populate a cache (dictionary) of known signals (wire values)
would be using a while loop to repeated iterate over the list of circuit instructions
and resolving/removing instructions which can be evaluated directly from literals and currently cached values.

References
- http://inspiredpython.com/course/pattern-matching/mastering-structural-pattern-matching
- https://docs.python.org/3/tutorial/controlflow.html#match-statements
- [PEP 636 – Structural Pattern Matching: Tutorial](https://peps.python.org/pep-0636/)
- [Raymond Hettinger's video on structural pattern matching](https://www.youtube.com/watch?v=ZTvwxXL37XI)
"""
import os

DIRPATH = os.path.dirname(__file__)

NUM_BITS = 16
ONES = (1 << NUM_BITS) - 1


def main():
    # Load input file
    instructions: dict[str, str] = {}
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        for line in file:
            source, _, target = line.strip().partition(" -> ")
            instructions[target] = source

    part_1_answer = calculate_signal('a', {}, instructions)
    part_2_answer = calculate_signal('a', {'b': part_1_answer}, instructions)

    print(f"Part 1: The signal provided to wire 'a' is {part_1_answer}")
    print(f"Part 2: After overriding wire 'b' to signal {part_1_answer} and resetting the wires, "
          f"the signal provided to wire 'a' is {part_2_answer}")


def calculate_signal(target: str, signals: dict[str, int], instructions: dict[str, str]) -> int:
    """Return the 16-bit signal provided to the target wire.
    First check in cache of known signals, and otherwise resolve the signal from source instructions recursively.
    Update the cache of known signals as they are discovered.
    """
    if target.isdigit():
        return int(target)

    # First check if the signal is already known
    if target in signals:
        return signals[target]

    match source := instructions[target].split(" "):
        case [x]:
            signals[target] = calculate_signal(x, signals, instructions)
        case ["NOT", x]:
            # Bitwise complement (a.k.a. one's complement) as uint
            # https://en.wikipedia.org/wiki/Ones%27_complement
            signals[target] = calculate_signal(x, signals, instructions) ^ ONES
        case [x, op, y]:
            x_signal: int = calculate_signal(x, signals, instructions)
            y_signal: int = calculate_signal(y, signals, instructions)
            match op:
                case "AND":
                    signals[target] = x_signal & y_signal
                case "OR":
                    signals[target] = x_signal | y_signal
                case "LSHIFT":
                    # Trim the result of the left shift to the expected number of bits
                    signals[target] = (x_signal << y_signal) & ONES
                case "RSHIFT":
                    signals[target] = x_signal >> y_signal
                case _:
                    raise ValueError(f"Could not parse operator {op} in instruction {source} -> {target}")
        case _:
            raise ValueError(f"Could not parse instruction {source} -> {target}")
    return signals[target]


if __name__ == "__main__":
    main()
