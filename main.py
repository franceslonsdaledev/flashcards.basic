

from pathlib import Path
import cli
import engine
import storage

DATA_FILE= Path("card.json")

def run_quiz() -> None:
    cards = storage.load_cards(DATA_FILE)
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
        is_correct = engine.check_answer(user_answer, card['a'])    
        if is_correct:
            score += 1
            cli.show_correct_answer()
        else:
            cli.show_incorrect_answer(card['a'])

        # Update in-memory card metrics (both correct counter and box level)
        engine.update_card_stats(card, is_correct)

    # Save updated stats back to card.json on disk
    storage.save_cards(DATA_FILE, cards)
    cli.show_summary(score, attempted, total_deck)

def handle_add_card(cards: list[dict]) -> None:
    q, a = cli.prompt_add_card()
    try:
        new_card = engine.create_card (q,a)
        cards.append(new_card)
        storage.save_cards(DATA_FILE, cards)
        cli.show_message("Card added successfully!")
    except ValueError as err:
        cli.show_message(f"Error adding card: {err}")

def main() -> None:
    cards = storage.load_cards(DATA_FILE)

    while True:
        choice = cli.show_main_menu()
        if choice == '1':
            run_quiz()
        elif choice == '2':
            handle_add_card(cards)
        elif choice == '3':
            cli.show_deck_list(cards)
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()