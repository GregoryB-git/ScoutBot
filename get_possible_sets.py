from card import Card, load_deck
from player import Player
from get_all_sets import get_all_sets
import random
import json
import itertools

def get_possible_sets(self, player, board):
    possible_sets = []
    hand = player.hand

    def can_beat(current_set, candidate_set):
        if not current_set:
            return True
        if len(candidate_set) > len(current_set):
            return True
        if len(candidate_set) == len(current_set):
            if len(set(card.active for card in candidate_set)) == 1 and \
                len(set(card.active for card in current_set)) > 1:
                return True
            if len(set(card.active for card in candidate_set)) == 1 and \
                len(set(card.active for card in current_set)) == 1:
                return candidate_set[0].active > current_set[0].active
            return candidate_set[-1].active > current_set[-1].active
        return False

    all_sets = self.get_all_sets(hand)

    for candidate_set in all_sets:
        if can_beat(board, candidate_set):
            possible_sets.append(candidate_set)

    # Sort possible sets by length (descending) and then by highest active number (descending)
    possible_sets.sort(key=lambda s: (-len(s), -max(card.active for card in s)))

    return possible_sets
