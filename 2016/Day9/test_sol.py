"""Testing functions for 2016 Day 9

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from sol import decompress, calculate_recursive_decompressed_length


@pytest.mark.parametrize(
    "compressed_text,expected",
    [
        ("ADVENT", "ADVENT"),
        ("A(1x5)BC", "ABBBBBC"),
        ("(3x3)XYZ", "XYZXYZXYZ"),
        ("A(2x2)BCD(2x2)EFG", "ABCBCDEFEFG"),
        ("(6x1)(1x3)A", "(1x3)A"),
        ("X(8x2)(3x3)ABCY", "X(3x3)ABC(3x3)ABCY"),
    ]
)
def test_decompress(compressed_text: str, expected: str):
    assert decompress(compressed_text) == expected


@pytest.mark.parametrize(
    "compressed_text,expected",
    [
        ("ADVENT", 6),
        ("A(1x5)BC", 7),
        ("(3x3)XYZ", 9),
        ("A(2x2)BCD(2x2)EFG", 11),
        ("(6x1)(1x3)A", 3),
        ("X(8x2)(3x3)ABCY", 20),
        ("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920),
        ("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", 445),
    ]
)
def test_calculate_recursive_decompressed_length(compressed_text: str, expected: str):
    assert calculate_recursive_decompressed_length(compressed_text) == expected
