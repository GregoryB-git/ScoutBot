from card import Card, load_deck
from player import Player
from get_all_sets import get_all_sets
from get_possible_sets import get_possible_sets
import random
import json
import itertools

class GameState:
    def __init__(self, players, deck):
        self.players = players
        self.deck = deck
        self.board = []
        self.current_player_index = 0
        self.round_count = 0
        self.round_over = False
        self.initialize_round()

    def initialize_round(self):
        # Remove one random card with active number 10 if there are two players
        if len(self.players) == 2:
            ten_cards = [card for card in self.deck if card.active == 10]
            if ten_cards:
                self.deck.remove(random.choice(ten_cards))

        # Shuffle the deck
        random.shuffle(self.deck)

        # Deal 11 cards to each player
        for player in self.players:
            player.hand = [self.deck.pop(0) for _ in range(11)]
        
        self.save_board()
        self.save_player_hands()

    def save_board(self):
        with open('board.json', 'w') as file:
            json.dump([{"active": card.active, "inactive": card.inactive} for card in self.board], file)

    def save_player_hands(self):
        for i, player in enumerate(self.players):
            with open(f'player_{i}.json', 'w') as file:
                json.dump([{"active": card.active, "inactive": card.inactive} for card in player.hand], file)

    def scout_card(self, player, position, board_card_position, flip=False):
        if player.scout_tickets <= 0:
            raise ValueError("Cannot scout card, no scout tickets left")
        card = self.board[board_card_position]
        self.board.pop(board_card_position)
        player.scout(card, position, flip)
        self.players[self.current_player_index].scout_bonus += 1
        self.save_board()
        self.save_player_hands()

    def show(self, player, card_indices):
        set_to_play = [player.hand[i] for i in card_indices]
        self.board = set_to_play
        for i in sorted(card_indices, reverse=True):
            player.hand.pop(i)
        player.beaten_cards += len(set_to_play)
        self.save_board()
        self.save_player_hands()

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def is_round_over(self):
        current_player = self.players[self.current_player_index]
        return len(self.get_possible_actions(current_player)) == 0

    def is_game_over(self):
        return self.round_count >= 3

    def get_possible_actions(self, player):
        possible_actions = []
        if self.can_play_set(player):
            possible_actions.append('show')
        if self.can_scout_card(player):
            possible_actions.append('scout')
        return possible_actions

    def can_play_set(self, player):
        possible_sets = self.get_possible_sets(player, self.board)
        return len(possible_sets) > 0

    def can_scout_card(self, player):
        return player.scout_tickets > 0 and len(self.board) > 0


# Example usage:
# players = [Player("Alice"), Player("Bob")]
# game_state = GameState(players, load_deck('/home/gregory/Documents/Playground/ScoutBot/original_deck.json'))
# print(game_state.get_possible_actions(players[0]))
