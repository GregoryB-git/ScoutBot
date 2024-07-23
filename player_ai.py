import random
from card import Card
from AI_model_0 import ai_model_0_action
from player import Player

class AIPlayer(Player):
    def take_turn(self, game_state):
        possible_actions = game_state.get_possible_actions(self)
        action, params = ai_model_0_action(possible_actions, game_state, self)
        if action == "show":
            game_state.show(self, params)
        elif action == "scout":
            game_state.scout_card(self, *params)

        print(f"\n{self.name}'s turn")
        print(f"Action taken: {action}")
        print(f"Parameters: {params}")
