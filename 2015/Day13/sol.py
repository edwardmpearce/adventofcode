#!/usr/bin/env python3
"""
--- Day 13: Knights of the Dinner Table ---
https://adventofcode.com/2015/day/13

Functions
- main: Read the puzzle inputs, then calculate and print the puzzle answers
- read_input_data: Read an input file of the payoffs (in happiness units), positive or negative, that a person would receive by sitting next to a particular other person
- calculate_seating_arrangement_payoff: Calculate the overall payoff for a given circular seating arrangement
- generate_all_circular_seating_arrangements: Generate all possible unique arrangments of the input elements into a circle
"""
import os
from collections.abc import Iterator
import itertools


DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    guests, payoffs = read_input_data()
    optimal_seating_arrangement_payoff = max(
        calculate_seating_arrangement_payoff(arrangement, payoffs)
        for arrangement in generate_all_circular_seating_arrangements(guests)
    )
    print(f"Part 1: The optimal seating arrangement yields {optimal_seating_arrangement_payoff} happiness units")

    # Part 2: Update the payoffs dictionary and set of attendees
    host = "You"
    for guest in guests:
        payoffs[(host, guest)] = payoffs[(guest, host)] = 0
    optimal_seating_arrangement_payoff_inc_host = max(
        calculate_seating_arrangement_payoff(arrangement, payoffs)
        for arrangement in generate_all_circular_seating_arrangements({host} | guests)
    )
    print(f"Part 2: Including yourself as the host, the optimal seating arrangement yields {optimal_seating_arrangement_payoff_inc_host} happiness units")


def read_input_data() -> tuple[set[str], dict[tuple[str, str], int]]:
    """Read an input file of the payoffs (in happiness units), positive or negative,
    that a person would receive by sitting next to a particular other person
    """
    payoff_signs = {"gain": 1, "lose": -1}
    people: set[str] = set()
    payoffs: dict[tuple[str, str], int] = {}
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        for line in file:
            words = line.split()
            person, neighbour, sign, payoff = words[0], words[-1][:-1], words[2], int(words[3])
            people.add(person)
            payoffs[(person, neighbour)] = payoff_signs[sign] * payoff

    return people, payoffs


def calculate_seating_arrangement_payoff(arrangement: list[str], payoffs: dict[tuple[str, str], int]) -> int:
    """Calculate the overall payoff for a given circular seating arrangement
    Accounts for payoffs in both directions and at the ends of the list representing the circle
    """
    p_first, p_last = arrangement[0], arrangement[-1]
    total_payoff = payoffs[(p_first, p_last)] + payoffs[(p_last, p_first)]
    for p1, p2 in zip(arrangement, arrangement[1:]):
        total_payoff += payoffs[(p1, p2)] + payoffs[(p2, p1)]
    return total_payoff


def generate_all_circular_seating_arrangements(people: set[str]) -> Iterator[tuple[str]]:
    """Generate all possible unique arrangments of the input elements into a circle
    Circular arrangements are represented by an ordered tuple of people and we fix a starting person
    to avoid counting duplicate/equivalent arrangements which differ by a rotation
    """
    # Convert the set of people to an ordered tuple for indexing
    people = tuple(people)
    for perm in itertools.permutations(people[1:]):
        yield people[0], *perm


if __name__ == "__main__":
    main()
