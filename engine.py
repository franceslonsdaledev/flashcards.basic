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


def update_card_box(cards, card_index, correct):
    """Update the card box based on whether the answer was correct."""
    if correct:
        cards[card_index]['box'] = min(cards[card_index].get('box', 1) + 1, 5)  # Move to next box, max 5
    else:
        cards[card_index]['box'] = 1  # Reset to box 1 if incorrect
