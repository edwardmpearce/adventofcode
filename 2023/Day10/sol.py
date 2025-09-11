#!/usr/bin/env python3
"""
--- Day 10: Pipe Maze ---
https://adventofcode.com/2023/day/10
Part 1: Conditional logic to navigate a closed loop in a 2D grid
Part 2: Updating variables based on current and previous state
"""


def main():
    with open("input.txt", 'r') as file:
        pipe_map = [line.strip() for line in file]

    main_loop_mask, num_steps, _ = traverse_main_loop(pipe_map)
    tiles_enclosed = count_tiles_enclosed_by_main_loop(pipe_map, main_loop_mask)

    print(f"Part 1: The number of steps from the starting position to its antipode in the main loop is {num_steps}")
    print(f"Part 2: The number of tiles enclosed by the main loop is {tiles_enclosed}")
    return 0


def traverse_main_loop(pipe_map: list[str]) -> tuple[list[list[bool]], int, tuple[int, int]]:
    """Given a pipe map input, return a 3-tuple of:
    1. a 2D boolean array of the same dimensions as the input pipe map indicating main loop pipe tiles,
    2. the number of steps between antipodal points in the main loop (this is half the length of the main loop),
    3. the starting position in the main loop, indicated by "S" in the input pipe map
    """
    num_rows, num_cols = len(pipe_map), len(pipe_map[0])
    main_loop_mask = [[False for _ in range(num_cols)] for _ in range(num_rows)]

    # Identify the starting position and its neighbours
    start_position = find_start_position(pipe_map)
    start_pipe_type = get_pipe_type(pipe_map, start_position)
    curr_node1, curr_node2 = get_neighbours(start_position, start_pipe_type)
    prev_node1, prev_node2 = start_position, start_position

    # Mark start position and its neighbours in the main loop mask
    for i, j in [start_position, curr_node1, curr_node2]:
        main_loop_mask[i][j] = True

    # The size of the pipe map is an upper bound on the length of the main loop
    for num_steps in range(2, num_rows * num_cols):
        # Increment step counter, step through the pipes in paths along the main loop in opposite directions
        curr_node1, prev_node1 = step_through_pipe(pipe_map, curr_node1, prev_node1), curr_node1
        curr_node2, prev_node2 = step_through_pipe(pipe_map, curr_node2, prev_node2), curr_node2
        # Add the two new positions to the main loop mask
        main_loop_mask[curr_node1[0]][curr_node1[1]] = True
        main_loop_mask[curr_node2[0]][curr_node2[1]] = True
        # The two paths meet at the point farthest from the starting position
        if curr_node1 == curr_node2:
            break
    return main_loop_mask, num_steps, start_position


def count_tiles_enclosed_by_main_loop(pipe_map: list[str], main_loop_mask: list[list[bool]]) -> int:
    tiles_enclosed, inside_main_loop, prev_east_bend = 0, False, ""
    for i, row in enumerate(main_loop_mask):
        for j, main_loop_tile in enumerate(row):
            if (not main_loop_tile) and inside_main_loop:
                # Count non-main-loop tile enclosed by main loop
                tiles_enclosed += 1
            elif main_loop_tile:
                pipe_type = get_pipe_type(pipe_map, (i, j))
                match prev_east_bend, pipe_type:
                    case ("", "L") | ("", "F"):
                        # East bend detected
                        prev_east_bend = pipe_type
                    case ("", "|") | ("L", "7") | ("F", "J"):
                        # Crosses the main loop
                        inside_main_loop = not inside_main_loop
                        prev_east_bend = ""
                    case ("L", "J") | ("F", "7"):
                        # West bend following east bend does not cross main loop
                        prev_east_bend = ""
    return tiles_enclosed


def find_start_position(pipe_map: list[str]) -> tuple[int, int]:
    for i, row in enumerate(pipe_map):
        if (j := row.find('S')) >= 0:
            return i, j
    # Did not find the starting symbol 'S'
    return -1, -1


def get_pipe_type(pipe_map: list[str], pos: tuple[int, int]) -> str:
    return symbol if (symbol := pipe_map[pos[0]][pos[1]]) != 'S' else determine_main_loop_pipe_type_from_neighbours(pipe_map, pos)


def determine_main_loop_pipe_type_from_neighbours(pipe_map: list[str], pos: tuple[int, int]) -> str:
    """Determine the pipe type of a position in the main loop by which two directions it has connecting neighbours"""
    connects_north = pos[0] > 0 and pipe_map[pos[0]-1][pos[1]] in "|7F"
    connects_west = pos[1] > 0 and pipe_map[pos[0]][pos[1]-1] in "-LF"
    connects_south = pos[0] + 1 < len(pipe_map) and pipe_map[pos[0]+1][pos[1]] in "|LJ"
    match (connects_north, connects_west, connects_south):
        case (True, True, False):
            return 'J'
        case (True, False, True):
            return '|'
        case (False, True, True):
            return '7'
        case (True, False, False):
            # North and East
            return 'L'
        case (False, True, False):
            # East and West
            return '-'
        case (False, False, True):
            # South and East
            return 'F'
        case _:
            # Unexpected combination
            return ""


def get_neighbours(position: tuple[int, int], pipe_type: str) -> list[tuple[int, int]]:
    i, j = position
    match pipe_type:
        case '|':
            return [(i-1, j), (i+1, j)]
        case '-':
            return [(i, j-1), (i, j+1)]
        case 'L':
            return [(i-1, j), (i, j+1)]
        case 'J':
            # North and West
            return [(i-1, j), (i, j-1)]
        case '7':
            # South and West
            return [(i+1, j), (i, j-1)]
        case 'F':
            return [(i, j+1), (i+1, j)]
        case _:
            # Unexpected combination
            return []


def step_through_pipe(pipe_map: list[str], curr_pos: tuple[int, int], prev_pos: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    # Lookup pipe type of current position to determine its neighbours
    curr_neighbours = get_neighbours(curr_pos, get_pipe_type(pipe_map, curr_pos))
    # Find the next position by eliminating the previous position from the list of neighbours
    curr_neighbours.remove(prev_pos)
    return curr_neighbours[0]


if __name__ == "__main__":
    main()
