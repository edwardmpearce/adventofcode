#!/usr/bin/env python3
"""
--- Day 14: Docking Data ---
https://adventofcode.com/2020/day/14
Part 1: Bitwise operations, bitmasking to modify values before writing to memory
        See https://en.wikipedia.org/wiki/Mask_(computing)
Part 2: Memory address decoder: Bitmasking with floating bits to modify memory addresses
        See https://www.youtube.com/watch?v=PvfhANgLrm4&ab_channel=RetroGameMechanicsExplained
"""


def main():
    # Represent memory address space as address:value pairs in a dictionary data structure
    memory1, memory2 = {}, {}

    # Initialise variables to record positions of zeros and ones in bitmask (36-bit unsigned integers)
    zero_mask, one_mask = (1 << 36) - 1, 0

    # Read data from input file into memory
    with open("input.txt", 'r') as file:
        for line in file:
            instruction, value = line.strip().split(" = ")

            if instruction == "mask":
                # Part 1: Parse bitmask which acts on values before writing to an address in memory
                zero_mask, one_mask = parse_value_bitmask(value)

                # Part 2: Bitmask acts on addresses before writing values, contains floating bits (X)
                address_mask = value
            else:
                # Parse memory address from instruction in format "mem[address]"
                address = int(instruction[4:-1])
                value = int(value)

                # Part 1: Apply current bitmask to value, then write to address in memory
                memory1[address] = (value & zero_mask) | one_mask

                # Part 2: Apply current bitmask to address and resolve floating bits into address list
                # Format address as 36-bit binary string, then mask
                masked_address = apply_address_mask(f"{address:036b}", address_mask)

                # Resolve bitstring with floating bits into list of all possible values it can take
                addresses = resolve_floating_bits(masked_address)

                # Write the value to the specified memory addresses
                for ptr in addresses:
                    memory2[ptr] = value

    print("Part 1: The sum of memory values after running initialization program with value bitmask is "
            f"{sum(memory1.values())}.")
    print("Part 2: The sum of memory values after running initialization program with address bitmask "
            f"is {sum(memory2.values())}.")

    return 0


def parse_value_bitmask(bitstring):
    """Parse a ternary string specifying a bitmask.
    The bitmask is given as a string of 36 bits, written with the most significant bit on the left
    and the least significant bit on the right. A 0 or 1 overwrites the corresponding bit in the value,
    while an X leaves the bit in the value unchanged.

    Since there are three possible modes for each position in the bitmask, we require more than one
    binary operation, which we separate into a zero_mask and a one_mask for overwriting with 0 and 1,
    respectively. Then to mask the value, we calculate `(value & zero_mask) | one_mask`.

    Truth table: Input I, Mask M, zero_mask Z, one_mask W, Result R; M = (Z,W), R = (I & Z) | W
    I | M | Z | W | R
    0 | 0 | 0 | 0 | 0
    1 | 0 | 0 | 0 | 0
    0 | 1 | 1 | 1 | 1
    1 | 1 | 1 | 1 | 1
    0 | X | 1 | 0 | 0
    1 | X | 1 | 0 | 1
    """
    zero_mask = int("".join(map(lambda c: '1' if c == 'X' else c, bitstring)), base=2)
    one_mask = int("".join(map(lambda c: '0' if c == 'X' else c, bitstring)), base=2)
    return zero_mask, one_mask


def apply_address_mask(address, bitmask):
    """Each bit in the bitmask modifies the corresponding bit of the destination memory address
    in the following way:
        If the bitmask bit is 0, the corresponding memory address bit is unchanged.
        If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
        If the bitmask bit is X, the corresponding memory address bit is floating.
    """
    assert len(address) == len(bitmask)
    return "".join(c1 if c2 == '0' else c2 for c1, c2 in zip(address, bitmask))


def resolve_floating_bits(bitstring):
    """Given a bitstring containing floating bits, return a list of all possible values it can take.

    In electronics, a floating bit is not connected to anything and instead fluctuates unpredictably.
    If a bitstring contains n floating bits (each denoted by 'X'), it can take on 2^n possible values,
    where each floating bit resolves to either 0 or 1 at a given time.
    """
    num_f_bits = bitstring.count('X')
    template = bitstring.replace('X', "{}")
    # Iterate through all binary strings of length num_f_bits to replace floating bits (X) with
    # either '0' or '1' in all possible combinations, then cast the resulting valid bitstrings to int
    values = [int(template.format(*f"{i:0{num_f_bits}b}"), base=2) for i in range(1 << num_f_bits)]
    return values


if __name__ == "__main__":
    main()
