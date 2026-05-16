#!/usr/bin/env python3
"""
--- Day 10: Balance Bots ---
https://adventofcode.com/2015/day/10
Simulate an automated microchip sorting factory

References
- Structural Pattern Matching
  - https://peps.python.org/pep-0636/
"""
import os
from typing import Literal
from dataclasses import dataclass, field
import math

# Types
OutputLocationType = Literal["output", "bot"]
OutputLocation = tuple[OutputLocationType, int]


DIRPATH = os.path.dirname(__file__)

def main():
    """Read the puzzle inputs, then calculate and print the puzzle answers"""
    with open(os.path.join(DIRPATH, "input.txt"), 'r') as file:
        instructions = file.read()

    factory = Factory(instructions)

    for bot_id, bot in factory.bots.items():
        if (17, 61) in bot.comparisons:
            print(f"Part 1: The number of the bot that is responsible for comparing value-61 microchips with value-17 microchips is {bot_id}.")

    print(f"Part 2: The product of the chip values in output bins with ids 0, 1, and 2 is {math.prod([factory.output_bins[i] for i in (0,1,2)])}.")


class Factory:
    """Represents the state of an automated microchip sorting factory given by bot and microchip locations"""
    def __init__(self, instructions: str) -> None:
        """Create an initial factory state from a list of input bin and bot instructions,
        then follow bot instructions to sort microchips from input bins to output bins
        """
        # Initialise instance attributes
        self.input_bins: dict[int, int] = {}
        self.bots: dict[int, Bot] = {}
        self.output_bins: dict[int, int] = {}

        # Configure initial factory state from a list of input bin and bot instructions
        for line in instructions.splitlines():
            match line.split():
                case ["value", value, "goes", "to", "bot", bot_id]:
                    self.input_bins[int(value)] = int(bot_id)
                case [
                    "bot", bot_id, "gives",
                    "low", "to", ("output" | "bot") as low_out_type, low_out_id, "and",
                    "high", "to", ("output" | "bot") as high_out_type, high_out_id
                ]:
                    self.bots[int(bot_id)] = Bot(
                        factory=self,
                        low_out=OutputLocation((low_out_type, int(low_out_id))),
                        high_out=OutputLocation((high_out_type, int(high_out_id)))
                    )

        # Follow bot instructions to sort microchips from input bins to output bins
        for val, bot_id in self.input_bins.items():
            self.bots[bot_id].add_chip(val)


@dataclass
class Bot:
    """Create a Bot in a factory for comparing pairs of microchip values.
    Each bot only proceeds when it has two microchips, and once it does,
    it gives each one to a different bot or puts it in a marked "output" bin.
    A bot's behaviour is determined by instructions for where to send its lower-value and higher-value chip after comparison.
    """
    factory: Factory
    low_out: OutputLocation
    high_out: OutputLocation
    hand: list[int] = field(init=False, default_factory=list)
    comparisons: list[tuple[int, int]] = field(init=False, default_factory=list)

    def add_chip(self, value: int) -> None:
        """Add a chip to this bot's hand.
        If the bot now has two microchips, it compares their values and gives each one to a different bot
        or puts it in a marked "output" bin, according to its behaviour instructions.
        Assumes available space in hand.
        """
        assert len(self.hand) < 2
        self.hand.append(value)

        if len(self.hand) == 2:
            low_val, high_val = sorted(self.hand)
            self.comparisons.append((low_val, high_val))
            self.send_chip(low_val, self.low_out)
            self.send_chip(high_val, self.high_out)

    def send_chip(self, value: int, location: OutputLocation) -> None:
        """Send a chip from the bot's hand to another location in the factory.
        Raises error if this chip is not in hand.
        """
        self.hand.remove(value)
        match location:
            case ("output", bin_id):
                self.factory.output_bins[bin_id] = value
            case ("bot", bot_id):
                self.factory.bots[bot_id].add_chip(value)


if __name__ == "__main__":
    main()
