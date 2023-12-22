#!/usr/bin/env python3
"""
--- Day 16: Ticket Translation ---
https://adventofcode.com/2020/day/16
Part 1: Parse strings of rules on ticket fields (valid ranges), and tickets (comma separated values),
        Then identify invalid tickets, containing value(s) not valid for any ticket field
Part 2: Discarding invalid tickets, determine which ticket field corresponds to each column by the
        examining the values in each column and comparing with the valid ranges for each field.
"""


def main():
    # Load ticket field rules, my ticket, and nearby tickets from file into memory
    rules, my_ticket, nearby_tickets = load_tickets_and_rules("input.txt")

    # Identify any invalid tickets, which contain values not valid for any field
    invalid_tickets = set()
    invalid_vals = []
    for i, ticket in enumerate(nearby_tickets):
        for val in ticket:
            if not any(valid_field(val, field, rules) for field in rules):
                invalid_tickets.add(i)
                invalid_vals.append(val)

    # The ticket scanning error rate is the sum of invalid values on nearby tickets
    # A value is invalid if it is not valid for any field. Union of intervals calculated by hand.
    # error_sum = sum(sum(val * (val < 28 or val > 974) for val in ticket) for ticket in nearby_tickets)
    # assert sum(invalid_vals) == error_sum

    print(f"Found {len(nearby_tickets)} nearby tickets, of which {len(invalid_tickets)} are invalid.")
    print(f"Part 1: The ticket scanning error rate (sum of invalid values) is {sum(invalid_vals)}.")

    valid_tickets = [ticket for i, ticket in enumerate(nearby_tickets) if i not in invalid_tickets]

    # Create a mapping from field_name to potential corresponding column index
    possible_cols = {field: set(range(len(rules))) for field in rules}
    for field in rules:
        # Eliminate the index of any column which contains values outside this field's valid range
        for i in range(len(rules)):
            if not all(valid_field(ticket[i], field, rules) for ticket in valid_tickets):
                possible_cols[field].remove(i)

    # Deduce which column corresponds to each field by process of elimination
    col_index = {}
    for _ in range(len(rules)):
        # Find the next field:column_index pair which is determined by process of elimination
        matched_field, matched_col = find_singleton(possible_cols)

        # Add the matched field:column_index pair to the field:column mapping
        col_index[matched_field] = matched_col

        # Remove the matched field and column from the possible_cols dictionary
        possible_cols.pop(matched_field)
        for field in possible_cols:
            possible_cols[field].discard(matched_col)

    # Interpret departure information from my ticket
    product = 1
    for field, col in col_index.items():
        if "departure" in field:
            product *= my_ticket[col]

    print(f"Part 2: The product of the six values in the departure fields of my ticket is {product}.")

    return 0


def load_tickets_and_rules(filename):
    """Load ticket field rules, my ticket, and nearby tickets from file into memory"""
    with open(filename, 'r') as file:
        line = file.readline()
        # Parse ticket rules and store in memory.
        rules = {}
        while line != '\n':
            field, rule = line.strip().split(": ")
            # Structure for rules dictionary is field_name: ((valid_range1), (valid_range2))
            # where each valid range consists of a pair (lower_bound, upper_bound)
            rules[field] = tuple(map(parse_range, rule.split(" or ")))
            # Read next line in file
            line = file.readline()

        # Read and parse my ticket into memory
        assert file.readline() == "your ticket:\n"
        my_ticket = tuple(map(int, file.readline().strip().split(',')))

        # Read and parse nearby tickets into memory
        assert file.readline() == "\n"
        assert file.readline() == "nearby tickets:\n"
        nearby_tickets = [tuple(map(int, line.strip().split(','))) for line in file]
    return rules, my_ticket, nearby_tickets


def parse_range(s):
    """Parse a string "a-b" describing a range of integers a <= x <= b, returning the bounds a, b."""
    return tuple(map(int, s.split("-")))


def in_range(target, bounds):
    """
    Check whether target integer x lies within the closed interval [a,b]
    where bounds (a,b) are given as a tuple of integers.
    Returns boolean value of the expression a <= x <= b
    """
    lower, upper = bounds
    return lower <= target <= upper


def valid_field(target, field, rules):
    """Check whether the target number lies within the valid range(s) of values
    for a given field according to the rules.
    """
    return any(in_range(target, bounds) for bounds in rules[field])


def find_singleton(input_dict):
    """
    Given an input dictionary of sequences, find a length 1 sequence and return its key and element
    """
    for key, seq in input_dict.items():
        if len(seq) == 1:
            return key, seq.pop()
    # No length 1 sequence (e.g. singleton set) found in the input dictionary
    return False


if __name__ == "__main__":
    main()
