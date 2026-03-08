"""Study Streak Dashboard Page."""

import streamlit as st
import httpx
import pandas as pd
from datetime import date, timedelta

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Streaks — Padhai Buddy", page_icon="🔥", layout="wide")
st.title("🔥 Study Streak Dashboard")

if not st.session_state.get("logged_in"):
    st.warning("⚠️ Pehle Home page pe jaake apna naam enter karo!")
    st.stop()

username = st.session_state.username
st.markdown(f"*Tracking streaks for **{username}***")

# Fetch streak data
try:
    resp = httpx.get(f"{API_BASE}/api/streaks/{username}", timeout=15)
    if resp.status_code == 200:
        data = resp.json()

        # ── Main Metrics ──
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            streak = data.get("current_streak", 0)
            fire = "🔥" * min(streak, 5) if streak > 0 else "❄️"
            st.markdown(f"### {fire}")
            st.metric("Current Streak", f"{streak} days")

        with col2:
            st.metric("🏆 Longest Streak", f"{data.get('longest_streak', 0)} days")

        with col3:
            today_count = data.get("today_count", 0)
            st.metric("📝 Today's Questions", f"{today_count}/3")

        with col4:
            threshold = 3
            progress = min(today_count / threshold, 1.0)
            if progress >= 1.0:
                st.markdown("### ✅")
                st.markdown("**Today's streak secured!**")
            else:
                remaining = threshold - today_count
                st.markdown(f"### ⏳")
                st.markdown(f"**{remaining} more to go!**")

        # ── Progress Bar ──
        st.markdown("### Today's Progress")
        st.progress(min(today_count / 3, 1.0))
        if today_count >= 3:
            st.success("🎉 Aaj ka streak complete! Bohot badhiya!")
        else:
            st.info(f"Aur {max(3 - today_count, 0)} questions puchho streak maintain karne ke liye!")

        # ── Streak Rules ──
        st.markdown("---")
        st.markdown("### 📋 Streak Rules")
        st.markdown(
            """
            | Rule | Details |
            |------|---------|
            | ✅ Streak Active | Ask **3 or more** questions in a day |
            | 🔥 Current Streak | Consecutive days with 3+ questions |
            | ❄️ Streak Break | Miss a day = streak resets to 0 |
            | 🏆 Goal | Build the longest streak! |
            """
        )

        # ── History Chart ──
        history = data.get("history", [])
        if history:
            st.markdown("---")
            st.markdown("### 📊 Question History (Last 30 Days)")

            df = pd.DataFrame(history)
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date")

            st.bar_chart(df.set_index("date")["question_count"])

            # Calendar-style heatmap
            st.markdown("### 📅 Streak Calendar")
            active_dates = set(
                row["date"] for row in history if row.get("streak_active")
            )

            # Simple calendar display
            today = date.today()
            cols = st.columns(7)
            day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            for i, name in enumerate(day_names):
                cols[i].markdown(f"**{name}**")

            # Show last 28 days
            start_date = today - timedelta(days=27)
            # Align to Monday
            start_date -= timedelta(days=start_date.weekday())

            for week in range(4):
                cols = st.columns(7)
                for day in range(7):
                    d = start_date + timedelta(days=week * 7 + day)
                    d_str = d.isoformat()
                    if d_str in active_dates:
                        cols[day].markdown(f"🔥 {d.day}")
                    elif d == today:
                        cols[day].markdown(f"📍 {d.day}")
                    elif d <= today:
                        cols[day].markdown(f"⬜ {d.day}")
                    else:
                        cols[day].markdown(f"  {d.day}")
        else:
            st.info("Abhi tak koi streak data nahi hai. Chat page pe jaake questions puchho! 💪")

    else:
        st.error(f"Error fetching streak data: {resp.status_code}")

except httpx.ConnectError:
    st.error(
        "❌ Backend server not running!\n\n"
        "Run this command first: `python run.py`"
    )
