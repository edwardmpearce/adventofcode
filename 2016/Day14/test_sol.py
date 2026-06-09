"""Testing functions for 2016 Day 14

References
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
from typing import Callable
import pytest
from sol import (
    md5_message_digest,
    stretched_md5_message_digest,
    generate_one_time_pad_keys,
    solve_part_1,
    solve_part_2
)


def test_md5_message_digest():
    assert md5_message_digest(salt="abc", idx=0) == "577571be4de9dcce85a041ba0410f29f"


def test_stretched_md5_message_digest():
    assert stretched_md5_message_digest(salt="abc", idx=0) == "a107ff634856bb300138cac6568c0f24"


@pytest.mark.parametrize(
    "salt,hash_function,key_number,expected",
    [
        ("abc", md5_message_digest, 1, 39),
        ("abc", md5_message_digest, 2, 92),
        ("abc", md5_message_digest, 64, 22728),
        ("abc", stretched_md5_message_digest, 1, 10),
        ("abc", stretched_md5_message_digest, 64, 22551),
    ]
)
def test_generate_one_time_pad_keys(salt: str, hash_function: Callable[[str, int], str], key_number: int, expected: int):
    key_generator = generate_one_time_pad_keys(salt=salt, hash_function=hash_function)
    for _ in range(key_number):
        hash_idx, _ = next(key_generator)
    assert hash_idx == expected


def test_solve_part_1():
    """Part 1 Test Case"""
    assert solve_part_1(salt="abc") == 22728


def test_solve_part_2():
    """Part 2 Test Case"""
    assert solve_part_2(salt="abc") == 22551
