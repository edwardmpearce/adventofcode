"""Testing functions for 2017 Day 4

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from sol import no_duplicate_words, no_anagram_words


@pytest.mark.parametrize(
    "passphrase,expected",
    [
        ("aa bb cc dd ee", True),
        ("aa bb cc dd aa", False),
        ("aa bb cc dd aaa", True),
    ]
)
def test_no_duplicate_words(passphrase: str, expected: bool):
    """Part 1 Test Cases"""
    assert no_duplicate_words(passphrase) == expected


@pytest.mark.parametrize(
    "passphrase,expected",
    [
        ("abcde fghij", True),
        ("abcde xyz ecdab", False),
        ("a ab abc abd abf abj", True),
        ("iiii oiii ooii oooi oooo", True),
        ("oiii ioii iioi iiio", False),
    ]
)
def test_no_anagram_words(passphrase: str, expected: bool):
    """Part 2 Test Cases"""
    assert no_anagram_words(passphrase) == expected
