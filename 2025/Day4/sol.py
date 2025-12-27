#!/usr/bin/env python3
"""
--- Day 4: Printing Department ---
https://adventofcode.com/2025/day/4

A cellular automaton consists of
    1. Grid: A regular grid of cells, each in one of a finite number of states
    2. Neighourhood criteria: For each cell, a set of cells called its neighborhood is defined relative to the specified cell
    3. Initial state: An initial state (time t = 0) is selected by assigning a state for each cell
    4. New generation rule: A new generation is created (advancing t by 1),
       according to some fixed rule that determines the new state of each cell
       in terms of the current state of the cell and the states of the cells in its neighborhood.

References
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

    paper_roll_grid = CellularAutomata(initial_state=data, cell_new_state_rule=identify_accessible_paper_roll)

    paper_roll_grid.evolve_n_generations(1)
    print(f"Part 1: There are {paper_roll_grid.count('x')} rolls of paper that can initially be accessed/removed.")

    paper_roll_grid.evolve_n_generations(10_000)
    print(f"Part 2: The total number of rolls of paper that can be successively removed is {paper_roll_grid.count('x')}.")


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


def identify_accessible_paper_roll(cell_grid: CellGrid, i: int, j: int) -> str:
    """Return the outcome of removing a roll of paper (@) from a grid if present and accessible.
    A roll of paper is accessible/removable if there are fewer than 4 rolls of paper in the 8 adjacent positions.
    """
    cell: str = cell_grid.get_cell(i,j)
    match cell:
        case '@':
            adjacent_rolls: int = sum(cell_grid.get_cell(x,y) == '@' for (x,y) in cell_grid.adjacent_neighbourhood(i,j))
            # A roll of paper is accessible/removable if there are fewer than 4 rolls of paper in the 8 adjacent positions.
            return 'x' if adjacent_rolls < 4 else cell
        case _:
            return cell


if __name__ == "__main__":
    main()
