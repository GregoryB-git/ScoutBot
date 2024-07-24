from card import Card, load_deck
from player import Player
import random
import json
import itertools

def get_all_sets(self, hand):
    all_sets = []

    # Single card sets
    for card in hand:
        all_sets.append([card])

    # Adjacent cards with the same active number
    for length in range(2, len(hand) + 1):
        for combo in itertools.combinations(hand, length):
            if all(card.active == combo[0].active for card in combo):
                all_sets.append(list(combo))

    # Adjacent cards with sequential active numbers
    for length in range(2, len(hand) + 1):
        for combo in itertools.combinations(hand, length):
            if all(combo[i].active == combo[i - 1].active + 1 for i in range(1, len(combo))):
                all_sets.append(list(combo))

    return all_sets
