"""Testing for functions used in the solution to 2025 Day 3

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from sol import find_max_value, find_max_joltage


@pytest.mark.parametrize(
    "bank,expected",
    [
        ("987654321111111", ('9', 0)),
        ("811111111111119", ('9', 14)),
        ("234234234234278", ('8', 14)),
        ("818181911112111", ('9', 6)),
    ]
)
def test_find_max_value(bank: str, expected: tuple[str, int]):
    assert find_max_value(bank) == expected


@pytest.mark.parametrize(
    "bank,num_batteries,expected",
    [
        ("987654321111111", 2, 98),
        ("811111111111119", 2, 89),
        ("234234234234278", 2, 78),
        ("818181911112111", 2, 92),
        ("987654321111111", 12, 987654321111),
        ("811111111111119", 12, 811111111119),
        ("234234234234278", 12, 434234234278),
        ("818181911112111", 12, 888911112111),
    ]
)
def test_find_max_joltage(bank: str, num_batteries: int, expected: int):
    assert find_max_joltage(bank, num_batteries) == expected
