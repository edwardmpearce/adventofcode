"""Testing helper functions for 2025 Day 2

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from solution.helpers import next_id_with_n_repeats


@pytest.mark.parametrize(
    "num,repeats,expected",
    [
        (998, 3, 999),
        (998, 2, 1010),
    ]
)
def test_next_id_with_n_repeats(num: int, repeats: int, expected: list[int]):
    assert next_id_with_n_repeats(num, repeats) == expected
