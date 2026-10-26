# This code handles the terminal prompts and print formatting

def show_welcome_message():
    print("Welcome to the Flashcard Quiz!")
    print("Type your answer and press Enter. Type 'q' to quit.\n")

def prompt_answer(question):
    return input(f"Q: {question}\nA: ").strip()

def show_correct_answer() -> None:
    print("Correct!\n")

def show_incorrect_answer(correct_answer) -> None:
    print(f"Incorrect! The correct answer is: {correct_answer}\n")

def show_summary (score: int, attempted: int, total_deck:int) -> None:
    print(f"Session ended. Score: {score}/{attempted} out of {total_deck} cards attempted.")

def show_empty_deck_message() -> None:
    print("No cards available. Please add some cards to the deck.")