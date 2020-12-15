#!/usr/bin/env python3
"""
--- Day 8: Handheld Halting ---
https://adventofcode.com/2020/day/8
Part 1: Simulate fetch-execute cycle on list of boot code instructions to detect infinite cycle.
        See an explanation by Tom Scott at https://www.youtube.com/watch?v=Z5JC9Ve1sfI
Part 2: Repair the boot code by modifying a single instruction so that the program terminates.
"""


def main():
    # Read through the input file and copy bootcode instructions into a list in memory
    boot_code = []
    # Record the indices of each type of operation instruction
    indices = {"acc": [], "jmp": [], "nop": []}
    with open("input.txt", 'r') as file:
        for i, line in enumerate(file):
            # The boot code is represented as a text file with one instruction per line of text. 
            # Each instruction consists of an operation (acc, jmp, or nop) 
            # and an argument (a signed number like +4 or -20).
            op, arg = line.split()
            boot_code.append((op, int(arg)))
            indices[op].append(i)

    exit_i, acc = fetch_execute(boot_code)
    print(f"Part 1: Infinite loop detected! Instruction {exit_i} was read twice.")
    # Immediately before the program would run an instruction a second time
    print(f"Accumulator value at exit was {acc}.")

    # Given that exactly one instruction was corrupted, either one jmp (to nop) or nop (to jmp),
    # we iterate over possible corrupted lines, change the instruction, and check whether the modified
    # program terminates correctly
    termination_line = len(boot_code)
    for op1, op2 in [("jmp", "nop"), ("nop", "jmp")]:
        for i in indices[op1]:
            modified = change_op(boot_code, i, op2)
            exit_i, acc = fetch_execute(modified)
            if exit_i == termination_line:
                print(f"Part 2: Repaired line {i} from {op1} to {op2}.")
                print(f"Program terminated successfully with accumulator value {acc} at exit.")
    return 0


def fetch_execute(instructions):
    """
    Read a list of machine instructions until we read an instruction for a second time (infinite loop)
    or jump to a instruction index outside the bounds of the input list, at which point we return
    the accumulator value (modified by 'acc' operations) and the index `i` which caused program halt
    """
    # Initialize variables for instruction line number and accumulator value
    i, acc = 0, 0
    # Initialize variable to record instructions we have already read in order to catch infinite loops
    visited = set()

    # Iterate through the instructions, updating the accumulator and following jump operations,
    # until we read the same instruction twice (infinite loop), or jump to instruction 
    # index out of bounds. Program terminated successfully if i = len(instructions).
    while 0 <= i < len(instructions):
        # Check for infinite loop
        if i in visited:
            # Infinite loop detected! Instruction `i` was read twice.
            break
        else:
            visited.add(i)

        op, arg = instructions[i]

        if op == "jmp":
            # Jump to next instruction according to relative position (not absolute index/address)
            i += arg
        else:
            # Update accumulator when op == "acc" and ignore when op == "nop"
            acc += arg if op == "acc" else 0
            # Move to next instruction immediately following
            i += 1
    # Infinite loop detected if 0 <= i < len(instructions)
    # Program terminated successfully if i == len(instructions)
    # Otherwise, we jumped to some other instruction outside the range (undefined behaviour)
    return i, acc


def change_op(instructions, i, new_op):
    """
    Return a copy of the `instructions` where the operation at index `i` is changed to `new_op`
    """
    # Store the value of the argument at index `i` in the instructions
    _, arg = instructions[i]
    # Make a copy of the instructions list
    modified = instructions.copy()
    # Update the instruction at index `i` with the new operation whilst keeping the argument unchanged
    modified[i] = (new_op, arg)
    return modified


if __name__ == "__main__":
    main()
