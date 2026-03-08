"""Student Chat Page — Main AI chat interface."""

import streamlit as st
import httpx

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Chat — Padhai Buddy", page_icon="💬", layout="wide")
st.title("💬 Padhai Buddy Chat")

# Check if user is logged in
if not st.session_state.get("logged_in"):
    st.warning("⚠️ Pehle Home page pe jaake apna naam enter karo!")
    st.stop()

username = st.session_state.username
st.markdown(f"*Chatting as **{username}***")

# Initialize chat history in session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for idx, msg in enumerate(st.session_state.chat_history):
    role = msg["role"]
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(msg["content"])

        # Voice button for assistant messages
        if role == "assistant" and msg["content"]:
            if st.button("🔊 Listen", key=f"voice_{idx}"):
                with st.spinner("Generating audio..."):
                    try:
                        resp = httpx.post(
                            f"{API_BASE}/api/chat/voice",
                            json={"text": msg["content"]},
                            timeout=30,
                        )
                        if resp.status_code == 200:
                            st.audio(resp.content, format="audio/mpeg")
                        else:
                            st.error("Audio generation failed.")
                    except httpx.ConnectError:
                        st.error("Backend server not running. Start it with `python run.py`")

# Chat input
if prompt := st.chat_input("Apna doubt puchho... (e.g., 'bhaiya photosynthesis samjha do')"):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Call backend API
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon... 🤔"):
            try:
                # Build conversation history for context
                conv_history = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.chat_history[-6:]
                ]

                resp = httpx.post(
                    f"{API_BASE}/api/chat",
                    json={
                        "question": prompt,
                        "username": username,
                        "conversation_history": conv_history,
                    },
                    timeout=60,
                )

                if resp.status_code == 200:
                    data = resp.json()
                    answer = data["answer"]
                    topic = data.get("detected_topic", "")
                    difficulty = data.get("difficulty_level", "normal")

                    # Show topic badge
                    if topic:
                        st.caption(f"📌 Topic: {topic} | Difficulty: {difficulty}")

                    st.markdown(answer)

                    # Store assistant response
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )

                    # Voice button
                    voice_key = f"voice_new_{len(st.session_state.chat_history)}"
                    if st.button("🔊 Listen to explanation", key=voice_key):
                        with st.spinner("Generating audio..."):
                            voice_resp = httpx.post(
                                f"{API_BASE}/api/chat/voice",
                                json={"text": answer},
                                timeout=30,
                            )
                            if voice_resp.status_code == 200:
                                st.audio(voice_resp.content, format="audio/mpeg")
                else:
                    st.error(f"Error: {resp.status_code} — {resp.text}")
            except httpx.ConnectError:
                st.error(
                    "❌ Backend server not running!\n\n"
                    "Run this command first:\n"
                    "```\npython run.py\n```"
                )

# Sidebar tips
st.sidebar.markdown("### 💡 Tips")
st.sidebar.markdown(
    """
    - Hinglish mein puchho: *"bhaiya photosynthesis kya hai?"*
    - Tanglish mein: *"anna, Newton's law puringiducha?"*
    - English mein bhi chal jayega!
    - Ek hi topic baar baar puchho → easier explanation milega
    - Roz 3+ questions = 🔥 streak!
    """
)
