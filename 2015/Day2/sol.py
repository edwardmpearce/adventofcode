#!/usr/bin/env python3
"""
--- Day 2: I Was Told There Would Be No Math ---
https://adventofcode.com/2015/day/2
"""
from __future__ import annotations
import os
from dataclasses import dataclass


DIRPATH = os.path.dirname(__file__)


@dataclass(frozen=True)
class Rectangle:
    length: int
    width: int

    @property
    def area(self) -> int:
        return self.length * self.width

    @property
    def perimeter(self) -> int:
        return 2 * (self.length + self.width)


@dataclass(frozen=True)
class Cuboid:
    length: int
    width: int
    height: int

    @property
    def volume(self) -> int:
        return self.length * self.width * self.height

    @property
    def surface_area(self) -> int:
        return 2 * (self.length * (self.width + self.height) + self.width * self.height)

    def sorted_side_lengths(self) -> list[int]:
        """Return the side lengths as a list in ascending order"""
        return sorted([self.length, self.width, self.height])

    @property
    def smallest_face(self) -> Rectangle:
        l0, l1, l2 = self.sorted_side_lengths()
        return Rectangle(l0, l1)


@dataclass(frozen=True)
class GiftBox(Cuboid):
    def required_wrapping_paper(self) -> int:
        return self.surface_area + self.smallest_face.area

    def required_ribbon(self) -> int:
        return self.smallest_face.perimeter + self.volume


def main():
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        boxes: list[GiftBox] = [GiftBox(*map(int, line.split('x'))) for line in file]

    total_wrapping_paper = sum(box.required_wrapping_paper() for box in boxes)
    print(f"Part 1: The total required wrapping paper is {total_wrapping_paper:,} square feet")

    total_ribbon = sum(box.required_ribbon() for box in boxes)
    print(f"Part 2: The total required ribbon in {total_ribbon:,} feet")


if __name__ == "__main__":
    main()
