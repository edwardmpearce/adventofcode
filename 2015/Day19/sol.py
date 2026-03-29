#!/usr/bin/env python3
"""
--- Day 19: Medicine for Rudolph ---
https://adventofcode.com/2015/day/19
Part 1: Substring substitution
Part 2: Successive substring substitution and Search

References
- Regular expressions for pattern matching and substiution
  - https://docs.python.org/3/library/re.html
  - https://docs.python.org/3/howto/regex.html#regex-howto
"""
import os
from collections import defaultdict
import re

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        substitutions, medicine_molecule = parse_puzzle_input(file.read())

    print(f"Part 1: The answer is {solve_part_1(substitutions, medicine_molecule)}")
    print(f"Part 2: The answer is {solve_part_2(substitutions, medicine_molecule)}")


def parse_puzzle_input(puzzle_input: str) -> tuple[dict[str, list[str]], str]:
    """Parse puzzle input string into a mapping of atom to list of possible substitutions and a starting molecule string"""
    replacements_input, _, molecule_input = puzzle_input.partition("\n\n")
    atom_replacements: dict[str, list[str]] = defaultdict(list)
    for line in replacements_input.splitlines():
        atom, replacement = line.split(" => ")
        atom_replacements[atom].append(replacement)
    return atom_replacements, molecule_input.strip()


def solve_part_1(atom_replacements: dict[str, list[str]], start_molecule: str) -> int:
    """Given a list of substitutions, calculate how many distinct molecule strings that can be obtained by any possible single replacement on the starting molecule string"""
    return len(distinct_substitution_outcomes(atom_replacements, start_molecule))


def solve_part_2(atom_replacements: dict[str, list[str]], target_molecule: str) -> int:
    """Find the fewest number of replacement steps to obtain the target molecule starting from a single electron 'e'"""
    # Successively calculates sets of all possible molecules that can be reached after n replacements until the target molecule is found and `n` is returned
    # This implementation does not have the required performance (ops, memory) to complete within reasonable time on the main puzzle input
    # It may be possible to find algorithmic efficiencies by considering 'reachability' from one prefix to another to help filter out dead ends in searching
    replacement_stages: list[set[str]] = [{'e'}]
    while target_molecule not in replacement_stages[-1]:
        replacement_stages.append({
            new_molecule
            for molecule in replacement_stages[-1]
            for new_molecule in distinct_substitution_outcomes(atom_replacements, molecule)
        })
        print(replacement_stages[-1])
    return len(replacement_stages) - 1


def distinct_substitution_outcomes(atom_replacements: dict[str, list[str]], molecule: str) -> set[str]:
    """Given a list of substitutions, return the set of distinct molecule strings that can be obtained by any possible single replacement on the starting molecule string"""
    return {
        molecule[:m.start()] + replacement + molecule[m.end():]
        for atom, replacements in atom_replacements.items()
        for m in re.finditer(atom, molecule)
        for replacement in replacements
    }


def split_molecule_by_atom(molecule: str, atom: str, replacement: str):
    """Return the set of distinct molecules (strings) that can be obtained by replacing any one occurence of an atom (substring) in the input molecule"""
    return {molecule[:m.start()] + replacement + molecule[m.end():] for m in re.finditer(atom, molecule)}


if __name__ == "__main__":
    main()
