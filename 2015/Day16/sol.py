#!/usr/bin/env python3
"""
--- Day 16: Aunt Sue ---
https://adventofcode.com/2015/day/16
Theme: Comparison operators

References:
- https://docs.python.org/3/library/operator.html
"""
import os
import operator


DIRPATH = os.path.dirname(__file__)


def main():
    reference: dict[str, int] = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        aunts: dict[str, dict[str, int]] = dict(map(parse_description, file))

    for aunt, props in aunts.items():
        if all(val == reference[key] for key, val in props.items()):
            print("Part 1: Reference match for", aunt, props)

    comparisons = {
        "cats": operator.gt, "trees": operator.gt,
        "pomeranians": operator.lt, "goldfish": operator.lt
    }

    for aunt, props in aunts.items():
        if all(comparisons.get(key, operator.eq)(val, reference[key]) for key, val in props.items()):
            print("Part 2: Reference match for", aunt, props)


def parse_description(line: str) -> tuple[str, dict[str, int]]:
    """Parse a formatted string representing a dictionary of integer values"""
    items: dict[str, int] = {}
    name, _, desc = line.strip().partition(": ")
    for prop in desc.split(", "):
        key, val_str = prop.split(": ")
        items[key] = int(val_str)
    return name, items


if __name__ == "__main__":
    main()
