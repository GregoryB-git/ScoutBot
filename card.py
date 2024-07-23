import json

class Card:
    def __init__(self, active, inactive):
        self.active = active
        self.inactive = inactive

    def flip(self):
        self.active, self.inactive = self.inactive, self.active

    def __repr__(self):
        return f"({self.active}/{self.inactive})"

def load_deck(filename):
    with open(filename, 'r') as file:
        deck_data = json.load(file)
    return [Card(card['active'], card['inactive']) for card in deck_data]
