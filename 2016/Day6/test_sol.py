"""Testing functions for 2016 Day 6

References
- https://docs.pytest.org/en/stable/how-to/fixtures.html
"""
import pytest
from sol import decode_repetition_code_by_most_common, decode_repetition_code_by_least_common


@pytest.fixture
def test_messages() -> list[str]:
    return [
        "eedadn",
        "drvtee",
        "eandsr",
        "raavrd",
        "atevrs",
        "tsrnev",
        "sdttsa",
        "rasrtv",
        "nssdts",
        "ntnada",
        "svetve",
        "tesnvt",
        "vntsnd",
        "vrdear",
        "dvrsen",
        "enarar"
    ]


def test_decode_repetition_code_by_most_common(test_messages: list[str]):
    """Part 1 Test Case"""
    assert decode_repetition_code_by_most_common(test_messages) == "easter"


def test_decode_repetition_code_by_least_common(test_messages: list[str]):
    """Part 2 Test Case"""
    assert decode_repetition_code_by_least_common(test_messages) == "advent"
