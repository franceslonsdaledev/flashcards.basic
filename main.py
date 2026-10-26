

from pathlib import Path
import cli
import engine
import storage

DATA_FILE= Path("card.json")

def run_quiz() -> None:
    cards = storage.load_cards()
    if not cards:
        cli.show_empty_deck_message()
        return

    deck = engine.pre_deck(cards)
    score = 0
    attempted = 0
    total_deck = len(deck)

    cli.show_welcome_message()

    for index, card in enumerate(deck):
        user_answer = cli.prompt_answer(card['q'])
        if user_answer.lower() == 'q':
            break
        attempted += 1
        correct = engine.check_answer(user_answer, card['a'])
        if correct:
            score += 1
            cli.show_correct_answer()
        else:
            cli.show_incorrect_answer(card['a'])

    cli.show_summary(score, attempted, total_deck)

if __name__ == "__main__":
    run_quiz()