#!/usr/bin/env python3
"""
--- Day 13: Shuttle Search ---
https://adventofcode.com/2020/day/13
Part 1: Find the coset -d + k * ZZ with the smallest nonnegative element
        for a fixed integer d and a list of candidates for k.
Part 2: Solving multiple congruence relations (Chinese remainder theorem)
        Solution exists as input bus IDs are all prime, hence pairwise coprime
        References:
        https://en.wikipedia.org/wiki/Chinese_remainder_theorem
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
"""


def main():
    # Read data from input file into memory
    bus_ids = []
    delays = []
    with open("input.txt", 'r') as file:
        earliest_departure = int(file.readline())
        for i, bus_id in enumerate(file.readline().split(',')):
            if bus_id != 'x':
                bus_ids.append(int(bus_id))
                delays.append(i)

    earliest_bus = min(bus_ids, key=lambda bus_id: wait_until_next_bus(bus_id, earliest_departure))
    min_wait = wait_until_next_bus(earliest_bus, earliest_departure)

    print(f"Part 1: The first bus departing after {earliest_departure} has ID {earliest_bus}.")
    print(f"The waiting time is {min_wait} and the product with bus ID is {earliest_bus * min_wait}.")

    # For part 2, we want to find the smallest nonnegative integer timestamp `t` satisfying
    # (t + delay) % bus_id == 0 for all matching pairs of bus_ids and delays
    # We may express this through congruence relations `t = -delay (mod bus_id)` for bus_ids, delays
    # The solution is bounded above by the product of the input (pairwise coprime) bus IDs
    timestamp, _ = solve_multiple_congruence([-d for d in delays], bus_ids)

    print("Part 2: By solving the corresponding system of congruence equations, we find that")
    print("the earliest timestamp such that all of the listed bus IDs depart at offsets matching")
    print(f"their positions in the list is {timestamp}.")

    return 0


def wait_until_next_bus(bus_id, start):
    # Find the time of the latest bus which departs on or before `start`
    bus_departs = bus_id * (start // bus_id)
    # Find the time of the earliest bus which departs on or after `start`
    if bus_departs < start:
        bus_departs += bus_id
    # Return time from `start` of waiting until next bus on this route
    return bus_departs - start


def extended_euclidean_algorithm(a, b):
    """
    Calculate the highest common factor (hcf) of integers `a` and `b` and the
    coefficients of Bézout's identity, which are integers `x` and `y` such that ax + by = hcf(a,b).
    """
    r0, r1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while r1:
        # q_{i} = r_{i-1} // r_{i}
        q = r0 // r1
        # r_{i+1} = r_{i-1} - q_{i} * r_{i}
        r0, r1 = r1, r0 - q * r1
        # x_{i+1} = x_{i-1} - q_{i} * x_{i}
        x0, x1 = x1, x0 - q * x1
        # y_{i+1} = y_{i-1} - q_{i} * y_{i}
        y0, y1 = y1, y0 - q * y1
    # Verify that when r_{k+1} = 0, the last nonzero remainder r_{k}
    # is the highest common factor of a and b
    assert a % r0 == 0 and b % r0 == 0
    # Verify the corresponding x_{k}, y_{k} are coefficients of Bézout's identity
    assert a * x0 + b * y0 == r0
    # Return the hcf(a,b) and the Bézout coefficients of a, b
    return x0, y0, r0


def solve_congruence_pair(a_i, n_i):
    """
    Solve the system of congruence equations, x = a_{1} (mod n_{1}), x = a_{2} (mod n_{2})
    where n_{1}, n_{2} are coprime.
    For integers m_{1}, m_{2} such that m_{1} * n_{1} + m_{2} * n_{2} = 1,
    then x = a_{2}*m_{1}*n_{1} + a_{1}*m_{2}*n_{2} is a solution.
    """
    (a1, a2), (n1, n2) = a_i, n_i
    m1, m2, _ = extended_euclidean_algorithm(n1, n2)
    return a2 * m1 * n1 + a1 * m2 * n2


def solve_multiple_congruence(a_i, n_i):
    """
    Solve the system of congruence equations, x = a_{i} (mod n_{i}), i = 1, 2, ..., k,
    where n_{i} are pairwise coprime. The Chinese remainder theorem states that
    there is a solution x which is unique modulo N = prod(n_i).
    """
    solution, modulus = a_i[0], n_i[0]
    # Solve the system by solving successive pairs of congruence equations
    for a, n in zip(a_i[1:], n_i[1:]):
        solution = solve_congruence_pair((solution, a), (modulus, n))
        modulus *= n
        solution %= modulus
    # Verify that our calculated solution satisfies all of the required congruence equations
    assert all((solution - a) % n == 0 for a, n in zip(a_i, n_i))
    return solution, modulus


if __name__ == "__main__":
    main()
