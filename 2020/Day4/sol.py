#!/usr/bin/env python3
"""
--- Day 4: Passport Processing ---
https://adventofcode.com/2020/day/4
Part 1: Process a batch file of passports consisting of `key:value` pairs separated by spaces
        or newlines. Passports are separated by blank lines. Count the number of passports for
        which all seven necessary fields (keys) are present.
Part 2: Count the number of passports with all necessary fields present and valid (by value).
"""


def main():
    validity_checks = {
    "byr": check_birth_year,
    "iyr": check_issue_year,
    "eyr": check_expiration_year,
    "hgt": check_height,
    "hcl": check_hair_colour,
    "ecl": check_eye_colour,
    "pid": check_passport_id
    }
    results = {"total": 0, "fields_present": 0, "fields_valid": 0}

    # Read through input file adding `key:value` pairs to a temporary dictionary
    passport = {}
    with open("input.txt", 'r') as file:
        for line in file:
            # Check for empty line, which signals the end of a passport entry
            if line != "\n":
                # Add the `key:value` pairs from this line to the current passport entry
                passport.update(keyval.split(":") for keyval in line.split())
            else:
                # Record the current passport into the results variable
                results["total"] += 1
                # Check this passport entry contains the seven necessary fields
                if check_fields_present(passport, validity_checks):
                    results["fields_present"] += 1
                    # Further check that all required fields pass the validation checks
                    results["fields_valid"] += check_fields_valid(passport, validity_checks)
                # Reset the `passport` variable to an empty dictionary
                passport = {}

    # Check validity of the final passport in the input file
    results["total"] += len(passport) > 0
    if check_fields_present(passport, validity_checks):
        results["fields_present"] += 1
        # Further check that all required fields pass the validation checks
        results["fields_valid"] += check_fields_valid(passport, validity_checks)

    # Print the count of valid passports
    print(f"Found {results['total']} passports")
    print(f"Part 1: {results['fields_present']} passports had all 7 necessary fields")
    print(f"Part 2: {results['fields_valid']} passports had all required fields present and valid")
    return 0


def check_fields_present(passport, validity_checks):
    """Check that all of the required fields are present as keys in the input dictionary"""
    return validity_checks.keys() <= passport.keys()


def check_fields_valid(passport, validity_checks):
    """Automatic validation checks for passport fields. Returns bool."""
    return all(check(passport[field]) for field, check in validity_checks.items())


def check_birth_year(val):
    """byr (Birth Year) - four digits; at least 1920 and at most 2002."""
    return len(val) == 4 and 1920 <= int(val) <= 2002


def check_issue_year(val):
    """iyr (Issue Year) - four digits; at least 2010 and at most 2020."""
    return len(val) == 4 and 2010 <= int(val) <= 2020


def check_expiration_year(val):
    """eyr (Expiration Year) - four digits; at least 2020 and at most 2030."""
    return len(val) == 4 and 2020 <= int(val) <= 2030


def check_height(val):
    """hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    """
    units = val[-2:]
    if units == "cm":
        return 150 <= int(val[:-2]) <= 193
    elif units == "in":
        return 59 <= int(val[:-2]) <= 76
    else:
        return False


def check_hair_colour(val):
    """hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f."""
    return len(val) == 7 and val[0] == '#' and all(c in "0123456789abcdef" for c in val[1:])


def check_eye_colour(val):
    """ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth."""
    return val in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def check_passport_id(val):
    """pid (Passport ID) - a nine-digit number, including leading zeroes."""
    return len(val) == 9 and val.isdigit()


if __name__ == "__main__":
    main()
