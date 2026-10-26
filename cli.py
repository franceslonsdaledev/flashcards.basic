# This code handles the terminal prompts and print formatting

def show_main_menu():
    print("Welcome to the Flashcard Quiz!")
    print("1. Start Quiz")
    print("2. Add Card")
    print("3. View Deck Summary")
    print("4. Exit")
    return input("Choose and option (1-4): ").strip()

def show_welcome_message():
    print("\n--- FLASHCARDS (Type your answer or 'q' to quit.) ---\n")

def prompt_answer(question):
    return input(f"Q: {question}\nA: ").strip()

def show_correct_answer() -> None:
    print("Correct!\n")

def show_incorrect_answer(correct_answer) -> None:
    print(f"Incorrect! The correct answer is: {correct_answer}\n")

def show_summary (score: int, attempted: int, total_deck:int) -> None:
    print(f"Session ended. Score: {score}/{attempted} out of {total_deck} cards attempted.")

def prompt_add_card() -> tuple[str, str]:
    print("\n--- ADD A NEW CARD ---\n")
    q = input("Enter the question: ").strip()
    a = input("Enter the answer: ").strip()
    return q, a

def show_deck_list(cards: list[dict]) -> None:
    print(f"\n--- DECK SUMMARY ({len(cards)} cards) ---\n")
    if not cards:
        print("No cards available.")
        return
    for index, card in enumerate(cards, start=1):
        box = card.get('box', 1)
        print(f"{index}. Q: {card['q']} | A: {card['a']} | Box: {box}")
    print("\n")

def show_message(msg:str) -> None:
    print(msg)

def show_empty_deck_message() -> None:
    print("No cards available. Please add some cards to the deck.")