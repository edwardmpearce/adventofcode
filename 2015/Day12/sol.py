#!/usr/bin/env python3
"""
--- Day 12: JSAbacusFramework.io ---
https://adventofcode.com/2015/day/12
Themes: JSON, recursion

References
- http://inspiredpython.com/course/pattern-matching/mastering-structural-pattern-matching
- https://docs.python.org/3/tutorial/controlflow.html#match-statements
- [PEP 636 – Structural Pattern Matching: Tutorial](https://peps.python.org/pep-0636/)
- [Raymond Hettinger's video on structural pattern matching](https://www.youtube.com/watch?v=ZTvwxXL37XI)
"""
import os
import json

DIRPATH = os.path.dirname(__file__)


def main():
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        account = json.load(file)

    print(f"Part 1: The sum of all numbers in the document is {sum(find_all_numbers(account, [], exclude_red=False))}")
    print(f"Part 2: Excluding objects with any property with value 'red', the sum of all numbers in the document is {sum(find_all_numbers(account, [], exclude_red=True))}")


def find_all_numbers(data: int | list | dict, num_cache: list[int], *, exclude_red: bool) -> list[int]:
    """Search recursively through a JSON document for int values and add them to a list
    Optional to ignore any object (and all of its children) which has any property with the value "red". Do this only for objects ({...}), not arrays ([...]).
    """
    match data:
        case int():
            num_cache.append(data)
        case list():
            temp_cache: list[int] = []
            for element in data:
                find_all_numbers(element, temp_cache, exclude_red=exclude_red)
            num_cache.extend(temp_cache)
        case dict():
            temp_cache: list[int] = []
            for value in data.values():
                if exclude_red and value == "red":
                    # Break early without adding numbers from the intermediate/temporary store to the list of found numbers
                    return num_cache
                else:
                    find_all_numbers(value, temp_cache, exclude_red=exclude_red)
            num_cache.extend(temp_cache)
    return num_cache


if __name__ == "__main__":
    main()
