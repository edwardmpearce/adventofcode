#!/usr/bin/env python3
"""
--- Day 12: Rain Risk ---
https://adventofcode.com/2020/day/12
Part 1: Navigate robot in 2D Cartesian space with instructions for turning, moving forward
        and moving in cardinal directions (NESW)
Part 2: Navigate robot in 2D Cartesian space with instructions for moving via a (moveable) waypoint
"""

# Standard library imports
import math


def main():
    # Read navigation instructions from file to memory, returning as a list of instruction strings
    nav_actions = Ferry.load_navigation_instructions("input.txt")

    # Create two Ferry instances located at the origin facing East with default waypoint at (10,1)
    ferry1 = Ferry()
    ferry2 = Ferry()

    for instruction in nav_actions:
        ferry1.move(instruction)
        ferry2.move_waypoint(instruction)

    for i, (move_mode, ship) in enumerate(zip(["directly", "via waypoint"], [ferry1, ferry2]), 1):
        x, y = ship.position
        l1_dist = ship.Manhattan_distance
        travelled = ship.distance_travelled
        print(f"Part {i}: Results from following navigation instructions when moving {move_mode}:")
        print(f"\tFinal position of ship is ({x}, {y}), Manhattan distance from start is {l1_dist},")
        print(f"\tTotal distance travelled is {travelled}.")

    return 0


class Ferry:
    def __init__(self, position=(0,0), bearing=0, waypoint=(10, 1)):
        """Default Ferry instance starts at the origin (0,0) facing East.
        By default, waypoint starts 10 units east and 1 unit north relative to the ship."""
        self._pos_x, self._pos_y = position
        self._bearing = bearing
        # Waypoint coordinates are always relative to the position of the ship
        self._waypoint_x, self._waypoint_y = waypoint
        self._dist_travelled = 0
        return


    @property
    def position(self):
        return self._pos_x, self._pos_y


    @property
    def bearing(self):
        return self._bearing


    @property
    def waypoint(self):
        return self._waypoint_x, self._waypoint_y


    @property
    def Manhattan_distance(self):
        """Get the Manhattan distance between `self` and the origin (0,0)."""
        x, y = self.position
        return abs(x) + abs(y)


    @property
    def Euclidean_distance(self):
        """Get the Euclidean distance between `self` and the origin (0,0)."""
        x, y = self.position
        return math.sqrt(x*x + y*y)


    @property
    def distance_travelled(self):
        return self._dist_travelled


    def move(self, instruction):
        """Move the ship directly according to input instruction.
        Either move the ship directly in a cardinal direction (NESW),
        turn the ship (LR) a given number of degrees, or move forward (F) on current bearing."""
        # Parse instruction string into `action` and `arg` (distance or angle)
        action, arg = instruction[0], int(instruction[1:])

        if action in {'N', 'E', 'S', 'W'}:
            # Calculate new coordinates of the ship
            x, y = self.position
            x += ((action == 'E') - (action == 'W')) * arg
            y += ((action == 'N') - (action == 'S')) * arg

            # Update position of ship and distance travelled
            self._pos_x, self._pos_y = x, y
            self._dist_travelled += arg

        elif action in {'L', 'R'}:
            # Update bearing of the ship
            self._bearing += ((action == 'L') - (action == 'R')) * arg
            self._bearing %= 360

        elif action == 'F':
            (x, y), theta = self.position, self.bearing
            # Calculate new coordinates of the ship by moving along bearing
            # Risk of errors accumulating due to floating point arithmetic
            x += round(math.cos(theta * math.pi / 180) * arg)
            y += round(math.sin(theta * math.pi / 180) * arg)

            # Update position of ship and distance travelled
            self._pos_x, self._pos_y = x, y
            self._dist_travelled += arg

        return


    def move_waypoint(self, instruction):
        """Move the ship's waypoint (or move ship towards waypoint) according to input instruction.
        Either move the waypoint directly in a cardinal direction (NESW), adjust the angle the
        waypoint makes with the ship by rotating (LR) a given number of degrees,
        or move forward (F) to the waypoint a given number of times."""
        # Parse instruction string into `action` and `arg` (distance or angle)
        action, arg = instruction[0], int(instruction[1:])

        if action in {'N', 'E', 'S', 'W'}:
            # Calculate new waypoint coordinates
            x, y = self.waypoint
            x += ((action == 'E') - (action == 'W')) * arg
            y += ((action == 'N') - (action == 'S')) * arg

            # Update waypoint coordinates
            self._waypoint_x, self._waypoint_y = x, y

        elif action in {'L', 'R'}:
            # Convert angle of rotation from degrees to radians (in appropriate orientation)
            arg *= ((action == 'L') - (action == 'R')) * math.pi / 180

            # Rotate waypoint through an angle about the ship using linear transformation
            x, y = self.waypoint
            x, y = x * math.cos(arg) - y * math.sin(arg), x * math.sin(arg) + y * math.cos(arg)

            # Round new waypoint coordinates to nearest integer.
            # Risk of errors accumulating due to floating point arithmetic
            x, y = round(x), round(y)

            # Update waypoint coordinates
            self._waypoint_x, self._waypoint_y = x, y

        elif action == 'F':
            # Calculate new coordinates of the ship by moving forward to waypoint
            (x, y), (waypoint_x, waypoint_y) = self.position, self.waypoint
            x += waypoint_x * arg
            y += waypoint_y * arg

            # Update position of ship and distance travelled
            self._pos_x, self._pos_y = x, y
            self._dist_travelled += arg * math.sqrt(waypoint_x * waypoint_x + waypoint_y * waypoint_y)

        return


    @staticmethod
    def load_navigation_instructions(filename):
        """Read navigation instructions from file and return as a list"""
        # Read the input data into memory as a list of strings and return
        with open(filename, 'r') as file:
            instructions = [line.strip() for line in file]
        return instructions


if __name__ == "__main__":
    main()
