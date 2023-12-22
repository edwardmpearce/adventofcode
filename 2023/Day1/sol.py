#!/usr/bin/env python3
"""
--- Day 1: Trebuchet?! ---
https://adventofcode.com/2023/day/1
Part 1: Character search
Part 2: Substring search

References
- https://docs.python.org/3/library/stdtypes.html
- https://stackoverflow.com/questions/22789392/str-isdecimal-and-str-isdigit-difference-example
- https://en.wikipedia.org/wiki/Trie
- https://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python
- https://news.ycombinator.com/item?id=38483271
  - https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm

"""

def main():
    # Setup for solution using built-in str.find method
    digit_chars = {char: int(char) for char in "123456789"}
    digit_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    # Trie solution setup
    digit_words_trie = {
        "o": {"n": {"e": 1}},
        "t": {"w": {"o": 2},
            "h": {"r": {"e": {"e": 3}}}
            },
        "f": {"o": {"u": {"r": 4}},
            "i": {"v": {"e": 5}}
            },
        "s": {"i": {"x": 6},
            "e": {"v": {"e": {"n": 7}}}
            },
        "e": {"i": {"g": {"h": {"t": 8}}}},
        "n": {"i": {"n": {"e": 9}}}
    }
    reversed_digit_words_trie = {
        "e": {"n": {"o": 1,
                    "i": {"n": 9}},
              "e": {"r": {"h": {"t": 3}}},
              "v": {"i": {"f": 5}}
              },
        "o": {"w": {"t": 2}},
        "r": {"u": {"o": {"f": 4}}},
        "x": {"i": {"s": 6}},
        "n": {"e": {"v": {"e": {"s": 7}}}},
        "t": {"h": {"g": {"i": {"e": 8}}}}
    }

    # Initialise running total variables
    line_results = {
        "built-in method": {
            "Part 1": None,
            "Part 2": None
        },
        "trie method": {
            "first": None,
            "last": None
        }
    }
    totals = {
        "built-in method": {
            "Part 1": 0,
            "Part 2": 0
        },
        "trie method": {
            "Part 1": 0,
            "Part 2": 0
        }
    }

    with open("input.txt", 'r') as file:

        for line in file:
            # Pythonic Solution: Use built-in functions and methods and don't worry about complexity too much
            line_results["built-in method"]["Part 1"] = substring_search(line, digit_chars)
            line_results["built-in method"]["Part 2"] = substring_search(line, digit_chars | digit_words)
            totals["built-in method"]["Part 1"] += 10 * line_results["built-in method"]["Part 1"]["first"]["value"] + line_results["built-in method"]["Part 1"]["last"]["value"]
            totals["built-in method"]["Part 2"] += 10 * line_results["built-in method"]["Part 2"]["first"]["value"] + line_results["built-in method"]["Part 2"]["last"]["value"]
            # Algorithmic Solution: Attempt to be more computationally and memory efficient by using trie data structure
            line_results["trie method"]["first"] = find_trie_word_or_digit(line, digit_words_trie)
            line_results["trie method"]["last"] = find_trie_word_or_digit("".join(reversed(line)), reversed_digit_words_trie)
            totals["trie method"]["Part 1"] += 10 * line_results["trie method"]["first"]["digit_char"]["value"] + line_results["trie method"]["last"]["digit_char"]["value"]
            totals["trie method"]["Part 2"] += 10 * line_results["trie method"]["first"]["trie_word_or_char"]["value"] + line_results["trie method"]["last"]["trie_word_or_char"]["value"]

    for method, part_totals in totals.items():
        for part_num, total in part_totals.items():
            print(f"{part_num} ({method}): The sum of all of the calibration values is {total}")
    return 0


def substring_search(search_string: str, substring_dict: dict[str, int]) -> dict:
    """Returns the index of the first occurence of a dictionary key within a string and its corresponding value, and similarly for the last occurence
    Assumes any(substr in search_string for substr in substring_dict) == True
    """
    results = {
        "first": {
            "index": len(search_string),
            "key": "",
            "value": None
        },
        "last": {
            "index": -1,
            "key": "",
            "value": None
        }
    }
    for substr, value in substring_dict.items():
        if substr in search_string:
            substr_lowest_index = search_string.find(substr)
            if substr_lowest_index < results["first"]["index"]:
                results["first"]["index"] = substr_lowest_index
                results["first"]["key"] = substr
                results["first"]["value"] = value
            substr_highest_index = search_string.rfind(substr)
            if substr_highest_index > results["last"]["index"]:
                results["last"]["index"] = substr_highest_index
                results["last"]["key"] = substr
                results["last"]["value"] = value
    return results


def find_trie_word_or_digit(s: str, trie: dict):
    """Returns the index of the first occurence of a trie word or digit within a string, and its corresponding trie value"""
    result = {
        "digit_char": {
            "index": len(s),
            "value": None
        },
        "trie_word_or_char": {
            "index": len(s),
            "value": None
        }
    }
    found_trie_word = False
    # Read line from start
    for index, char in enumerate(s):
        if char.isdigit():
            result["digit_char"]["index"] = index
            result["digit_char"]["value"] = int(char)
            if not found_trie_word:
                # Found a digit before a trie word
                result["trie_word_or_char"]["index"] = index
                result["trie_word_or_char"]["value"] = int(char)
            break
        # Check for possible start of first trie word if not already found
        if not found_trie_word and char in trie:
            # Check for trie word as substring in s starting from current index
            found_trie_word, trie_value = trie_startswith_lookup(trie, s[index:])
            if found_trie_word:
                result["trie_word_or_char"]["index"] = index
                result["trie_word_or_char"]["value"] = trie_value
    return result


def trie_startswith_lookup(trie: dict, s: str) -> tuple[bool, int | None]:
    """Modified prefix tree lookup. Trie values are integers at leaf nodes only."""
    current_dict = trie
    for c in s:
        temp = current_dict.get(c)
        if temp is None:
            # Start of s does not match any value in trie
            return False, None
        elif isinstance(temp, int):
            # The string s starts with a word in the trie, return the corresponding value
            return True, temp
        elif isinstance(temp, dict):
            # Current character c is not the end of a word in the trie
            current_dict = temp
    # Reached the end of s without completing a word in the trie
    return False, None


if __name__ == "__main__":
    main()
