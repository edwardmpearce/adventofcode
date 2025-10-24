#!/usr/bin/env python3
"""
--- Day 14: Reindeer Olympics ---
https://adventofcode.com/2015/day/14
Themes: Integer division with remainder
"""
import os
from dataclasses import dataclass

DIRPATH = os.path.dirname(__file__)


def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    racers: dict[str, Reindeer] = read_input_data()
    race_duration: int = 2503

    final_standings: dict[str, int] = {name: reindeer.distance_travelled(race_duration) for name, reindeer in racers.items()}
    part_1_winner: str = max(racers, key=final_standings.get)

    print(f"Part 1: After {race_duration} seconds, the winning reindeer is {part_1_winner}, who travelled {final_standings[part_1_winner]} km")
    
    points: dict[str, int] = {name: 0 for name in racers}
    for i in range(1, race_duration + 1):
        standings = {name: reindeer.distance_travelled(i) for name, reindeer in racers.items()}
        lead_distance = max(standings.values())
        for name, distance in standings.items():
            if distance == lead_distance:
                points[name] += 1
    
    part_2_winner: str = max(racers, key=points.get)

    print(f"Part 2: After {race_duration} seconds, the winning reindeer is {part_2_winner}, with {points[part_2_winner]} points")


@dataclass
class Reindeer:
    """"""
    flight_speed: int
    flight_duration: int
    cooldown: int

    def distance_travelled(self, seconds: int) -> int:
        """Calculate the total distance travelled after the given number of seconds
        Reindeer travel in bursts at constant speed with cooldown periods in which they are stationary
        """
        num_full_cycles, remainder = divmod(seconds, self.flight_duration + self.cooldown)
        return self.flight_speed * (num_full_cycles * self.flight_duration + min(remainder, self.flight_duration))


def read_input_data() -> dict[str, Reindeer]:
    """Read an input file of the payoffs (in happiness units), positive or negative,
    that a person would receive by sitting next to a particular other person
    """
    racers: dict[str, Reindeer] = {}
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        for line in file:
            words = line.split()
            name, flight_speed, flight_duration, cooldown = words[0], int(words[3]), int(words[6]), int(words[-2])
            racers[name] = Reindeer(flight_speed, flight_duration, cooldown)

    return racers


if __name__ == "__main__":
    main()
