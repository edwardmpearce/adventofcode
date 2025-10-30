#!/usr/bin/env python3
"""
--- Day 15: Science for Hungry People ---
https://adventofcode.com/2015/day/15
Themes: Combinatorics (Weak compositions), linear optimization problems

References
- https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types
- https://docs.python.org/3/library/itertools.html#itertools.combinations
- https://en.wikipedia.org/wiki/Composition_(combinatorics)
- https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)

"""
import os
from dataclasses import dataclass, asdict
import math
from collections.abc import Iterator
from itertools import combinations


DIRPATH = os.path.dirname(__file__)


@dataclass
class CookieProperties:
    """5D cookie vector supporting addition and scalar multiplication on both sides"""
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    def __add__(self, other):
        """Vector addition"""
        return CookieProperties(
            self.capacity + other.capacity,
            self.durability + other.durability,
            self.flavor + other.flavor,
            self.texture + other.texture,
            self.calories + other.calories
        )

    def __mul__(self, scalar: int):
        """Scalar multiplication"""
        return CookieProperties(**{prop: val * scalar for prop, val in asdict(self).items()})

    def __rmul__(self, scalar: int):
        """Swap order of operands to re-use implementation of __mul__"""
        return self * scalar

    def score(self) -> int:
        """Calculate the score of a cookie with the following properties, bounded below by zero"""
        return math.prod(max(val, 0) for prop, val in asdict(self).items() if prop != "calories")


def read_input_data() -> dict[str, CookieProperties]:
    """Read an input file of cookie ingredient properties per teaspoon"""
    ingredients: dict[str, CookieProperties] = {}
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        for line in file:
            ingredient_name, _, rest = line.strip().partition(": ")
            properties: dict[str, int] = {}
            for prop_desc in rest.split(", "):
                prop_name, val_str = prop_desc.split()
                properties[prop_name] = int(val_str)
            ingredients[ingredient_name] = CookieProperties(**properties)

    return ingredients


def recipes(total_teaspoons: int) -> Iterator[dict[str, int]]:
    """Generate all possible ways to allocate n teaspoons across 4 different ingredients
    Yields the same set as weak_compositions(total_teaspoons, 4).
    """
    for i in range(total_teaspoons + 1):
        for j in range(total_teaspoons + 1 - i):
            for k in range(total_teaspoons + 1 - i - j):
                yield (i, j, k, total_teaspoons - (i + j + k))


def weak_compositions(n: int, m: int) -> Iterator[tuple[int]]:
    """Yield all m-tuples of non-negative integers which sum to n.
    A weak composition of an integer n is a way of writing n as the sum of a sequence of non-negative integers.
    Equivalently, yield all weak compositions of n of length m.
    Uses the 'stars and bars' method to give a 1:1 mapping from length-m weak compositions of n
    to combinations selecting positions of m-1 bars among n+m-1 star and bar symbols
    """
    for bar_positions in combinations(range(n + m - 1), m - 1):
        bars = (-1,) + bar_positions + (n + m - 1,) # Tuple concatenation
        yield tuple(bars[i+1] - bars[i] - 1 for i in range(m))


def make_cookie(ingredients: dict[str, CookieProperties], recipe: tuple[int]) -> CookieProperties:
    """Make cookie from a collection of ingredients and a recipe indicating the amounts"""
    return sum(
        (ingredient * amount for ingredient, amount in zip(ingredients.values(), recipe, strict=True)),
        start=CookieProperties(0,0,0,0,0)
    )


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    ingredients: dict[str, CookieProperties] = read_input_data()
    num_ingredients: int = len(ingredients)
    total_teaspoons: int = 100
    calorie_requirement: int = 500

    best_cookie_score = max(make_cookie(ingredients, recipe).score() for recipe in weak_compositions(total_teaspoons, num_ingredients))
    best_meal_replacement_cookie_score = max(
        cookie.score()
        for recipe in weak_compositions(total_teaspoons, num_ingredients)
        if (cookie := make_cookie(ingredients, recipe)).calories == calorie_requirement
    )

    print(f"Part 1: The best cookie has total score {best_cookie_score}")
    print(f"Part 2: The best 500-calorie meal replacement cookie has total score {best_meal_replacement_cookie_score}")


if __name__ == "__main__":
    main()
