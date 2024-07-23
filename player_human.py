import random
from card import Card
from player import Player
import game_state


class HumanPlayer(Player):
    def take_turn(self, game_state):
        while True:
            print(f"\n{self.name}'s turn")
            print(f"Your hand: {self.hand}")
            print(f"Current board: {game_state.board}")
            possible_actions = game_state.get_possible_actions(self)
            print(f"Possible actions: {possible_actions}")

            action = input("Enter action (show or scout): ").strip().lower()
            if action == "show" and "show" in possible_actions:
                possible_sets = game_state.get_possible_sets(self, game_state.board)
                for idx, possible_set in enumerate(possible_sets):
                    print(f"{idx}: {possible_set}")
                try:
                    choice = int(input("Choose a set to play (enter the number): "))
                    if choice >= 0 and choice < len(possible_sets):
                        game_state.show(self, possible_sets[choice])
                        break
                    else:
                        print("Invalid set number. Try again.")
                except ValueError:
                    print("Invalid input. Try again.")
            elif action == "scout" and "scout" in possible_actions:
                try:
                    board_card_position = int(input("Enter board card position to scout: "))
                    position = int(input("Enter position in hand to place the scouted card: "))
                    flip = input("Flip card? (yes or no): ").strip().lower() == "yes"
                    if board_card_position >= 0 and board_card_position < len(game_state.board) and \
                       position >= 0 and position <= len(self.hand):
                        game_state.scout_card(self, position, board_card_position, flip)
                        break
                    else:
                        print("Invalid card position. Try again.")
                except ValueError:
                    print("Invalid input. Try again.")
            else:
                print("Invalid action. Try again.")
