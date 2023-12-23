#!/usr/bin/env python3
"""
--- Day 4: Scratchcards ---
https://adventofcode.com/2023/day/4
Part 1: Set intersection
Part 2: Sequential propogation
"""
from collections import Counter


def main():
    points_total = 0
    scratchcard_counter = Counter()
    with open("input.txt", 'r') as file:
        for idx, line in enumerate(file):
            # Parse each line representing a scratchcard
            # Each card has two lists of numbers separated by a vertical bar (|): a list of winning numbers and then a list of numbers you have.
            _, card_data = line.strip().split(": ")
            winning_numbers, player_numbers = map(lambda s: set(map(int, s.split())), card_data.split(" | "))
            num_winning_player_numbers = len(winning_numbers & player_numbers)

            # Part 1: A winning card is worth points equal to 2**(num_matches - 1)
            points_total += 1 << (num_winning_player_numbers - 1) if num_winning_player_numbers > 0 else 0

            # Part 2: Count the original card, then add copies of the scratchcards below the winning card equal to the number of matches
            # Cards will never make you copy a card past the end of the table.
            scratchcard_counter[idx] += 1
            for i in range(num_winning_player_numbers):
                scratchcard_counter[idx + i+1] += scratchcard_counter[idx]

    print(f"Part 1: In total, the cards are worth {points_total} points")
    print(f"Part 2: After processing all of the original and copied scratchcards, there are {scratchcard_counter.total()} scratchcards in total.")


if __name__ == "__main__":
    main()
