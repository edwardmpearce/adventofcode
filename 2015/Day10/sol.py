#!/usr/bin/env python3
"""
--- Day 10: Elves Look, Elves Say ---
https://adventofcode.com/2015/day/10
Themes: Look-and-Say sequence, iteration (over string objects), running totals

References
- https://en.wikipedia.org/wiki/Look-and-say_sequence
- https://www.youtube.com/watch?v=ea7lJkEhytA
"""
import os

DIRPATH = os.path.dirname(__file__)


def main():
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        seed_digits = file.read()

    # Apply the look-and-say process 40 times on the input seed
    res1 = seed_digits
    for _ in range(40):
        res1 = look_and_say(res1)

    # Apply the look-and-say process 50 times on the input seed, by applying it a further 10 times to the result of part 1
    res2 = res1
    for _ in range(10):
        res2 = look_and_say(res2)

    print(f"Part 1: The answer is {len(res1)}")
    print(f"Part 2: The answer is {len(res2)}")


def look_and_say(digits: str) -> str:
    """Return a string sequence of digits obtained by applying the look-and-say process
    on the input string sequence of digits (left-to-right)
    """
    result = ""
    # Initialise loop variables
    val, count = digits[0], 1
    for d in digits[1:]:
        if d == val:
            # Update the running count of occurrences of the current value
            count += 1
        else:
            # Append the completed run to the result string
            result += f"{count}{val}"
            # Start a new running count
            val, count = d, 1
    # Append the final running count to the result string
    result += f"{count}{val}"
    return result


if __name__ == "__main__":
    main()
