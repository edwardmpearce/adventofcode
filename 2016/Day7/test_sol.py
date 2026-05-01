"""Testing functions for 2016 Day 7

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from sol import supports_tls, has_abba, supports_ssl, find_aba_sequences


@pytest.mark.parametrize(
    "address,expected",
    [
        ("abba[mnop]qrst", True),
        ("abcd[bddb]xyyx", False),
        ("aaaa[qwer]tyui", False),
        ("ioxxoj[asdfgh]zxcvbn", True)
    ]
)
def test_supports_tls(address: str, expected: bool):
    assert supports_tls(address) == expected


@pytest.mark.parametrize(
    "sequence,expected",
    [
        ("abba", True),
        ("[mnop]", False),
        ("qrst", False),
        ("abcd", False),
        ("[bddb]", True),
        ("xyyx", True),
        ("aaaa", False),
        ("[qwer]", False),
        ("tyui", False),
        ("ioxxoj", True),
        ("[asdfgh]", False),
        ("zxcvbn", False),
        ("aaaabba", True),
    ]
)
def test_has_abba(sequence: str, expected: bool):
     assert has_abba(sequence) == expected


@pytest.mark.parametrize(
    "address,expected",
    [
        ("aba[bab]xyz", True),
        ("xyx[xyx]xyx", False),
        ("aaa[kek]eke", True),
        ("zazbz[bzb]cdb", True)
    ]
)
def test_supports_ssl(address: str, expected: bool):
    assert supports_ssl(address) == expected


@pytest.mark.parametrize(
    "sequence,expected",
    [
        ("aba[bab]xyz", {"aba", "bab"}),
        ("xyx[xyx]xyx", {'x[x', 'x]x', 'xyx'}),
        ("aaa[kek]eke", {"kek", "eke"}),
        ("zazbz[bzb]cdb", {"zaz", "zbz", "bzb"})
    ]
)
def test_find_aba_sequences(sequence: str, expected: bool):
     assert find_aba_sequences(sequence) == expected
