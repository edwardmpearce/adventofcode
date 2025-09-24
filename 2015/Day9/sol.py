#!/usr/bin/env python3
"""
--- Day 9: All in a Single Night ---
https://adventofcode.com/2015/day/9
Part 1: Minimum weight Hamiltonian path in weighted complete graph
Part 2: Maximum weight Hamiltonian path in weighted complete graph

Background
'In the mathematical field of graph theory, a Hamiltonian path (or traceable path) is
a path in an undirected or directed graph that visits each vertex exactly once.'
'The computational problem of determining whether such paths exist in [arbitrary] graphs is NP-complete;
see [Hamiltonian path problem](https://en.wikipedia.org/wiki/Hamiltonian_path_problem) for details.'
- [Wikipedia](https://en.wikipedia.org/wiki/Hamiltonian_path)

Commentary
The distances between every pair of locations is provided, (i.e. complete (undirected) weighted graph).
In this case any permutation (a.k.a. ordering) of the locations will define a (Hamiltonian) path in the graph.
A straightforward approach to finding the path(s) of minimum/maximum length is to first calculate the length of
every possible path/permutation through the locations. If there are n locations, this has complexity O(n!).
Note that as the graph weights are undirected (same distance in either direction), the length of a path will
be the same when traversing from either end to the other. In this way it is possible to
check the lengths of only half of all possible paths to find the max/min possible path length.

In our case, there are 8 different locations, leading to 8! = 40,320 possible paths through each location.

Relevant References
- https://docs.python.org/3/library/itertools.html
- https://en.wikipedia.org/wiki/Hamiltonian_path
- https://en.wikipedia.org/wiki/Hamiltonian_path_problem
- https://cs.stackexchange.com/questions/163259/shortest-hamiltonian-path-in-a-complete-graph
- https://stackoverflow.com/questions/9092741/algorithm-to-find-a-linear-path-of-minimum-weight-in-a-graph-that-connects-all-t

Extra Reading
- https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
- https://en.wikipedia.org/wiki/Travelling_salesman_problem
- https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm
- https://en.wikipedia.org/wiki/A*_search_algorithm
- https://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html
"""
import os
import itertools

DIRPATH = os.path.dirname(__file__)


def main():
    locations, distances = read_weighted_graph_data()

    route_lengths = {
        route: sum(distances[(loc_1, loc_2)] for loc_1, loc_2 in zip(route, route[1:]))
        for route in itertools.permutations(locations)
    }

    print(f"Part 1: The length of a shortest path through all of the locations is {min(route_lengths.values())}")
    print(f"Part 1: The length of a longest path through all of the locations is {max(route_lengths.values())}")


def read_weighted_graph_data() -> tuple[set[str], dict[tuple[str, str], int]]:
    """Read an input file of distances between pairs of locations and
    return the set of vertices (locations) and a dictionary of edges and weights
    """
    locations: set[str] = set()
    distances: dict[tuple[str, str], int] = {}
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        for line in file:
            start, end, distance = parse_distance_between_locations(line)
            locations |= {start, end}
            distances[(start, end)] = distances[(end, start)] = distance
    return locations, distances


def parse_distance_between_locations(s: str) -> tuple[str, str, int]:
    """Extract the key information from a string of the form `<start> to <end> = <distance>`"""
    location_pair, _, distance = s.partition(" = ")
    start, _, end = location_pair.partition(" to ")
    return start, end, int(distance)


if __name__ == "__main__":
    main()
