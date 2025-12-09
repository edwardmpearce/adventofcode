"""Testing functions for 2025 Day 2 Part 2

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""

import pytest
from solution.part_2 import solve_part_2, find_invalid_ids, prime_factors_of_numbers_in_range


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124",
            4174379265
        )
    ]
)
def test_solve_part_2(test_input: str, expected: int):
    assert solve_part_2(test_input) == expected


@pytest.mark.parametrize(
    "start,end,expected",
    [
        (11, 22, [11, 22]),
        (95, 115, [99, 111]),
        (998, 1012, [999, 1010]),
        (1188511880, 1188511890, [1188511885]),
        (222220, 222224, [222222]),
        (1698522, 1698528, []),
        (446443, 446449, [446446]),
        (38593856, 38593862, [38593859]),
        (565653, 565659, [565656]),
        (824824821, 824824827, [824824824]),
        (2121212118, 2121212124, [2121212121]),
    ]
)
def test_find_invalid_ids(start: int, end: int, expected: list[int]):
    assert list(find_invalid_ids(start, end)) == expected


@pytest.mark.parametrize(
    "start,end,expected",
    [
        (2, 2, {2}),
        (2, 3, {2, 3}),
        (3, 4, {2, 3}),
        (6, 6, {2, 3}),
        (7, 7, {7}),
        (8, 8, {2}),
        (8, 9, {2, 3}),
        (9, 9, {3}),
        (10, 10, {2, 5}),
        (10, 11, {2, 5, 11}),
        (1, 11, {2, 3, 5, 7, 11}),
    ]
)
def test_prime_factors_of_numbers_in_range(start: int, end: int, expected: set[int]):
    assert prime_factors_of_numbers_in_range(start, end) == expected
