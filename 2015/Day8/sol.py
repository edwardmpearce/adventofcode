#!/usr/bin/env python3
"""
--- Day 8: Matchsticks ---
https://adventofcode.com/2015/day/8
Themes: Escaping special characters, representation in computer memory, string encoding and decoding

References
- https://docs.python.org/3/library/ast.html#ast.literal_eval
- https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/
"""
import os
import ast

DIRPATH = os.path.dirname(__file__)


def main():
    """Note: This script uses a couple of examples of runtime testing using `assert` statements to verify intended program behaviour"""
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        literal_strings: list[str] = [line.strip() for line in file]

    character_counts: dict[str, int] = {
        "literal_strings": sum(len(s_literal) for s_literal in literal_strings),
        "in-memory strings": sum(len(ast.literal_eval(s_literal)) for s_literal in literal_strings),
        "encoded string literals": sum(len(encode_string(s_literal)) for s_literal in literal_strings)
    }

    part_1_answer = character_counts["literal_strings"] - character_counts["in-memory strings"]
    part_2_answer_direct = character_counts["encoded string literals"] - character_counts["literal_strings"]
    # It is possible to calculate the answer to part 2 without directly encoding the input string literals
    part_2_answer_indirect = sum(2 + s.count("\\") + s.count("\"") for s in literal_strings)
    assert part_2_answer_direct == part_2_answer_indirect

    print(f"Part 1: The answer is {part_1_answer}")
    print(f"Part 2: The answer is {part_2_answer_direct}")


def encode_string(s: str) -> str:
    """Returns an encoded string which will produce the input string `s` when passed to `ast.literal_eval`.
    Escapes the special characters (single backslash) and (single double-quote) in string literals by adding a leading backslash,
    and concatenates a double-quote character to the start and end of the result.
    Note: The order of `replace` operations in this implementation is important to avoid double-escaping.
    """
    encoded_s = f"\"{s.replace("\\", "\\\\").replace("\"", "\\\"")}\""
    assert ast.literal_eval(encoded_s) == s
    return encoded_s


if __name__ == "__main__":
    main()
