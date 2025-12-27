#!/usr/bin/env python3
"""
--- Day 18: Like a GIF For Your Yard ---
https://adventofcode.com/2015/day/18
Part 1: Simulating Conway's Game of Life (Cellular Automata)
Part 2: Modification with boundary condition: corners always on

References:
- https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
- https://en.wikipedia.org/wiki/Cellular_automaton
"""
import os
from collections.abc import Iterator, Callable

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    # Load input file
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        data = [line.strip() for line in file]

    part_1_answer = solve_part_1(data)
    print(f"Part 1: After 100 steps, there are {part_1_answer} lights on.")

    part_2_answer = solve_part_2(data)
    print(f"Part 2: With the four corner lights always in the on state, after 100 steps, there are {part_2_answer} lights on.")


def solve_part_1(data: list[str]) -> int:
    """Simulate Conway's Game of Life for 100 steps on a 100x100 grid from an initial state"""
    light_grid = CellularAutomata(initial_state=data, cell_new_state_rule=conways_rule_of_life)
    light_grid.evolve_n_generations(100)
    return light_grid.count('#')


def solve_part_2(data: list[str]) -> int:
    """"""
    # Ensure corners lights are switched on in initial state
    initial_state: list[str] = [
        "".join([
            '#' if (i in {0, len(data)-1} and j in {0, len(line)-1}) else c
            for j, c in enumerate(line)
        ])
        for i, line in enumerate(data)
    ]
    light_grid = CellularAutomata(initial_state, life_with_corner_cases)
    light_grid.evolve_n_generations(100)
    return light_grid.count('#')


class CellGrid:
    """Finite two dimensional grid of cells represented by a list of strings of equal length.
    The state of a cell is represented by a single character.
    """
    def __init__(self, state: list[str]):
        self._state: list[str] = state

    @property
    def state(self) -> list[str]:
        return self._state

    @property
    def height(self) -> int:
        return len(self.state)

    @property
    def width(self) -> int:
        return len(self.state[0]) if self.height > 0 else 0

    def get_cell(self, i: int, j: int) -> str:
        return self.state[i][j]

    def count(self, cell_state: str) -> int:
        """Count occurrences of a given cell state/character within the grid."""
        return sum(row.count(cell_state) for row in self.state)

    def adjacent_neighbourhood(self, i, j) -> Iterator[tuple[int, int]]:
        """Yield all positions of adjacent neighbours to (i,j), not including itself."""
        # Ensure we do not access out-of-bounds indexes when iterating over neighbours
        x_start, x_end = max(i-1, 0), min(i+2, self.height)
        y_start, y_end = max(j-1, 0), min(j+2, self.width)
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if (x,y) != (i,j):
                    yield (x,y)


class CellularAutomata(CellGrid):
    """A cellular automaton consists of
    1. Grid: A regular grid of cells, each in one of a finite number of states
    2. Neighourhood criteria: For each cell, a set of cells called its neighborhood is defined relative to the specified cell
    3. Initial state: An initial state (time t = 0) is selected by assigning a state for each cell
    4. New generation rule: A new generation is created (advancing t by 1),
       according to some fixed rule that determines the new state of each cell
       in terms of the current state of the cell and the states of the cells in its neighborhood.
    """
    def __init__(self, initial_state: list[str], cell_new_state_rule: Callable[[CellGrid, int, int], str]):
        """Define a cellular automaton from an initial state and cell state update rule.
        :param initial_state: An initial state (time t = 0) of a grid of cells, assigning a state for each cell
        :param cell_new_state_rule: Returns the new state of cell (i,j) given its current state and the states of its neighbors.
        """
        super().__init__(initial_state)
        self._cell_new_state_rule = cell_new_state_rule
        self._t: int = 0

    def grid_new_state(self) -> tuple[list[str], int]:
        """Return tuple of new state after applying an update rule to each cell, together with how many cells have changed state.

        `cell_new_state_rule` is some fixed rule that determines the new state of each cell
        in terms of the current state of the cell and the states of the cells in its neighborhood.
        """
        new_state: list[str] = []
        num_changes: int = 0
        # Apply the update rule to every cell simultaneously, storing the result in a new 2D array
        for i in range(self.height):
            new_row: str = ""
            for j in range(self.width):
                new_cell = self._cell_new_state_rule(self, i, j)
                new_row += new_cell
                num_changes += (new_cell != self.get_cell(i, j))
            new_state.append(new_row)

        return new_state, num_changes

    def evolve_n_generations(self, n: int) -> None:
        """Calculate the state of a cellular automaton after n new generations"""
        for i in range(n):
            new_state, num_changes = self.grid_new_state()
            if num_changes == 0:
                # A stable, homogeneous state has been reached, so we can return early without further calculation
                print(f"Reached equilibrium state after {i} iterations.")
                break
            self._state = new_state
        self._t += n


def conways_rule_of_life(cell_grid: CellGrid, i: int, j: int) -> str:
    """
    A `#` means "on", and a `.` means "off".
    A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.

    Each cell is in one of two possible states, live or dead.

    Every cell interacts with its eight neighbours,
    which are the cells that are horizontally, vertically, or diagonally adjacent.

    At each step in time, the following transitions occur:
    1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    2. Any live cell with two or three live neighbours lives on to the next generation.
    3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    """
    live_neighbours: int = sum(cell_grid.get_cell(x,y) == '#' for (x,y) in cell_grid.adjacent_neighbourhood(i,j))
    match cell_grid.get_cell(i,j):
        case '#':
            return '#' if live_neighbours in {2, 3} else '.'
        case '.':
            return '#' if live_neighbours == 3 else '.'


def life_with_corner_cases(cell_grid: CellGrid, i: int, j: int) -> str:
    """The four corner lights are stuck on and can't be turned off"""
    if i in {0, cell_grid.height-1} and j in {0, cell_grid.width-1}:
        return '#'
    else:
        return conways_rule_of_life(cell_grid, i, j)


if __name__ == "__main__":
    main()
