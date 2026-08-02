"""
app.py - KTU AI Study Assistant

A simple AI study helper for KTU CS students, built for Epochs '26 Assignment 10.
Uses the Groq API (free tier) with a Llama model to power 3 study modes:
1. Concept Explainer  - explain any topic simply
2. Notes Summarizer   - paste messy notes, get a clean summary + key terms
3. Quiz Generator      - generate self-test questions for a topic
"""

import streamlit as st
from groq import Groq

st.set_page_config(page_title="KTU AI Study Assistant", page_icon="📚", layout="centered")

# ---- setting up the groq client ----
# API key comes from Streamlit secrets (when deployed) or a sidebar input (for quick local testing)
def get_client():
    api_key = st.secrets.get("GROQ_API_KEY", None) if hasattr(st, "secrets") else None
    if not api_key:
        api_key = st.session_state.get("manual_api_key")
    if not api_key:
        return None
    return Groq(api_key=api_key)


MODEL = "llama-3.3-70b-versatile"  # free tier model on groq


def ask_groq(client, system_prompt, user_prompt, temperature=0.4):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content


# ---- sidebar: api key + mode ----
st.sidebar.title("📚 KTU AI Study Assistant")

if "manual_api_key" not in st.session_state:
    st.session_state["manual_api_key"] = ""

has_secret_key = hasattr(st, "secrets") and st.secrets.get("GROQ_API_KEY", None)
if not has_secret_key:
    st.session_state["manual_api_key"] = st.sidebar.text_input(
        "Groq API Key (get one free at console.groq.com)",
        type="password",
        value=st.session_state["manual_api_key"],
    )

mode = st.sidebar.radio(
    "Choose a mode",
    ["Concept Explainer", "Notes Summarizer", "Quiz Generator"],
)

st.sidebar.markdown("---")
st.sidebar.caption("Built for Epochs '26 - Assignment 10, using the free Groq API.")

client = get_client()

st.title("📚 KTU AI Study Assistant")
st.write(
    "A little AI helper i built for studying — pick a mode on the left. "
    "Explain a topic i'm stuck on, summarize messy notes, or generate quiz "
    "questions to self test before exams."
)

if client is None:
    st.warning(
        "⚠️ No Groq API key found. Add one in the sidebar (or set `GROQ_API_KEY` "
        "in Streamlit secrets when deployed) to start using the assistant. "
        "Its free — sign up at [console.groq.com](https://console.groq.com)."
    )

# ============ MODE 1: CONCEPT EXPLAINER ============
if mode == "Concept Explainer":
    st.subheader("💡 Concept Explainer")
    st.write("Stuck on a topic from your syllabus? Paste it in and get a simple explanation.")

    topic = st.text_input("Topic / concept", placeholder="e.g. Normalization in DBMS, or Dijkstra's algorithm")
    level = st.select_slider(
        "Explain it like i'm...",
        options=["a total beginner", "a CS student who knows the basics", "prepping for exams (concise + exam-focused)"],
        value="a CS student who knows the basics",
    )

    if st.button("Explain it", type="primary"):
        if not topic.strip():
            st.error("Type a topic first!")
        elif client is None:
            st.error("Add your Groq API key in the sidebar first.")
        else:
            system_prompt = (
                "You are a friendly study tutor helping a Computer Science engineering "
                "student (KTU syllabus, India) understand concepts clearly. "
                "Explain the topic the student gives you, tailored to the level they specify. "
                "Use short paragraphs and bullet points where helpful. "
                "Include one small example if it helps understanding. "
                "Keep it focused and not overly long."
            )
            user_prompt = f"Explain this topic: {topic}\n\nExplain it like I'm: {level}"
            with st.spinner("Thinking..."):
                try:
                    answer = ask_groq(client, system_prompt, user_prompt)
                    st.markdown("### Explanation")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Something went wrong calling the API: {e}")

# ============ MODE 2: NOTES SUMMARIZER ============
elif mode == "Notes Summarizer":
    st.subheader("📝 Notes Summarizer")
    st.write("Paste your (probably messy lol) notes below and get a clean summary + key terms.")

    notes = st.text_area("Paste your notes here", height=250, placeholder="Paste lecture notes, textbook paragraphs, etc.")

    if st.button("Summarize", type="primary"):
        if not notes.strip():
            st.error("Paste some notes first!")
        elif client is None:
            st.error("Add your Groq API key in the sidebar first.")
        else:
            system_prompt = (
                "You are a study assistant that summarizes lecture notes for a Computer "
                "Science engineering student. Given messy or long notes, produce:\n"
                "1. A short summary (3-5 bullet points) of the main ideas\n"
                "2. A 'Key Terms' list with a one-line definition for each important term\n"
                "Keep it concise and exam-revision friendly. Do not add information that "
                "isn't supported by the notes given."
            )
            with st.spinner("Summarizing..."):
                try:
                    answer = ask_groq(client, system_prompt, notes)
                    st.markdown("### Summary")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Something went wrong calling the API: {e}")

# ============ MODE 3: QUIZ GENERATOR ============
elif mode == "Quiz Generator":
    st.subheader("🧠 Quiz Generator")
    st.write("Generate a few self-test questions on a topic before your exam.")

    quiz_topic = st.text_input("Topic for the quiz", placeholder="e.g. OSI Model, Binary Search Trees")
    num_questions = st.slider("Number of questions", 3, 10, 5)
    q_type = st.radio("Question type", ["Multiple Choice (MCQ)", "Short Answer"], horizontal=True)

    if st.button("Generate Quiz", type="primary"):
        if not quiz_topic.strip():
            st.error("Type a topic first!")
        elif client is None:
            st.error("Add your Groq API key in the sidebar first.")
        else:
            if q_type == "Multiple Choice (MCQ)":
                format_instruction = (
                    "Format each question as:\nQ1. <question>\nA) ... B) ... C) ... D) ...\n"
                    "Correct Answer: <letter>\n\nLeave a blank line between questions."
                )
            else:
                format_instruction = (
                    "Format each question as:\nQ1. <question>\nAnswer: <short answer, 1-2 sentences>\n\n"
                    "Leave a blank line between questions."
                )

            system_prompt = (
                "You are a study assistant generating exam-style self-test questions for a "
                "Computer Science engineering student (KTU syllabus, India). "
                f"Generate exactly {num_questions} questions on the topic given. {format_instruction} "
                "Keep questions clear and at an undergraduate exam difficulty level."
            )
            with st.spinner("Generating quiz..."):
                try:
                    answer = ask_groq(client, system_prompt, quiz_topic, temperature=0.6)
                    st.markdown("### Quiz")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Something went wrong calling the API: {e}")

st.markdown("---")
st.caption("Powered by Groq (Llama 3.3 70B) · Built for Epochs '26 - Assignment 10")
