# This file is the python file that deals with cards.json file, this is an improvement from before as json files can't run code or vadliate/ update
# this means this python file 'protects' it by turning it into python objects so it cards can be added/ updated and if errors like a missing or empty file
# or broken syntax it catches this error safely and stops the file from crashing

import json
from pathlib import Path


def load_cards(file_path: Path) -> list[dict]:
    if not file_path.exists():
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Error: card.json is not a valid JSON file.")
        return []

def save_cards(file_path: Path, cards: list[dict]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=4)
