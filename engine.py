# This file is going to now run the quiz it'll deal with the logic of the quiz and deal with the user I/O. 

import random

def pre_deck(cards):  
    """Prepares the deck of cards for the quiz."""
    deck = list(cards)  # Create a copy of the cards list
    random.shuffle(deck)
    return deck

def check_answer(user_answer, correct_answer):
    """Check if the user's answer is correct."""
    return user_answer.strip().lower() == correct_answer.strip().lower()

def calculate_score(attempted, correct):
    """Calculate the score as a percentage."""
    if attempted == 0:
        return 0
    return (correct / attempted) * 100


def update_card_stats(card: dict, is_correct: bool) -> None:
    current_box = card.get('box', 1)
    if is_correct:
        card['box'] = min(current_box + 1, 5)
    else:
        card['box'] = 1

def create_card(question: str, answer: str) -> dict:
    q = question.strip()
    a = answer.strip()
    if not q or not a:
        raise ValueError("Question and answer cannot be blank.")
    return {"q": q, "a": a, "box": 1}
