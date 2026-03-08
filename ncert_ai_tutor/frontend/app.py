"""NCERT AI Tutor — Streamlit Frontend Entry Point."""

import streamlit as st
from pathlib import Path

# Page config must be first Streamlit command
st.set_page_config(
    page_title="Padhai Buddy — NCERT AI Tutor",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Initialize session state
if "username" not in st.session_state:
    st.session_state.username = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Sidebar — Student Identity
st.sidebar.title("📚 Padhai Buddy")
st.sidebar.markdown("*NCERT Class 9-10 AI Tutor*")
st.sidebar.markdown("---")

if not st.session_state.logged_in:
    username = st.sidebar.text_input(
        "Apna naam enter karo:",
        placeholder="e.g., Rahul, Priya, Karthik...",
        key="username_input",
    )
    if st.sidebar.button("Start Learning! 🚀", type="primary"):
        if username.strip():
            st.session_state.username = username.strip()
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.sidebar.error("Please enter your name!")
else:
    st.sidebar.success(f"Welcome, **{st.session_state.username}**! 👋")
    if st.sidebar.button("Logout"):
        st.session_state.username = ""
        st.session_state.logged_in = False
        st.session_state.pop("chat_history", None)
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Subjects:** Science, Maths, Social Science\n\n"
    "**Classes:** 9th & 10th\n\n"
    "**Languages:** Hinglish, Tanglish, English"
)

# Main page content
st.title("📚 Padhai Buddy — NCERT AI Tutor")
st.markdown(
    """
    > *Tera apna AI bhaiya/didi jo NCERT samjhaye bilkul easy language mein!*

    ### 🎯 Kya kar sakte ho:
    - **💬 Chat:** Koi bhi doubt puchho — Hinglish, Tanglish, English mein
    - **📝 Practice:** Topic select karo, questions generate karo
    - **🔥 Streaks:** Daily padhai ka streak maintain karo
    - **👨‍🏫 Teacher Dashboard:** Analytics dekho (teachers ke liye)

    ### 📖 How to use:
    1. Apna naam enter karo sidebar mein
    2. Left sidebar se page select karo
    3. Questions puchho aur padhai shuru karo!
    """
)

if not st.session_state.logged_in:
    st.info("👈 Pehle apna naam enter karo sidebar mein to get started!")
else:
    st.success(f"✅ Naam entered: **{st.session_state.username}** — Ab sidebar se page select karo!")

    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Subjects", "3")
    with col2:
        st.metric("📖 Topics", "55+")
    with col3:
        st.metric("🎯 Classes", "9th & 10th")
