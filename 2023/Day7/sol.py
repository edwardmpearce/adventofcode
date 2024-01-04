#!/usr/bin/env python3
"""
--- Day 7: Camel Cards ---
https://adventofcode.com/2023/day/7
Part 1: Sorting with custom comparison operators
Part 2: Effect of wildcards on value counts

References
- https://docs.python.org/3/howto/sorting.html
- https://docs.python.org/3/library/collections.html
- https://stackoverflow.com/questions/2825452/correct-approach-to-validate-attributes-of-an-instance-of-class
"""
# Standard library imports
import operator
from collections import Counter


def main():
    with open("input.txt", 'r') as file:
        hands_and_bids = []
        for line in file:
            cards, bid = line.strip().split()
            hands_and_bids.append((CamelCardsHand(cards), int(bid)))

    results = {
        J_type: sum(bid * rank for rank, (hand, bid) in enumerate(sorted(hands_and_bids, key=lambda hand_bid: hand_bid[0].hand_strength(joker_mode=J_type == "Joker")), 1))
        for J_type in ("Jack", "Joker")
    }

    for i, (J_type, total_winnings) in enumerate(results.items(), 1):
        print(f"Part {i}: With 'J' = {J_type}, the total winnings for this set of hands are {total_winnings}.")

    return 0


class CamelCardsHand:
    # Hand types are ordered lexicographically by descending value counts
    HAND_SIZE = 5
    HAND_TYPE_NAMES = {
        (1, 1, 1, 1, 1): "High card",
        (2, 1, 1, 1): "One pair",
        (2, 2, 1): "Two pair",
        (3, 1, 1): "Three of a kind",
        (3, 2): "Full house",
        (4, 1): "Four of a kind",
        (5): "Five of a kind"
    }
    CARD_RANKING = {card: rank for rank, card in enumerate("j23456789TJQKA")}


    def __init__(self, cards: str):
        if len(cards) != CamelCardsHand.HAND_SIZE:
            raise ValueError(f"A hand must consist of exactly {CamelCardsHand.HAND_SIZE} cards")
        if not (set(cards).issubset(CamelCardsHand.CARD_RANKING) and 'j' not in cards):
            raise ValueError(f"Cards must be labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2")
        self._cards = cards


    cards = property(operator.attrgetter("_cards"))


    def hand_type(self, joker_mode=False) -> tuple[int]:
        card_counts = Counter(self.cards)
        if joker_mode and "J" in card_counts:
            # Separate the jokers from the rest of the hand
            joker_count = card_counts.pop("J")
            if joker_count == CamelCardsHand.HAND_SIZE:
                # Full hand of jokers
                return (CamelCardsHand.HAND_SIZE,)
            else:
                # Make a descending list of value counts for non-joker cards
                value_counts = list(sorted(card_counts.values(), reverse=True))
                # Add the jokers to (one of) the most common other card types
                value_counts[0] += joker_count
                return tuple(value_counts)
        else:
            # Hand types are based on descending value counts, ordered lexicographically
            return tuple(sorted(card_counts.values(), reverse=True))


    def card_strength(self, joker_mode=False) -> tuple[int]:
        return tuple(map(CamelCardsHand.CARD_RANKING.get, self.cards.replace("J", "j") if joker_mode else self.cards))


    def hand_strength(self, joker_mode=False) -> tuple[tuple[int], tuple[int]]:
        return (self.hand_type(joker_mode=joker_mode), self.card_strength(joker_mode=joker_mode))


if __name__ == "__main__":
    main()
