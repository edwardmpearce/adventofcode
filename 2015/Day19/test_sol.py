"""Testing functions for 2015 Day 19

References
- https://docs.pytest.org/en/stable/how-to/fixtures.html
- https://docs.pytest.org/en/latest/how-to/parametrize.html#parametrizemark
"""
import pytest
from sol import (
    solve_part_1,
    solve_part_2,
    distinct_substitution_outcomes,
    split_molecule_by_atom
)


@pytest.mark.parametrize(
    "atom_replacements,start_molecule,expected",
    [
        ({"H": ["HO", "OH"], "O": ["HH"]}, "HOH", 4),
        ({"H": ["HO", "OH"], "O": ["HH"]}, "HOHOHO", 7)
    ]
)
def test_solve_part_1(atom_replacements: dict[str, list[str]], start_molecule: str, expected: int):
    assert solve_part_1(atom_replacements, start_molecule) == expected


@pytest.mark.parametrize(
    "atom_replacements,target_molecule,expected",
    [
        ({"e": ["H", "O"], "H": ["HO", "OH"], "O": ["HH"]}, "HOH", 3),
        ({"e": ["H", "O"], "H": ["HO", "OH"], "O": ["HH"]}, "HOHOHO", 6)
    ]
)
def test_solve_part_2(atom_replacements: dict[str, list[str]], target_molecule: str, expected: int):
    assert solve_part_2(atom_replacements, target_molecule) == expected


@pytest.mark.parametrize(
    "atom_replacements,start_molecule,expected",
    [
        ({"H": ["HO"]}, "HOH", {"HOOH", "HOHO"}),
        ({"H": ["OH"]}, "HOH", {"OHOH", "HOOH"}),
        ({"O": ["HH"]}, "HOH", {"HHHH"}),
        ({"H": ["OO"]}, "H2O", {"OO2O"}),
        ({"H": ["HO", "OH"], "O": ["HH"]}, "HOH", {"HOOH", "HOHO", "OHOH", "HHHH"}),
        ({"H": ["HO", "OH"], "O": ["HH"]}, "HOHOHO", {"HOOHOHO", "HOHOOHO", "HOHOHOO", "OHOHOHO", "HHHHOHO", "HOHHHHO", "HOHOHHH"})
    ]
)
def test_distinct_substitution_outcomes(atom_replacements: dict[str, list[str]], start_molecule: str, expected: set[str]):
    assert distinct_substitution_outcomes(atom_replacements, start_molecule) == expected


@pytest.mark.parametrize(
    "molecule,atom,replacement,expected",
    [
        ("HOH", "H", "HO", {"HOOH", "HOHO"}),
        ("HOH", "H", "OH", {"OHOH", "HOOH"}),
        ("HOH", "O", "HH", {"HHHH"}),
        ("H2O", "H", "OO", {"OO2O"}),
    ]
)
def test_split_molecule_by_atom(molecule: str, atom: str, replacement: str, expected: set[str]):
    assert split_molecule_by_atom(molecule, atom, replacement) == expected
