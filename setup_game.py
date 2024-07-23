import random
from card import load_deck
from player import Player
from player_human import HumanPlayer
from player_ai import AIPlayer
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