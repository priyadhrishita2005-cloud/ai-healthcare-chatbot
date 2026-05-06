import streamlit as st
from deep_translator import GoogleTranslator
from fuzzywuzzy import process

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Rural Health Info Bot",
    page_icon="🏥",
    layout="centered"
)

# ---------------- TITLE ----------------

st.title("🏥 Rural Health Info Bot")

st.write("### Multilingual Healthcare Assistance Chatbot")

st.write(
    """
Ask healthcare-related questions about:
- diseases
- hospital departments
- appointments
- vaccinations
- emergency services
- first aid
- nutrition
- pregnancy care
"""
)

# ---------------- SIDEBAR ----------------

st.sidebar.title("About")

st.sidebar.write(
    """
This chatbot helps rural users get healthcare information
in multiple languages.

Features:
✅ Healthcare FAQs
✅ Multilingual Support
✅ Citations
✅ Smart Retrieval
✅ Admin Content Updates
"""
)

# ---------------- LOAD HEALTHCARE DATA ----------------

knowledge_base = {}

with open(
    "frontend/healthcare_data.txt",
    "r",
    encoding="utf-8"
) as file:

    lines = file.readlines()

    for i in range(0, len(lines), 2):

        if i + 1 < len(lines):

            question = lines[i].strip().lower()

            answer = lines[i + 1].strip()

            knowledge_base[question] = answer

# ---------------- ADMIN PANEL ----------------

st.sidebar.title("🛠 Admin Panel")

new_question = st.sidebar.text_input(
    "Add Healthcare Question"
)

new_answer = st.sidebar.text_area(
    "Add Healthcare Answer"
)

if st.sidebar.button("Update Knowledge Base"):

    if new_question and new_answer:

        with open(
            "frontend/healthcare_data.txt",
            "a",
            encoding="utf-8"
        ) as file:

            file.write("\n")
            file.write(new_question.lower() + "\n")
            file.write(new_answer + "\n")

        st.sidebar.success(
            "Healthcare information updated successfully."
        )

# ---------------- LANGUAGES ----------------

languages = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "Telugu": "te",
    "Marathi": "mr",
    "Malayalam": "ml",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Punjabi": "pa"
}

# ---------------- LANGUAGE SELECT ----------------

selected_language = st.selectbox(
    "🌐 Choose Language",
    list(languages.keys())
)

# ---------------- CHAT HISTORY ----------------

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

# ---------------- QUESTION INPUT ----------------

question = st.text_input(
    "💬 Enter your healthcare question"
)

# ---------------- ASK BUTTON ----------------

if st.button("Ask"):

    if question.strip() != "":

        q = question.lower().strip()

        # ---------------- SMART RETRIEVAL ----------------

        best_match = process.extractOne(
            q,
            knowledge_base.keys()
        )

        if best_match and best_match[1] > 60:

            matched_question = best_match[0]

            answer = knowledge_base[matched_question]

        else:

            answer = (
                "Sorry, relevant healthcare information is not available."
            )

        # ---------------- TRANSLATION ----------------

        target_language = languages[selected_language]

        if target_language != "en":

            answer = GoogleTranslator(
                source='auto',
                target=target_language
            ).translate(answer)

        # ---------------- DISPLAY ANSWER ----------------

        st.subheader("Answer")

        st.write(answer)

        # ---------------- CITATION ----------------

        st.subheader(" Citation")

        st.write(
            "Source: healthcare_data.txt"
        )

        # ---------------- SAVE CHAT HISTORY ----------------

        st.session_state.chat_history.append(
            ("Question", question)
        )

        st.session_state.chat_history.append(
            ("Answer", answer)
        )

    else:

        st.warning(
            "Please enter a healthcare question."
        )

# ---------------- CHAT HISTORY ----------------

st.subheader("🕘 Chat History")

for chat in st.session_state.chat_history:

    st.write(
        chat[0] + ": " + chat[1]
    )

# ---------------- FOOTER ----------------

st.markdown("---")

