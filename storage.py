# This file is the python file that deals with cards.json file, this is an improvement from before as json files can't run code or vadliate/ update
# this means this python file 'protects' it by turning it into python objects so it cards can be added/ updated and if errors like a missing or empty file
# or broken syntax it catches this error safely and stops the file from crashing

import json
from pathlib import Path


def load_cards():
    """Load cards from the card.json file."""
    DATA_PATH = Path(__file__).parent / "card.json"
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Error: card.json is not a valid JSON file.")
            return []

def save_cards(cards):
    """Save cards to the card.json file."""
    DATA_PATH = Path(__file__).parent / "card.json"
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=4)
