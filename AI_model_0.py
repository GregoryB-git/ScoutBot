import random

def ai_model_0_action(possible_actions, game_state, player):
    if 'show' in possible_actions:
        possible_sets = game_state.get_possible_sets(player, game_state.board)
        if possible_sets:
            return 'show', possible_sets[0]  # Choose the first possible set
    elif 'scout' in possible_actions:
        board_card_position = random.choice([0, len(game_state.board) - 1])
        position = random.choice(range(len(player.hand) + 1))
        flip = random.choice([True, False])
        return 'scout', (position, board_card_position, flip)
    return None, None
