#!/usr/bin/env python3
"""
--- Day 6: Memory Reallocation ---
https://adventofcode.com/2017/day/6
Theme: Division with remainder
"""
import os

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        memory_banks = tuple(map(int, file.read().split()))

    print(f"Part 1: The answer is {solve_part_1(memory_banks)}")
    print(f"Part 2: The answer is {solve_part_2(memory_banks)}")


def redistribute(memory_banks: tuple[int]) -> tuple[int]:
    """Return memory bank block counts after redistributing blocks.

    1. Find the memory bank with the most blocks (ties won by the lowest-numbered memory bank).
    2. Remove all blocks from the selected bank, then sequentially re-insert blocks one by one
    into subsequent memory banks (by index, cyclically); Continuing until running out of blocks.
    """
    num_banks: int = len(memory_banks)
    max_val = max(memory_banks)
    max_idx = memory_banks.index(max_val)
    q, r = divmod(max_val, num_banks)
    return tuple(
        (
            (0 if i == max_idx else memory_banks[i]) +
            q + (1 if 1 <= ((i - max_idx) % num_banks) <= r else 0)
        )
        for i in range(num_banks)
    )


def reallocation_routine(initial_config: tuple[int]) -> tuple[dict, tuple[int]]:
    """Run the memory bank block redistribution routine from an initial configuration of block counts
    until a configuration is produced that has been seen before, then return a dictionary from
    memory bank configuration to cycle number along with the first repeated block configuration
    """
    seen_configs: set[tuple[int]] = {initial_config: 0}
    block_config, num_cycles = redistribute(initial_config), 1
    while block_config not in seen_configs:
        seen_configs |= {block_config: num_cycles}
        block_config = redistribute(block_config)
        num_cycles += 1
    return seen_configs, block_config


def solve_part_1(initial_config: tuple[int]) -> int:
    """Given a tuple of initial block counts, return the number of redistribution cycles before
    a configuration is produced that has been seen before
    """
    seen_configs, _ = reallocation_routine(initial_config)
    return len(seen_configs)


def solve_part_2(initial_config: tuple[int]) -> int:
    """Given a tuple of initial block counts, return the size of the repeating loop. That is,
    starting from a state that has already been seen, return the number of redistribution cycles
    before that same state is seen again
    """
    seen_configs, first_repeated_config = reallocation_routine(initial_config)
    return len(seen_configs) - seen_configs[first_repeated_config]


if __name__ == "__main__":
    main()
