#!/usr/bin/env python3
"""
--- Day 15: Rambunctious Recitation ---
https://adventofcode.com/2020/day/15
Part 1: Implement number memory game which produces a sequence from a list of starting numbers
Part 2: Consider space and runtime complexity as we increase the number of rounds played
"""


def main():
    # Verify that the game has been implemented correctly
    # test_game()

    starting_nums = [19,0,5,1,10,13]

    print(f"We play the game with starting numbers {starting_nums}.")
    for i, n in enumerate([2020, 30000000], 1):
        print(f"Part {i}: The {n}th number in the sequence is {play_game_n_rounds(starting_nums, n)}.")

    return 0


def play_game_n_rounds(starting_nums, n):
    """Given a list of starting numbers, return the number spoken on round n of the game."""
    if n <= len(starting_nums):
        return starting_nums[n-1]

    # Create a dictionary for the most recent two times each number was spoken (if present)
    occurences = {}

    for turn, num in enumerate(starting_nums, 1):
        occurences[num] = (occurences[num][-1], turn) if num in occurences else (turn,)

    num = starting_nums[-1]

    for turn in range(len(starting_nums) + 1, n + 1):
        # Calculate the number that is spoken in this turn
        # If the number spoken on the previous turn is new/not a repeat, then the current player says 0.
        # Otherwise the number spoken on the previous turn is a repeat, and the current player announces
        # how many turns passed between the last turn and the earlier turn when the number was spoken.
        num = 0 if len(occurences[num]) < 2 else turn - 1 - occurences[num][-2]           

        # Update the list of occurences for the number which was announced on this turn
        occurences[num] = (occurences[num][-1], turn) if num in occurences else (turn,)

    return num  


def test_game():
    # Basic tests
    starting_nums = [0, 3, 6]
    sequence = [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]
    for turn, num in enumerate(sequence, 1):
        assert play_game_n_rounds(starting_nums, turn) == num

    # Long range tests
    starters = [[0, 3, 6], [1, 3, 2], [2, 1, 3], [1, 2, 3], [2, 3, 1], [3, 2, 1], [3, 1, 2]]
    for start_seq, expected in zip(starters, [436, 1, 10, 27, 78, 438, 1836]):
        assert play_game_n_rounds(start_seq, 2020) == expected

    # Very longe range tests (compute/time intensive!)
    for start_seq, expected in zip(starters, [175594, 2578, 3544142, 261214, 6895259, 18, 362]):
        assert play_game_n_rounds(start_seq, 30000000) == expected


if __name__ == "__main__":
    main()
