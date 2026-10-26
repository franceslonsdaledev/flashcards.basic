from pathlib import Path
import streamlit as st
import engine
import storage

DATA_FILE = Path("card.json")

st.set_page_config(page_title="Index Deck", page_icon="🗂️", layout="centered")

# Custom CSS for physical speaker card + horizontal deck rows
st.markdown(
    """
<style>
    /* Physical study card */
    .deck-card {
        background-color: #1e1e24;
        border-radius: 14px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.35);
        border-top: 6px solid #4a90e2;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .deck-card.correct {
        background-color: #12281e;
        border-top: 6px solid #2ecc71;
    }
    .deck-card.incorrect {
        background-color: #2b171a;
        border-top: 6px solid #e74c3c;
    }
    .card-meta {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #888;
        margin-bottom: 15px;
    }
    .card-question {
        font-size: 1.35rem;
        font-weight: 600;
        color: #f1f2f6;
        line-height: 1.5;
        margin-bottom: 25px;
    }
    .card-feedback {
        font-size: 1.05rem;
        font-weight: 500;
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px dashed rgba(255,255,255,0.15);
    }

    /* Horizontal Deck Summary Cards */
    .deck-row {
        background-color: #1e1e24;
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 5px solid #4a90e2;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .deck-row-q {
        font-size: 1.05rem;
        color: #f1f2f6;
        font-weight: 500;
        flex: 3;
        padding-right: 20px;
    }
    .deck-row-a {
        font-size: 0.95rem;
        color: #2ecc71;
        font-weight: 600;
        background-color: rgba(46, 204, 113, 0.12);
        padding: 6px 14px;
        border-radius: 8px;
        border: 1px solid rgba(46, 204, 113, 0.3);
        text-align: right;
        flex: 1.5;
        word-break: break-word;
    }
    .deck-row-box {
        color: #888;
        font-size: 0.8rem;
        margin-right: 15px;
        font-family: monospace;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 1. State Initialization
if "cards" not in st.session_state:
  st.session_state.cards = storage.load_cards(DATA_FILE)
if "deck" not in st.session_state:
  st.session_state.deck = engine.pre_deck(st.session_state.cards)
if "index" not in st.session_state:
  st.session_state.index = 0
if "score" not in st.session_state:
  st.session_state.score = 0
if "submitted" not in st.session_state:
  st.session_state.submitted = False
if "is_correct" not in st.session_state:
  st.session_state.is_correct = False
if "view" not in st.session_state:
  st.session_state.view = "quiz"  # 'quiz', 'add', or 'deck'

# 2. Top Controls (All 3 buttons wired up)
col1, col2, col3 = st.columns(3)
with col1:
  if st.button("🗂️ Study Deck", use_container_width=True):
    st.session_state.view = "quiz"
    st.rerun()
with col2:
  if st.button("➕ Add Card", use_container_width=True):
    st.session_state.view = "add"
    st.rerun()
with col3:
  if st.button("📊 View Deck", use_container_width=True):
    st.session_state.view = "deck"
    st.rerun()

st.write("")

# 3. View: Add a New Card
if st.session_state.view == "add":
  st.markdown("### ➕ Create a Flashcard")
  with st.form("add_card_form", clear_on_submit=True):
    new_q = st.text_input("Question")
    new_a = st.text_input("Answer")
    add_btn = st.form_submit_button("Save to Deck")

    if add_btn:
      if new_q and new_a:
        card = engine.create_card(new_q, new_a)
        st.session_state.cards.append(card)
        storage.save_cards(DATA_FILE, st.session_state.cards)
        st.session_state.deck = engine.pre_deck(st.session_state.cards)
        st.success("Card added! Swapped into the deck.")
      else:
        st.error("Both fields are required.")

# 4. View: Scrollable Horizontal Deck List
elif st.session_state.view == "deck":
  st.markdown(f"### 📊 Full Deck ({len(st.session_state.cards)} Cards)")

  if not st.session_state.cards:
    st.info("Your deck is empty! Click '➕ Add Card' above to add cards.")
  else:
    for idx, card in enumerate(st.session_state.cards, 1):
      box_lvl = card.get("box", 1)
      row_html = f"""
            <div class="deck-row">
                <div class="deck-row-box">#{idx} • B{box_lvl}</div>
                <div class="deck-row-q">{card['q']}</div>
                <div class="deck-row-a">{card['a']}</div>
            </div>
            """
      st.markdown(row_html, unsafe_allow_html=True)

# 5. View: Physical Speaker Card Quiz
else:
  if not st.session_state.deck:
    st.info("Your deck is empty! Click '➕ Add Card' above to get started.")
  elif st.session_state.index < len(st.session_state.deck):
    card = st.session_state.deck[st.session_state.index]

    status_class = ""
    if st.session_state.submitted:
      status_class = "correct" if st.session_state.is_correct else "incorrect"

    box_num = card.get("box", 1)
    deck_progress = (
        f"Card {st.session_state.index + 1} of {len(st.session_state.deck)}  • "
        f" Mastery Box {box_num}"
    )

    card_html = f"""
    <div class="deck-card {status_class}">
        <div class="card-meta">{deck_progress}</div>
        <div class="card-question">{card['q']}</div>
    """

    if st.session_state.submitted:
      if st.session_state.is_correct:
        feedback = "<span style='color: #2ecc71;'>✔ Correct! Well done.</span>"
      else:
        feedback = f"<span style='color: #e74c3c;'>✘ Incorrect.</span> Answer was: <b>{card['a']}</b>"
      card_html += f'<div class="card-feedback">{feedback}</div>'

    card_html += "</div>"
    st.markdown(card_html, unsafe_allow_html=True)

    if not st.session_state.submitted:
      with st.form("card_input_form", clear_on_submit=False):
        user_input = st.text_input("Your Answer:", key="user_answer_field")
        submit_btn = st.form_submit_button("Submit Answer", type="primary")

        if submit_btn and user_input:
          is_correct = engine.check_answer(user_input, card["a"])
          engine.update_card_stats(card, is_correct)
          storage.save_cards(DATA_FILE, st.session_state.cards)

          st.session_state.is_correct = is_correct
          if is_correct:
            st.session_state.score += 1
          st.session_state.submitted = True
          st.rerun()
    else:
      if st.button("Next Card ➔", type="primary", use_container_width=True):
        st.session_state.index += 1
        st.session_state.submitted = False
        st.rerun()

  else:
    st.markdown("""
        <div class="deck-card correct">
            <div class="card-meta">Deck Complete</div>
            <div class="card-question">You reached the end of the stack! 🎉</div>
        </div>
        """, unsafe_allow_html=True)

    pct = round(
        (st.session_state.score / len(st.session_state.deck)) * 100, 1
    )
    st.metric(
        "Final Accuracy",
        f"{st.session_state.score}/{len(st.session_state.deck)}",
        f"{pct}%",
    )

    if st.button("↺ Shuffle & Restart Deck", use_container_width=True):
      st.session_state.deck = engine.pre_deck(st.session_state.cards)
      st.session_state.index = 0
      st.session_state.score = 0
      st.session_state.submitted = False
      st.rerun()