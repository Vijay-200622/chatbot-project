"""Practice Questions & Mistake Analyzer Page."""

import streamlit as st
import httpx

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Practice — Padhai Buddy", page_icon="📝", layout="wide")
st.title("📝 Practice Questions & Mistake Analyzer")

if not st.session_state.get("logged_in"):
    st.warning("⚠️ Pehle Home page pe jaake apna naam enter karo!")
    st.stop()

# ── Section 1: Practice Question Generator ────────────────────────

st.header("🎯 Practice Question Generator")
st.markdown("Topic select karo, questions generate karo — Easy, Medium, Hard!")

col1, col2 = st.columns([2, 1])

# Topic selection
TOPIC_LIST = [
    "States of Matter", "Mixtures and Solutions", "Atoms and Molecules",
    "Atomic Structure", "Cell Biology", "Tissues",
    "Motion and Kinematics", "Newton's Laws", "Gravitation",
    "Work and Energy", "Sound", "Food Resources",
    "Number Systems", "Polynomials", "Coordinate Geometry",
    "Linear Equations", "Triangles", "Quadrilaterals",
    "Circles", "Heron's Formula", "Surface Areas and Volumes",
    "Statistics", "Probability",
    "French Revolution", "India Geography Basics", "Democracy", "Village Economy",
    "Chemical Reactions", "Acids, Bases, Salts", "Metals and Non-metals",
    "Carbon Compounds", "Life Processes", "Control and Coordination",
    "Reproduction", "Heredity and Evolution",
    "Light - Reflection and Refraction", "Human Eye",
    "Electricity", "Magnetism and Electromagnetism", "Environment and Ecosystem",
    "Real Numbers", "Polynomials (Class 10)", "Pair of Linear Equations",
    "Quadratic Equations", "Arithmetic Progressions",
    "Similar Triangles", "Trigonometry",
    "Circles (Class 10)", "Areas Related to Circles",
    "Surface Areas and Volumes (Class 10)", "Statistics (Class 10)", "Probability (Class 10)",
    "Nationalism in Europe", "Indian National Movement",
    "Resources", "Power Sharing", "Economic Development",
]

with col1:
    selected_topic = st.selectbox("📖 Topic select karo:", TOPIC_LIST)

with col2:
    class_level = st.radio("Class:", [9, 10], horizontal=True)

if st.button("🎲 Generate Practice Questions", type="primary"):
    with st.spinner("Questions generate ho rahe hain..."):
        try:
            resp = httpx.post(
                f"{API_BASE}/api/practice",
                json={"topic": selected_topic, "class_level": class_level},
                timeout=60,
            )
            if resp.status_code == 200:
                data = resp.json()

                # Easy
                st.markdown("### 🟢 Easy")
                st.success(data.get("easy", "No question generated"))

                # Medium
                st.markdown("### 🟡 Medium")
                st.warning(data.get("medium", "No question generated"))

                # Hard
                st.markdown("### 🔴 Hard")
                st.error(data.get("hard", "No question generated"))
            else:
                st.error(f"Error: {resp.status_code}")
        except httpx.ConnectError:
            st.error("❌ Backend server not running! Run `python run.py` first.")

st.markdown("---")

# ── Section 2: Concept Map ────────────────────────────────────────

st.header("🗺️ Concept Map Generator")
st.markdown("Topic ka visual concept map dekho!")

map_topic = st.selectbox("📖 Concept map ke liye topic:", TOPIC_LIST, key="map_topic")

if st.button("🗺️ Generate Concept Map", type="secondary"):
    with st.spinner("Concept map ban raha hai..."):
        try:
            resp = httpx.post(
                f"{API_BASE}/api/concept-map",
                json={"topic": map_topic},
                timeout=60,
            )
            if resp.status_code == 200:
                data = resp.json()
                svg = data.get("svg", "")
                if svg:
                    st.markdown("### Concept Map:")
                    st.image(svg)

                # Show edges as text too
                edges = data.get("edges", [])
                if edges:
                    st.markdown("### Relationships:")
                    for parent, child in edges:
                        st.markdown(f"- **{parent}** → {child}")
            else:
                st.error(f"Error: {resp.status_code}")
        except httpx.ConnectError:
            st.error("❌ Backend server not running!")

st.markdown("---")

# ── Section 3: Mistake Analyzer ──────────────────────────────────

st.header("🔍 Mistake Analyzer")
st.markdown("Apna galat answer paste karo, AI batayega kya galti hui aur kaise sudhaarein!")

mistake_topic = st.selectbox("📖 Topic (optional):", [""] + TOPIC_LIST, key="mistake_topic")
question_text = st.text_area(
    "❓ Question (optional):",
    placeholder="e.g., What is photosynthesis?",
    height=80,
)
student_answer = st.text_area(
    "✍️ Apna answer paste karo:",
    placeholder="Yahan pe apna answer likho jo galat ho gaya tha exam mein...",
    height=150,
)

if st.button("🔎 Analyze My Answer", type="primary", key="analyze_btn"):
    if not student_answer.strip():
        st.error("Answer field empty hai! Apna answer paste karo.")
    else:
        with st.spinner("Answer analyze ho raha hai..."):
            try:
                resp = httpx.post(
                    f"{API_BASE}/api/analyze-mistake",
                    json={
                        "student_answer": student_answer,
                        "question": question_text,
                        "topic": mistake_topic,
                    },
                    timeout=60,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.markdown("### 📋 Analysis:")
                    st.markdown(data.get("analysis", "Analysis not available"))
                else:
                    st.error(f"Error: {resp.status_code}")
            except httpx.ConnectError:
                st.error("❌ Backend server not running!")
