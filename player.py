import random
from card import Card
from AI_model_0 import ai_model_0_action

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.total_score = 0
        self.scout_bonus = 0
        self.beaten_cards = 0
        self.scout_tickets = 3

    def scout(self, card, position=None, flip=False):
        if self.scout_tickets <= 0:
            raise ValueError("No scout tickets left")
        if flip:
            card.flip()
        if position is None:
            self.hand.append(card)
        else:
            self.hand.insert(position, card)
        self.scout_tickets -= 1

    def __repr__(self):
        return (f"Player({self.name}, Hand: {self.hand}, Total Score: {self.total_score}, "
                f"Scout Bonus: {self.scout_bonus}, Beaten Cards: {self.beaten_cards}, "
                f"Scout Tickets: {self.scout_tickets})")

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
                        game_state.show(self, [self.hand.index(card) for card in possible_sets[choice]])
                        break
                    else:
                        print("Invalid set number. Try again.")
                except ValueError:
                    print("Invalid input. Try again.")
            elif action == "scout" and "scout" in possible_actions:
                try:
                    board_card_position = int(input("Enter board card position to scout (first or last card): "))
                    if board_card_position == 0 or board_card_position == len(game_state.board) - 1:
                        position = int(input("Enter position in hand to place the scouted card (between two cards): "))
                        flip = input("Flip card? (yes or no): ").strip().lower() == "yes"
                        if position >= 0 and position <= len(self.hand):
                            game_state.scout_card(self, position, board_card_position, flip)
                            break
                        else:
                            print("Invalid hand position. Try again.")
                    else:
                        print("You can only scout the first or last card of the set. Try again.")
                except ValueError:
                    print("Invalid input. Try again.")
            else:
                print("Invalid action. Try again.")

class AIPlayer(Player):
    def take_turn(self, game_state):
        possible_actions = game_state.get_possible_actions(self)
        action, params = ai_model_0_action(possible_actions, game_state, self)
        if action == "show":
            game_state.show(self, [self.hand.index(card) for card in params])
        elif action == "scout":
            game_state.scout_card(self, *params)

        print(f"\n{self.name}'s turn")
        print(f"Action taken: {action}")
        print(f"Parameters: {params}")

# Example usage:
# players = [HumanPlayer("Alice"), AIPlayer("AI_1")]
# game_state = GameState(players, load_deck('/home/gregory/Documents/Playground/ScoutBot/original_deck.json'))
