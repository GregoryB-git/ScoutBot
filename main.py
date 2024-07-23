import random
from card import load_deck
from player import Player, HumanPlayer, AIPlayer
from game_state import GameState

def setup_game():
    deck = load_deck('/home/gregory/Documents/Playground/ScoutBot/original_deck.json')
    
    print("Choose game mode:")
    print("1. Automatized testing")
    print("2. Manual testing")
    mode = input("Enter 1 or 2: ")

    if mode == "1":
        # Automatized testing setup
        players = [AIPlayer("AI_1"), AIPlayer("AI_2")]
    elif mode == "2":
        # Manual testing setup
        num_human = int(input("Enter number of human players: "))
        num_ai = int(input("Enter number of AI players: "))
        
        players = []
        for i in range(num_human):
            name = input(f"Enter name for human player {i+1}: ")
            players.append(HumanPlayer(name))
        
        for i in range(num_ai):
            name = f"AI_{i+1}"
            players.append(AIPlayer(name))
    else:
        print("Invalid mode selected. Exiting...")
        return None, None

    return players, deck

def main():
    players, deck = setup_game()
    if not players:
        return

    game_state = GameState(players, deck)

    while not game_state.is_game_over():
        current_player = game_state.players[game_state.current_player_index]

        if isinstance(current_player, HumanPlayer):
            current_player.take_turn(game_state)
        else:
            current_player.take_turn(game_state)

        if len(game_state.players) == 2 and isinstance(current_player, HumanPlayer):
            while "show" not in game_state.get_possible_actions(current_player):
                current_player.take_turn(game_state)

        if game_state.is_round_over():
            print("Round over!")
            print("Round results:")
            for player in players:
                print(player)
            game_state.round_count += 1
            if game_state.is_game_over():
                break
            game_state.initialize_round()
        else:
            game_state.next_player()

    print("Game over!")
    print("Final results:")
    for player in players:
        print(player)

if __name__ == "__main__":
    main()
