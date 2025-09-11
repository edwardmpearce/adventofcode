#!/usr/bin/env python3
"""
--- Day 8: Haunted Wasteland ---
https://adventofcode.com/2023/day/8
Part 1: Navigating a directed graph via Deterministic Finite Automata
Part 2: Multiple Deterministic Finite Automata and the Chinese reaminder theorem

References
- Deterministic Finite Automata/State Machines
  - https://en.wikipedia.org/wiki/Deterministic_finite_automaton
  - https://www.youtube.com/watch?v=32bC33nJR3A
  - https://en.wikipedia.org/wiki/Finite-state_machine
  - https://en.wikipedia.org/wiki/Automata-based_programming
- DFA minimization and Hopcroft's Algorithm
  - https://en.wikipedia.org/wiki/DFA_minimization
  - https://www.youtube.com/watch?v=oHVHkkah3MY
  - https://stackoverflow.com/questions/26727766/hopcrofts-algorithm-dfa-minimization
  - https://stackoverflow.com/questions/13549662/dfa-minimization-by-hopcroft-algorithm
  - http://i.stanford.edu/pub/cstr/reports/cs/tr/71/190/CS-TR-71-190.pdf
  - https://web.archive.org/web/20090117201637/http://www.dcc.fc.up.pt/dcc/Pubs/TReports/TR07/dcc-2007-03.pdf
  - https://web.archive.org/web/20150621004621/http://www8.cs.umu.se/kurser/TDBC92/VT06/final/1.pdf
- Dataclasses
  - https://www.youtube.com/watch?v=vBH6GRJ1REM
  - https://www.youtube.com/watch?v=CvQ7e6yUtnw
  - https://docs.python.org/3/library/dataclasses.html
- Chinese remainder theorem
  - https://en.wikipedia.org/wiki/Chinese_remainder_theorem
"""
from dataclasses import dataclass, replace
from math import gcd, lcm


def main():
    with open("input.txt", 'r') as file:
        instructions = file.readline().strip()
        alphabet = set(instructions)
        assert file.readline() == '\n'
        states, transitions = set(), {}
        for line in file:
            node_name, rest = line.strip().split(" = ")
            states.add(node_name)
            transitions[(node_name, "L")], transitions[(node_name, "R")] = rest.strip('()').split(', ')

    instructions_length = len(instructions)
    print(f"Inputs: Instruction word length: {instructions_length}, Number of states: {len(states)}, Number of Transitions: {len(transitions)}")

    initial_states = sorted(state for state in states if state.endswith('A'))
    final_states = {state for state in states if state.endswith('Z')}
    DFA_dict = {initial_state: DeterministicFiniteAutomaton(states, alphabet, transitions, initial_state, final_states).remove_unreachable_states() for initial_state in initial_states}

    residues, moduli = [], []
    for initial_state, DFA in DFA_dict.items():
        end_Z_state = next(iter(DFA.final_states))
        print(
            f"\nIn the component of the mapping containing initial state {initial_state} and final states: {DFA.final_states}, "
            f"There are {len(DFA.reachable_states)} reachable states and {len(DFA.distinguishable_states_partition)} distinguishable states."
        )
        DFA = DFA.minimize()
        steps = count_DFA_steps_to_final_state(DFA, instructions)
        quotient, remainder = steps // instructions_length, steps % instructions_length
        print(f"Following the instructions, the (minimum) number of steps from {initial_state} to {end_Z_state} is {steps} = {quotient} * {instructions_length} + {remainder}.")
        residues.append(steps)

        final_state = next(iter(DFA.final_states))
        loop_steps = count_DFA_steps_to_final_state(DFA, instructions, initial_state=final_state, allow_empty_str=False)
        quotient, remainder = loop_steps // instructions_length, loop_steps % instructions_length
        print(f"Following the instructions, the (minimum, positive) number of steps to loop from {end_Z_state} to {end_Z_state} is {loop_steps} = {quotient} * {instructions_length} + {remainder}.")
        moduli.append(loop_steps)

    # TODO: Add chinese remainder theorem solver which generalizes to non-coprime moduli
    part2_summary =f"""
The map is split into {len(initial_states)} disjoint subgraphs, each requiring a fixed multiple of the instruction set to transition from the initial state ending with 'A'
to the corresponding final state ending with 'Z', and the same multiple of the instruction set steps to loop back to the final state a second time.
It follows that the (minimum) number of simultaneous steps through each of the subgraphs from the vector of initial states to the vector of final states
is the least common multiple of the component journey loop lengths, which is {lcm(*moduli)} = {' * '.join(map(str, [modulus // gcd(*moduli) for modulus in sorted(moduli)] + [gcd(*moduli)]))}.
This is implicitly an application of the Chinese remainder theorem. Note that the highest common factor between the component loop lengths is the length of the instruction set.
"""
    print(part2_summary)

    return 0


def count_DFA_steps_to_final_state(DFA, instructions: str, initial_state=None, allow_empty_str: bool=True):
    """Will run forever if the final state is not reachable from initial state by following the instructions"""
    assert instructions or allow_empty_str
    counter = 0
    current_state = initial_state or DFA.initial_state
    # Take at least one step through the (nonempty) instructions if the empty string is not allowed
    reached_final = current_state in DFA.final_states and allow_empty_str
    while not reached_final:
        for char in instructions:
            current_state = DFA.transitions[(current_state, char)]
            reached_final = current_state in DFA.final_states
            counter += 1
            if reached_final:
                return counter
    # Returns 0 if the initial state is already a final state
    return counter


@dataclass(frozen=True, slots=True)
class DeterministicFiniteAutomaton:
    states: set[str]
    alphabet: set[str]
    transitions: dict[tuple[str, str], str]
    initial_state: str
    final_states: set[str]


    @property
    def reachable_states(self) -> set[str]:
        """Return the set of states reachable from the initial state"""
        reachable_states = {self.initial_state}
        new_states = {self.initial_state}
        while new_states:
            new_states = {self.transitions[(q, c)] for q in new_states for c in self.alphabet} - reachable_states
            reachable_states |= new_states
        return reachable_states


    def remove_unreachable_states(self):
        """Return an equivalent DFA with any states not reachable from the initial state removed"""
        reachable_states = self.reachable_states
        return replace(
            self,
            states=reachable_states,
            transitions={(q_curr, move): q_next for (q_curr, move), q_next in self.transitions.items() if q_curr in reachable_states},
            final_states=self.final_states & reachable_states
        )


    def split_block(self, block_to_split: set[str], distinguishing_set: set[str], symbol: str) -> tuple[set[str], set[str]]:
        """Split a block (a set of states) into two subsets based on whether each
        element maps by the given input symbol into a distinguishing set of states or not
        """
        preimage_of_distinguishing_set_in_block = {state for state in block_to_split if self.transitions[(state, symbol)] in distinguishing_set}
        return preimage_of_distinguishing_set_in_block, block_to_split - preimage_of_distinguishing_set_in_block


    @property
    def distinguishable_states_partition(self) -> list[set[str]]:
        """Implements Hopcroft's algorithm
        Return a partition of the states into equivalence classes where states in the same class cannot be distinguished from one another for any input string
        A pair of states is distinguishable if there is a word in the language which maps one to a final state and the other to a non-final state
        """
        partition = [self.final_states, self.states - self.final_states]
        distinguishing_sets_to_check = [min(partition, key=len)]
        while distinguishing_sets_to_check:
            distinguishing_set = distinguishing_sets_to_check.pop()
            for symbol in self.alphabet:
                for block in partition:
                    # Split the block by whether each state transitions by the symbol into distinguishing set or not
                    sub_block1, sub_block2 = self.split_block(block, distinguishing_set, symbol)
                    if sub_block1 and sub_block2:
                        # We have a proper refinement as both sub-blocks are non-empty
                        partition.remove(block)
                        partition.extend([sub_block1, sub_block2])
                        if block in distinguishing_sets_to_check:
                            # Shortcut condition
                            distinguishing_sets_to_check.remove(block)
                            distinguishing_sets_to_check.extend([sub_block1, sub_block2])
                        else:
                            # We only need to further refine on one of the sub-blocks, so choose the smaller one
                            distinguishing_sets_to_check.append(min(sub_block1, sub_block2, key=len))
        return partition


    def merge_nondistinguishable_states(self):
        """Return an equivalent DFA with nondistinguishable states merged into equivalence classes"""
        state_to_block_id_mapping = {state: index for index, block in enumerate(self.distinguishable_states_partition) for state in block}

        return DeterministicFiniteAutomaton(
            states=set(state_to_block_id_mapping.values()),
            alphabet=self.alphabet,
            transitions={(state_to_block_id_mapping.get(src), symbol): state_to_block_id_mapping.get(dest) for (src, symbol), dest in self.transitions.items()},
            initial_state=state_to_block_id_mapping.get(self.initial_state),
            final_states={state_to_block_id_mapping.get(state) for state in self.final_states}
        )


    def minimize(self):
        """Return the minimal DFA (by number of states) equivalent to `self`"""
        return self.remove_unreachable_states().merge_nondistinguishable_states()


if __name__ == "__main__":
    main()
