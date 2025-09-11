#!/usr/bin/env python3
"""
--- Day 9: Mirage Maintenance ---
https://adventofcode.com/2023/day/9
Part 1: Fit a degree-n polynomial through the n+1 points [P(0), P(1), P(2), ..., P(n)] and calculate P(n+1)
Part 2: Calculate P(-1)
"""
from dataclasses import dataclass
import math


def main():
    part1_total, part2_total = 0, 0
    with open("input.txt", 'r') as file:
        for line in file:
            points = list(map(int, line.split()))
            P = Polynomial.fit(points)
            # Extrapolate the values one before and one after the list of points and add it to the total
            part1_total += P(len(points))
            part2_total += P(-1)

    print(f"Part 1: {part1_total}")
    print(f"Part 2: {part2_total}")
    return 0


@dataclass(frozen=True, slots=True)
class Polynomial:
    """Polynomial P of the form P(x) = sum(coef * prod(x - j for j in range(i)) for i, coef in enumerate(coefficients))
    If the list of coefficients is nonempty (assuming trailing zeros are removed), the degree of the polynomial is len(coefficients) - 1.
    Note that P(n) = P(0) + n*Q(n-1) where P(0) = coefficients[0] and Q(x) = sum(coef * prod(x - j for j in range(i)) for i, coef in enumerate(coefficients[1:]))
    is a polynomial of the same form of degree deg(P) - 1. We may inductively build up a polynomial P of degree n through the n+1 points [P(0), P(1), ..., P(n)]
    from lower-degree polynomials of the same form.
    """
    coefficients: list[int]


    def __call__(self, x: int):
        return sum(coef * math.prod(x - j for j in range(i)) for i, coef in enumerate(self.coefficients))


    @property
    def degree(self) -> int:
        delete_trailing_zeros(self.coefficients)
        return 0 if len(self.coefficients) <= 1 else (len(self.coefficients) - 1)


    @classmethod
    def fit(cls, points: list[int]):
        """Fit a degree-n polynomial P of the given form through the n+1 points [P(0), P(1), P(2), ..., P(n)]
        Initially approximates P by a constant zero function, then by a constant function, then a linear function, adding a term of higher degree at each step
        """
        approximation = cls([])
        for i, point_i in enumerate(points):
            approximation.coefficients.append((point_i - approximation(i)) / math.prod(i - j for j in range(i)))
        delete_trailing_zeros(approximation.coefficients)
        return approximation


def delete_trailing_zeros(number_list: list) -> list:
    for item in reversed(number_list):
        if item:
            # Found last nonzero item
            break
        # Last item was zero, so delete from the list
        del number_list[-1]


if __name__ == "__main__":
    main()
