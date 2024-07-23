from card import Card, load_deck
from player import Player
import random
import json

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

    def get_all_sets(self, hand):
        all_sets = []

        # Single card sets
        for card in hand:
            all_sets.append([card])

        # Adjacent cards with the same active number
        for i in range(len(hand)):
            for j in range(i + 1, len(hand) + 1):
                subset = hand[i:j]
                if all(card.active == subset[0].active for card in subset):
                    all_sets.append(subset)
                else:
                    break

        # Adjacent cards with sequential active numbers
        for i in range(len(hand) - 1):
            for j in range(i + 1, len(hand) + 1):
                subset = hand[i:j]
                if all(subset[k].active == subset[k - 1].active + 1 for k in range(1, len(subset))):
                    all_sets.append(subset)

        return all_sets

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

# Example usage:
# players = [Player("Alice"), Player("Bob")]
# game_state = GameState(players, load_deck('/home/gregory/Documents/Playground/ScoutBot/original_deck.json'))
# print(game_state.get_possible_actions(players[0]))
