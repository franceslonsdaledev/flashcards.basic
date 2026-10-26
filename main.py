import json
import random
from pathlib import Path

DATA_PATH = Path(__file__).parent / "card.json"

def load_cards():
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def run_quiz():
    cards = load_cards()
    if not cards:
        print("No cards available.")
        return

    random.shuffle(cards)
    score = 0

    print("\n--- FLASHCARDS (Type answer, or 'q' to quit) ---\n")
    attempted = 0
    for card in cards:
        print(f"Q: {card['q']}")
        answer = input("A: ").strip()
        if answer.lower() == 'q':
            break
        attempted += 1
        if answer == card['a']:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect! The correct answer is: {card['a']}\n")
    print(f"Session ended. Score: {score}/{attempted}")


if __name__ == "__main__":
    run_quiz()
    