"""

Functions
- Data Parsing
  - get_puzzle_input
  - parse_ranges
- Repetitive strings
  - is_repeated_sequence: Check whether the input string is composed of an exact number of repeats of a substring.
  - next_id_with_n_repeats: Return the smallest integer that is greater than the input and consists of a subsequence of digits repeated a given number of times.
- Mathematical generator functions
  - primes: Returns a list of primes < n via sieve
  - prime_factors: Yield prime factors of n according to multiplicity.

References
- Generating Prime Numbers
  - https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
  - https://stackoverflow.com/questions/11619942/print-series-of-prime-numbers-in-python
  - https://stackoverflow.com/questions/567222/simple-prime-number-generator-in-python
  - https://code.activestate.com/recipes/117119/
  - https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n
  - https://docs.python.org/3/library/itertools.html
  - https://pypi.org/project/more-itertools/
"""
import os
from collections.abc import Iterator
from math import isqrt


def get_puzzle_input() -> str:
    with open(os.path.join(os.path.dirname(__file__), "../input.txt"), 'r') as file:
        return file.read()


def parse_ranges(puzzle_input: str) -> list[tuple[int, int]]:
    return [tuple(map(int, s.split("-"))) for s in puzzle_input.split(",")]


def is_repeated_sequence(s: str, repeats: int) -> bool:
    """Check whether the input string is composed of an exact number of repeats of a substring."""
    s_len = len(s)
    if s_len % repeats:
        # Length of s is not a multiple of the number of repeats
        return False
    else:
        subsequence_len = s_len // repeats
        # Check whether initial subsequence repeats through the rest of the string
        return s[subsequence_len:] == s[:subsequence_len] * (repeats - 1)


def next_id_with_n_repeats(num: int, repeats: int) -> int:
    """Return the smallest integer that is greater than the input and
    consists of a subsequence of digits repeated a given number of times.
    """
    assert num >= 0
    num_str = str(num)
    num_digits = len(num_str)

    if num_digits % repeats:
        return int(str(10 ** (num_digits // repeats)) * repeats)
    else:
        initial_subseq = num_str[:num_digits // repeats]
        repeat_candidate = int(initial_subseq * repeats)
        return repeat_candidate if num < repeat_candidate else int(str(int(initial_subseq) + 1) * repeats)


def primes(n: int) -> list[int]:
    """Returns a list of primes < n
    Sieve of Eratosthenes with shortcuts (half-sieve, even number skip, square root skip, slice assignment instead of loop)

    https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """
    sieve = [True] * (n // 2)
    for i in range(3, isqrt(n)+1, 2):
        if sieve[i // 2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
    return [2] + [2*i+1 for i in range(1,n//2) if sieve[i]]


def prime_factors(n: int) -> Iterator[int]:
    """Yield prime factors of n according to multiplicity.
    - factor(99) → 3 3 11
    - factor(1_000_000_000_000_007) → 47 59 360620266859
    - factor(1_000_000_000_000_403) → 1000000000000403

    https://docs.python.org/3/library/itertools.html
    """
    for prime in primes(isqrt(n) + 1):
        while not n % prime:
            yield prime
            n //= prime
            if n == 1:
                return
    if n > 1:
        yield n
