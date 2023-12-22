#!/usr/bin/env python3
"""
--- Day 7: Handy Haversacks ---
https://adventofcode.com/2020/day/7
Part 1: Depth-First Search, existence of path between nodes in a directed graph
Part 2: Recursively count the number of descendents of a node in a directed acyclic graph
"""

# Standard library imports
from collections import defaultdict


def main():
    # Read through the input file compiling a dictionary of bag types and their rules on subbags
    regulations = load_luggage_regulations("input.txt")
    print(f"Regulations found for {len(regulations)} different types of bag!")

    # Partition the bag colours in the `regulations` into two disjoint subsets:
    # Those which contain a shiny gold bag as a descendant and those which do not.
    # For each bag type in the regulations, we depth-first search through the dependency tree
    # for a path from the starting bag type to a shiny gold bag.
    ancestors, nonancestors = get_ancestors(regulations, "shiny gold")

    print(f"Part 1: Found {len(ancestors)} bag types which have a shiny gold bag as a descendent.\n"
            f"\tFound {len(nonancestors)} bag types which do not have a shiny gold bag as an descendent.")

    # Count the number of individual bags required inside a single shiny gold bag
    descendents = count_descendents(regulations, "shiny gold")

    print(f"Part 2: A single shiny gold bag is required to contain {descendents} other bags.")
    return 0


def load_luggage_regulations(filename):
    """Load luggage regulations from input file into dictionary of bag types and their rules on subbags"""
    regulations = defaultdict(dict)
    with open(filename, 'r') as file:
        for line in file:
            # Example line: "plaid fuchsia bags contain 5 light violet bags, 1 light yellow bag.\n"
            superbag, rules = line.split("contain")
            bag_type = superbag.rsplit(maxsplit=1)[0]
            for rule in rules.split(","):
                if len(rule.split()) == 3:
                    # rule == "no other bags."
                    regulations[bag_type] = {}
                else:
                    # rule == "{num} {pattern} {colour} bag(s)"
                    num, pattern, colour, _ = rule.split()
                    # Example dict item: "plaid fuchsia: {'light violet': '5', 'light yellow': '1'}"
                    regulations[bag_type][pattern + " " + colour] =  int(num)
    return regulations


def get_ancestors(graph, target):
    """
    Partition the nodes of a graph into two disjoint subsets:
    those which contain the target node as a descendant and those which do not.

    For each node in the graph, we depth-first search through the graph to find a path from the
    the starting node to the target node. If we can find a path to the target node, we add it to
    the set of `ancestors` of the `target`, otherwise we add it to the set of `nonancestors`.
    """
    # Initialize the `ancestors` and `nonancestors` variables as empty sets
    ancestors, nonancestors = set(), set()

    for node in graph.copy():
        path_exists = search(graph, node, target)
        if path_exists:
            ancestors.add(node)
        else:
            nonancestors.add(node)

    return ancestors, nonancestors


def search(graph, start, target, avoiding=None):
    """Depth-first search through graph for path from start to target avoiding visited nodes"""
    # Initialize the set of visited nodes to avoid in the search if not passed as argument
    avoiding = {start} if not avoiding else avoiding
    for child in graph[start]:
        if child in avoiding:
            continue
        # In subsequent recursive calls to the search function we add to the set of visited nodes
        elif child == target or search(graph, child, target, avoiding | {child}):
            return True
    # No path exists from start to target (via any of its children, avoiding the specified nodes)
    return False


def count_descendents(graph, root):
    """
    Inputs: A weighted directed acyclic `graph` with positive edge weights and a starting `root` node
    Let the weight of a path in the graph be the product of the weights of its constituent edges
    and 0 if the path is trivial with no edges
    Returns: The sum of the weights of all paths in the graph starting at the `root` node
    """
    if len(graph[root]) == 0:
        # `root` has no children, so no (paths to) descendents contributing to the sum/count
        return 0
    # Iterate over each child, multiplying by the weight of edge from root to child before recursing
    # This counts the child node itself as well as all of the higher degree descendents
    return sum(count * (1 + count_descendents(graph, node)) for node, count in graph[root].items())


if __name__ == "__main__":
    main()
