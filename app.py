from pathlib import Path
import streamlit as st
import engine
import storage

DATA_FILE = Path("card.json")

st.set_page_config(page_title="Index Deck", page_icon="🗂️", layout="centered")

# Custom CSS: isolated strictly to flashcard components
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
        margin-bottom: 15px;
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
        padding: 16px 20px;
        border-left: 5px solid #4a90e2;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .deck-row-q {
        font-size: 1.05rem;
        color: #f1f2f6;
        font-weight: 500;
    }
    .deck-row-a {
        font-size: 0.92rem;
        color: #2ecc71;
        font-weight: 600;
        background-color: rgba(46, 204, 113, 0.12);
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-top: 6px;
    }
    .deck-row-box {
        color: #888;
        font-size: 0.75rem;
        font-family: monospace;
    }

    /* Target ONLY delete buttons (keys starting with del_) */
    button[key^="del_"] {
        height: 48px !important;
        width: 48px !important;
        min-width: 48px !important;
        padding: 0 !important;
        border-radius: 8px !important;
        background-color: #2b171a !important;
        border: 1px solid rgba(231, 76, 60, 0.4) !important;
        margin-top: 8px !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# 1. State Initialization
if "cards" not in st.session_state:
    st.session_state.cards = storage.load_cards(DATA_FILE)
if "deck" not in st.session_state:
    st.session_state.deck = []
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False
if "index" not in st.session_state:
    st.session_state.index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "is_correct" not in st.session_state:
    st.session_state.is_correct = False
if "view" not in st.session_state:
    st.session_state.view = "quiz"

# 2. Top Navigation Bar (Clean standard columns)
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

def start_quiz_session(card_limit: int):
    full_deck = engine.pre_deck(st.session_state.cards)
    st.session_state.deck = full_deck[:card_limit] if card_limit > 0 else full_deck
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.submitted = False
    st.session_state.quiz_active = True
    st.rerun()

# -------------------------------------------------------------
# 3. View: Add a New Card
# -------------------------------------------------------------
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
                st.success("Card added successfully!")
            else:
                st.error("Both fields are required.")

# -------------------------------------------------------------
# 4. View: Deck List with Mini Cube Bin
# -------------------------------------------------------------
elif st.session_state.view == "deck":
    st.markdown(f"### 📊 Full Deck ({len(st.session_state.cards)} Cards)")

    if not st.session_state.cards:
        st.info("Your deck is empty! Click '➕ Add Card' above to get started.")
    else:
        for idx, card in enumerate(st.session_state.cards):
            box_lvl = card.get("box", 1)
            
            c_info, c_bin = st.columns([9, 1])
            with c_info:
                st.markdown(
                    f"""
                    <div class="deck-row">
                        <div class="deck-row-box">#{idx + 1} • Box {box_lvl}</div>
                        <div class="deck-row-q">{card['q']}</div>
                        <div class="deck-row-a">A: {card['a']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with c_bin:
                st.write("")
                if st.button("🗑️", key=f"del_{idx}", help="Delete card"):
                    engine.delete_card(st.session_state.cards, idx)
                    storage.save_cards(DATA_FILE, st.session_state.cards)
                    st.rerun()

# -------------------------------------------------------------
# 5. View: Physical Speaker Card Quiz + Setup Screen
# -------------------------------------------------------------
else:
    total_avail = len(st.session_state.cards)

    if total_avail == 0:
        st.info("Your deck is empty! Click '➕ Add Card' above to get started.")

    # 5A. Session Setup: Choose how many questions to attempt
    elif not st.session_state.quiz_active:
        st.markdown("### 🎯 Choose Session Length")
        st.caption(f"Total cards available in deck: **{total_avail}**")

        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            if st.button("⚡ Quick 5", use_container_width=True, disabled=(total_avail < 5)):
                start_quiz_session(5)
        with btn_col2:
            if st.button("🔥 Standard 10", use_container_width=True, disabled=(total_avail < 10)):
                start_quiz_session(10)
        with btn_col3:
            if st.button(f"📚 Full Set ({total_avail})", use_container_width=True):
                start_quiz_session(total_avail)

        st.divider()
        st.markdown("**Or select a custom number of cards:**")
        custom_num = st.number_input(
            "Cards to study:",
            min_value=1,
            max_value=total_avail,
            value=min(5, total_avail),
            step=1,
        )
        if st.button("Start Custom Session", type="primary", use_container_width=True):
            start_quiz_session(custom_num)

    # 5B. Active Card Flashcard UI
    elif st.session_state.index < len(st.session_state.deck):
        card = st.session_state.deck[st.session_state.index]
        total_session = len(st.session_state.deck)

        status_class = ""
        if st.session_state.submitted:
            status_class = "correct" if st.session_state.is_correct else "incorrect"

        box_num = card.get("box", 1)
        deck_progress = (
            f"Card {st.session_state.index + 1} of {total_session} • Box {box_num}"
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

        # Single progress bar positioned directly under the physical card
        current_progress = (st.session_state.index) / total_session
        st.progress(current_progress, text=f"Progress: {st.session_state.index}/{total_session} completed")

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

    # 5C. Session Complete Screen
    else:
        st.markdown(
            """
            <div class="deck-card correct">
                <div class="card-meta">Round Complete</div>
                <div class="card-question">You finished all selected cards! 🎉</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        total_session = len(st.session_state.deck)
        st.progress(1.0, text=f"Progress: {total_session}/{total_session} completed")

        pct = round((st.session_state.score / total_session) * 100, 1)
        st.metric(
            "Session Accuracy",
            f"{st.session_state.score}/{total_session}",
            f"{pct}%",
        )

        col_again, col_menu = st.columns(2)
        with col_again:
            if st.button("↺ Practice Again", type="primary", use_container_width=True):
                start_quiz_session(total_session)
        with col_menu:
            if st.button("⚙ Change Session Size", use_container_width=True):
                st.session_state.quiz_active = False
                st.rerun()