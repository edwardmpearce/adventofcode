#!/usr/bin/env python3
"""
--- Day 17: No Such Thing as Too Much ---
https://adventofcode.com/2015/day/17
Part 1: Count the number of different combinations of summands which sum to the target total
Part 2: Count the number of different combinations of summands which sum to the target total using the minimum number of summands

Themes: Combinatorics, Recursion, Variation of Combination Sum

References
- https://docs.python.org/3/library/functools.html#functools.partial
"""
import os
from collections.abc import Iterator


DIRPATH = os.path.dirname(__file__)


def main():
    target_total: int = 150

    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        jugs: list[int] = sorted(map(int, file), reverse=True)

    num_combinations = count_combinations(jugs, target_total)
    assert len(list(generate_combinations(jugs, target_total))) == num_combinations
    print(f"Part 1: There are {num_combinations} possible combinations which sum to {target_total}.")

    min_containers_required = min(map(len, generate_combinations(jugs, target_total)))
    fewest_summand_solutions = [combo for combo in generate_combinations(jugs, target_total) if len(combo) == min_containers_required]
    print(f"Part 2: There are {len(fewest_summand_solutions)} combinations which sum to {target_total} using the minimum possible {min_containers_required} containers.")
    print(fewest_summand_solutions)


def count_combinations(summands: list[int], target_total: int) -> int:
    """Count the number of different combinations of summands which sum to the target total.
    Assumes target total and summands are nonnegative integers.
    """
    if target_total < 0 or (target_total > 0 and not summands):
        return 0
    elif target_total == 0:
        return 1
    else:
        first, *rest = summands
        return count_combinations(rest, target_total - first) + count_combinations(rest, target_total)


def generate_combinations(summands: list[int], target_total: int) -> Iterator[tuple[int]]:
    """Yield all combinations of a collection of summands which sum to the target total.
    Assumes target total and summands are nonnegative integers.
    """
    def generate_combinations_recursively(candidates: list[int], target: int, current_combo: tuple[int]) -> Iterator[tuple[int]]:
        """Yield all tuples consisting of combinations of the candidates which sum to the target, prepended by the `current_combo` tuple.
        Assumes target and candidates are nonnegative integers.

        The main recursive logic is defined in this inner function to decouple implementation details from the desired usage pattern,
        allowing the outer function to have a clean and intuitive function signature (i.e. without exposing the `currnet_combo` argument).
        """
        if target < 0 or (target > 0 and not candidates):
            return
        elif target == 0:
            yield current_combo
        else:
            x, *rest = candidates
            for combo_with_x in generate_combinations_recursively(rest, target - x, current_combo + (x,)):
                yield combo_with_x
            for combo_without_x in generate_combinations_recursively(rest, target, current_combo):
                yield combo_without_x

    for combo in generate_combinations_recursively(summands, target_total, tuple()):
        yield combo


if __name__ == "__main__":
    main()
