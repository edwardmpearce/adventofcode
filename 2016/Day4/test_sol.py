"""Testing functions for 2016 Day 4 Part 1

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from sol import RoomData, top_5_letters, right_shift_char


@pytest.mark.parametrize(
    "test_input,encrypted_data,sector_id,checksum",
    [
        ("aaaaa-bbb-z-y-x-123[abxyz]", "aaaaa-bbb-z-y-x", 123, "abxyz"),
        ("a-b-c-d-e-f-g-h-987[abcde]", "a-b-c-d-e-f-g-h", 987, "abcde"),
        ("not-a-real-room-404[oarel]", "not-a-real-room", 404, "oarel"),
        ("totally-real-room-200[decoy]", "totally-real-room", 200, "decoy")
    ]
)
def test_room_data_from_string(test_input: str, encrypted_data: str, sector_id: int, checksum: str):
    assert RoomData.from_string(test_input) == RoomData(encrypted_data, sector_id, checksum)


@pytest.mark.parametrize(
    "encrypted_data,sector_id,checksum,expected",
    [
        ("aaaaa-bbb-z-y-x", 123, "abxyz", True),
        ("a-b-c-d-e-f-g-h", 987, "abcde", True),
        ("not-a-real-room", 404, "oarel", True),
        ("totally-real-room", 200, "decoy", False)
    ]
)
def test_room_data_is_valid(encrypted_data: str, sector_id: int, checksum: str, expected: bool):
    room = RoomData(encrypted_data, sector_id, checksum)
    assert room.is_valid() == expected


@pytest.mark.parametrize(
    "encrypted_data,sector_id,checksum,expected",
    [
        ("qzmt-zixmtkozy-ivhz", 343, "", "very encrypted name")
    ]
)
def test_room_data_decrypt(encrypted_data: str, sector_id: int, checksum: str, expected: bool):
    room = RoomData(encrypted_data, sector_id, checksum)
    assert room.decrypt() == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("aaaaa-bbb-z-y-x", "abxyz"),
        ("a-b-c-d-e-f-g-h", "abcde"),
        ("not-a-real-room", "oarel"),
        ("totally-real-room", "loart")
    ]
)
def test_top_5_letters(test_input: str, expected: str):
    assert top_5_letters(test_input.replace("-", "")) == expected


@pytest.mark.parametrize(
    "char,shift,expected",
    [
        ("d", -3, "a"),
        ("d", 23, "a"),
        ("e", 5, "j"),
        ("x", 15, "m")
    ]
)
def test_right_shift_char(char: str, shift: int, expected: str):
    assert right_shift_char(char, shift) == expected
