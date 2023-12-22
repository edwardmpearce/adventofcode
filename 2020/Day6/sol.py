#!/usr/bin/env python3
"""
--- Day 6: Custom Customs ---
https://adventofcode.com/2020/day/6
Part 1: Size of set union as the number of elements which are in *any* of the subsets
Part 2: Size of set intersection as the number of elements in *all* of the supersets
"""


def main():
    results = {"passengers": 0, "groups": 0, "any_yes_group_sum": 0, "all_yes_group_sum": 0}

    # Read through input file recording the set of positive responses from each group
    responses = {"any_yes": set(), "all_yes": set("abcdefghijklmnopqrstuvwxyz")}
    with open("input.txt", 'r') as file:
        for line in file:
            # Check for empty line, which signals the end of a group of form responses
            if line != "\n":
                results["passengers"] += 1
                # Collect the set of questions to which this passenger answered 'yes'
                yes_questions = set(line.strip())
                # Union the set of positive responses from this form with the rest of the group
                responses["any_yes"] |= yes_questions
                # Intersect to find questions which all respondents in the group answered positively
                responses["all_yes"] &= yes_questions
            else:
                # Record the current group into the results variable
                results["groups"] += 1
                results["any_yes_group_sum"] += len(responses["any_yes"])
                results["all_yes_group_sum"] += len(responses["all_yes"])
                # Reset the `responses` variable for the next group of passengers
                responses["any_yes"] = set()
                responses["all_yes"] = set("abcdefghijklmnopqrstuvwxyz")

    # Add the form reponses summary from the last group in the input file
    if len(responses["any_yes"]) > 0:
        results["groups"] += 1
        results["any_yes_group_sum"] += len(responses["any_yes"])
        results["all_yes_group_sum"] += len(responses["all_yes"])

    # Print the counts for number of passengers, groups, and questions answered positively by group
    print(f"Found {results['passengers']} passengers collected into {results['groups']} groups.")
    print("For each group, we counted the number of questions to which anyone answered 'yes'.")
    print(f"Part 1: The sum of these 'any_yes' question counts is {results['any_yes_group_sum']}.")
    print("For each group, we counted the number of questions to which everyone answered 'yes'.")
    print(f"Part 2: The sum of these 'all_yes' question counts is {results['all_yes_group_sum']}.")
    return 0


if __name__ == "__main__":
    main()
