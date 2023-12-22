#!/usr/bin/env python3
"""
--- Day 11: Seating System ---
https://adventofcode.com/2020/day/11
Part 1: Simulating Conway's Game of Life (Cellular Automata)
        References:
        - https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
        - https://en.wikipedia.org/wiki/Von_Neumann_neighborhood
        - https://en.wikipedia.org/wiki/Moore_neighborhood
Part 2: Variation on Game of Life simulation mixed with attacking chess queens
"""


def main():
    # Create SeatMap instances based on input data from file with different rules for updating state
    # SeatMap state is stored as a list of strings
    update_rules = ["adjacency", "visibility"]
    seat_maps = {rule: SeatMap.load_initial_state("input.txt", rule) for rule in update_rules}
    rounds_to_stable = {rule: 0 for rule in update_rules}
    equilibrium_occupancy = {}

    # For each update rule, find the equilibrium state and final seat occupancy
    for rule, seat_map in seat_maps.items():
        # Update SeatMap instance by a single round from initial state according to the update rule
        changes = seat_map.update_state()

        # Update the state of the SeatMap one round at a time until we stabilize/reach an equilibrium
        # To avoid infinite loops, it would be necessary to record a list of visited states
        while changes > 0:
            changes = seat_map.update_state()
            rounds_to_stable[rule] += 1

        # Calculate the number of occupied seats in the final equilibrium state
        equilibrium_occupancy[rule] = seat_map.occupied()

    for i, (rule, final_occupancy) in enumerate(equilibrium_occupancy.items(), 1):
        print(f"Part {i}:\n"
        f"With {rule} update rule, equilibrium reached after {rounds_to_stable[rule]} rounds.\n"
        f"Once stabilized, {final_occupancy} seats were occupied.")

    return 0


class SeatMap:
    """SeatMap state is stored as a list of strings"""
    def __init__(self, data, update_method="adjacency"):
        self._state = data
        self.update_method = update_method
        return


    @property
    def state(self):
        return self._state


    @property
    def height(self):
        return len(self.state)


    @property
    def width(self):
        return len(self.state[0]) if self.height > 0 else 0


    @classmethod
    def load_initial_state(cls, filename, update_method="adjacency"):
        """Read seat layout initial state from file"""
        # Read the input data into memory as a list of (immutable) strings
        with open(filename, 'r') as file:
            data = [line.strip() for line in file]
        # Create a SeatMap instance based on the input data
        return cls(data, update_method)


    def get_cell(self, i, j):
        return self.state[i][j]


    def set_state(self, data):
        # Check that the input data matches the shape of the state grid
        assert len(data) == self.height
        assert (len(data[0]) if self.height > 0 else 0) == self.width
        self._state = data
        return


    def occupied(self):
        """Return the number of occupied seats (#) in the current grid state"""
        return sum(sum(cell == '#' for cell in row) for row in self.state)


    def update_state(self, inplace=True):
        """Update the state of the seat map by a single round, returning number of changes"""
        # Initialize variable to count the number of changes made to the state of cells in the grid
        changes = 0

        # Apply the update rule to every cell simultaneously, storing the result in a new 2D array
        new_state = []
        for i in range(self.height):
            new_row = []
            for j in range(self.width):
                cell = self.get_cell(i, j)
                if self.update_method == "adjacency":
                    neighbours = self.get_adjacent_neighbours(i, j)
                elif self.update_method == "visibility":
                    neighbours = self.get_visible_neighbours(i, j)
                new_cell = self.update_rule(cell, neighbours)

                # Record if the state of cell (i,j) will change during this round
                changes += (new_cell != cell)
                new_row.append(new_cell)

            # Add the new row as a string to the variable storing the new state
            new_state.append("".join(new_row))

        if inplace:
            # Update the state variable of the SeatMap class instance in-place
            self.set_state(new_state)
            return changes
        else:
            # Return a new SeatMap instance
            return changes, SeatMap(new_state)


    def get_adjacent_neighbours(self, i, j):
        """
        Return the number of occupied seats (#) in a 3x3 grid about cell (i,j).
        Usually this grid will contain 9 cells, including cell (i,j) itself,
        except when (i,j) is at the edge of the grid and we only have 4 or 6 neighbouring cells.
        """
        neighbours = 0
        # Ensure we do not access out-of-bounds indexes when iterating over neighbours
        for y_offset in range(i - 1, i + 2):
            if not 0 <= y_offset < self.height:
                continue
            for x_offset in range(j - 1, j + 2):
                if 0 <= x_offset < self.width:
                    neighbours += (self.get_cell(y_offset, x_offset) == '#')
        return neighbours


    def get_visible_neighbours(self, i, j):
        """Count the number of occupied seats in the eight lines of sight from cell (i,j)"""
        neighbours = 0
        for direction in [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]:
            neighbours += (self.line_of_sight(i, j, direction) == '#')
        return neighbours


    def line_of_sight(self, i, j, direction):
        """Return the state of the first seat visible from (i,j) when looking towards `direction`.
        Follow line of sight (i,j) + k * `direction`, k > 0 until we find an empty (L) or
        occupied (#) seat to return or otherwise reach the edge of the grid and return '.'
        """
        # Unpack direction tuple
        x_shift, y_shift = direction
        # Initialize coordinates of cell offset from (i,j) to check for a seat
        x_offset, y_offset = i + x_shift, j + y_shift
        # Follow line of sight in direction until a seat is seen or we reach the edge of the grid
        while (0 <= x_offset < self.height) and (0 <= y_offset < self.width):
            view_cell = self.get_cell(x_offset, y_offset)
            if view_cell in {'L', '#'}:
                # Seat found
                return view_cell
            else:
                # No seat found. Follow line of sight further
                x_offset += x_shift
                y_offset += y_shift
        # No seat found within grid boundaries when viewing from (i,j) in towards `direction`
        return '.'


    @staticmethod
    def update_rule(cell, neighbours, tolerance=4):
        """
        Given an input cell and a count of its (adjacent or visible) neighbours,
        return the state of the input cell in the next round according to the update rule:
            If a seat is empty (L) and there are no occupied seats adjacent to/visible from it,
                the seat becomes occupied.
            If a seat is occupied (#) and the number of occupied neighbours exceeds the tolerance,
                the seat becomes empty.
            Otherwise, the seat's state does not change.
        """
        if cell == 'L' and neighbours == 0:
            # Empty seat with no occupied neighbours becomes occupied
            return '#'
        elif cell == '#' and neighbours > tolerance:
            # Occupied seat becomes empty due to overcrowding
            # The cell itself is counted as neighbour when using the adjacency rule
            return 'L'
        else:
            # Otherwise seat status doesn't change
            return cell


if __name__ == "__main__":
    main()
