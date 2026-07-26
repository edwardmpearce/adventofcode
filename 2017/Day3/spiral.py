"""Utility functions used in Advent of Code 2017 Day 3 (Spiral Memory)"""
from collections.abc import Iterator
from dataclasses import dataclass
from typing import ClassVar, Self


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: int) -> Self:
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int) -> Self:
        """Swap order of operands to re-use implementation of __mul__
        https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types
        """
        return self * scalar

    def __abs__(self) -> int:
        return abs(self.x) + abs(self.y)


def half_line_embedding(n: int) -> Vector:
    """Bijectively embed the positive integers into an infinite 2-dimensional grid by incrementally
    spiralling outwards counterclockwise from the origin starting from 1 |-> (0,0), 2 |-> (0,1).
    """
    if n == 1:
        return Vector(0, 0)
    # Determine the smallest odd square containing the input
    k: int = 1
    while n > (2*k+1)**2:
        k += 1
    # Determine the side of the square containing the input
    q, r = divmod(n - (2*k-1)**2, 2*k)
    match q:
        case 0:
            return Vector(k, r-k)
        case 1:
            return Vector(k-r, k)
        case 2:
            return Vector(-k, k-r)
        case 3:
            return Vector(r-k, -k)
        case 4:
            return Vector(k, -k)


def generate_spiral_adjacent_sum_sequence() -> Iterator[int]:
    """Generate an integer sequence by first embedding the positive integers into an infinite 2-dimensional grid
    by incrementally spiralling outwards counterclockwise from the origin starting from 1 |-> (0,0), 2 |-> (0,1),
    and then assigning a value to each positive integer as the sum of previously assigned values in all
    adjacent squares, including diagonals, starting from initial condition value 1 in square 1 at location (0,0).
    Once a square is written, its value does not change.
    """
    # Store the value 1 in square 1 at location (0,0)
    n = 1
    yield 1
    grid_values: dict[Vector, int] = {Vector(0,0): 1}
    ADJACENT_DIRECTIONS: list[Vector] = [
        Vector(1,0),
        Vector(1,1),
        Vector(0,1),
        Vector(-1,1),
        Vector(-1,0),
        Vector(-1,-1),
        Vector(0,-1),
        Vector(1,-1)
    ]
    while True:
        n += 1
        pos: Vector = half_line_embedding(n)
        # Yield the sum of the previous values in all adjacent squares, including diagonals.
        value: int = sum(grid_values.get(pos + offset, 0) for offset in ADJACENT_DIRECTIONS)
        grid_values[pos] = value
        yield value


class NeighbourSumSpiralFunction:
    """Function on the positive integers obtained by assigning a value to each positive integer as
    the sum of previously assigned values in all adjacent squares, including diagonals, after
    embedding the positive integers into an infinite 2-dimensional grid by spiralling outwards
    counterclockwise from the origin, starting from initial condition value 1 in square 1.
    Once a square is written, its value does not change.
    """
    # Initialise generator and cached values as class variables
    cached_values: ClassVar[list[int]] = []
    _value_generator: ClassVar[Iterator[int]] = generate_spiral_adjacent_sum_sequence()

    def __call__(self, n: int) -> int:
        """Return previously assigned values from memory if available"""
        if n > len(self.cached_values):
            self.cached_values.extend([next(self._value_generator) for _ in range(n - len(self.cached_values))])
        return self.cached_values[n-1]
