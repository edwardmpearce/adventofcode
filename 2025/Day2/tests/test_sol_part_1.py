"""Testing functions for 2025 Day 2 Part 1

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""

import pytest
from solution.part_1 import solve_part_1, find_invalid_ids


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124",
            1227775554
        )
    ]
)
def test_solve_part_1(test_input: str, expected: int):
    assert solve_part_1(test_input) == expected


@pytest.mark.parametrize(
    "start,end,expected",
    [
        (11, 22, [11, 22]),
        (95, 115, [99]),
        (998, 1012, [1010]),
        (1188511880, 1188511890, [1188511885]),
        (222220, 222224, [222222]),
        (1698522, 1698528, []),
        (446443, 446449, [446446]),
        (38593856, 38593862, [38593859]),
        (565653, 565659, []),
        (824824821, 824824827, []),
        (2121212118, 2121212124, []),
    ]
)
def test_find_invalid_ids(start: int, end: int, expected: list[int]):
    assert list(find_invalid_ids(start, end)) == expected
