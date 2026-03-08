"""Teacher Analytics Dashboard Page."""

import streamlit as st
import httpx
import pandas as pd

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Teacher Dashboard — Padhai Buddy", page_icon="👨‍🏫", layout="wide")
st.title("👨‍🏫 Teacher Analytics Dashboard")

# ── Teacher Login ─────────────────────────────────────────────────

if "teacher_logged_in" not in st.session_state:
    st.session_state.teacher_logged_in = False

if not st.session_state.teacher_logged_in:
    st.markdown("### 🔐 Teacher Login")
    st.markdown("*Default credentials: username=`teacher`, password=`teach123`*")

    with st.form("teacher_login"):
        teacher_user = st.text_input("Username:")
        teacher_pass = st.text_input("Password:", type="password")
        submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            if not teacher_user or not teacher_pass:
                st.error("Please enter both username and password.")
            else:
                try:
                    resp = httpx.post(
                        f"{API_BASE}/api/auth/login",
                        json={"username": teacher_user, "password": teacher_pass},
                        timeout=15,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get("success"):
                            st.session_state.teacher_logged_in = True
                            st.session_state.teacher_name = teacher_user
                            st.rerun()
                        else:
                            st.error(data.get("message", "Login failed"))
                    else:
                        st.error("Server error")
                except httpx.ConnectError:
                    st.error("❌ Backend server not running!")
    st.stop()

# ── Dashboard (after login) ──────────────────────────────────────

st.success(f"✅ Logged in as **{st.session_state.get('teacher_name', 'Teacher')}**")

if st.button("🚪 Logout"):
    st.session_state.teacher_logged_in = False
    st.session_state.pop("teacher_name", None)
    st.rerun()

st.markdown("---")

try:
    # Fetch all analytics data
    weekly_resp = httpx.get(f"{API_BASE}/api/analytics/weekly-topics", timeout=15)
    confused_resp = httpx.get(f"{API_BASE}/api/analytics/confused-topics", timeout=15)
    daily_resp = httpx.get(f"{API_BASE}/api/analytics/daily-counts?days=30", timeout=15)

    # ── Section 1: Top Topics This Week ──
    st.header("📊 Top Asked Topics This Week")
    if weekly_resp.status_code == 200:
        weekly_data = weekly_resp.json()
        if weekly_data:
            df_weekly = pd.DataFrame(weekly_data)
            st.bar_chart(df_weekly.set_index("topic")["count"])

            st.dataframe(df_weekly, use_container_width=True, hide_index=True)
        else:
            st.info("No data yet. Students haven't asked questions this week.")
    else:
        st.error("Failed to fetch weekly topics")

    st.markdown("---")

    # ── Section 2: Most Confusing Topics ──
    st.header("🤔 Most Confusing Topics")
    st.markdown("*Topics that the same student asks about repeatedly*")
    if confused_resp.status_code == 200:
        confused_data = confused_resp.json()
        if confused_data:
            df_confused = pd.DataFrame(confused_data)
            st.dataframe(df_confused, use_container_width=True, hide_index=True)

            # Aggregate by topic
            topic_confusion = {}
            for row in confused_data:
                topic = row["topic"]
                topic_confusion[topic] = topic_confusion.get(topic, 0) + row["repeat_count"]

            if topic_confusion:
                df_agg = pd.DataFrame(
                    [{"topic": k, "total_repeats": v} for k, v in topic_confusion.items()]
                ).sort_values("total_repeats", ascending=False)
                st.bar_chart(df_agg.set_index("topic")["total_repeats"])
        else:
            st.info("No confused topics detected yet.")
    else:
        st.error("Failed to fetch confused topics")

    st.markdown("---")

    # ── Section 3: Daily Question Frequency ──
    st.header("📈 Daily Question Frequency (Last 30 Days)")
    if daily_resp.status_code == 200:
        daily_data = daily_resp.json()
        if daily_data:
            df_daily = pd.DataFrame(daily_data)
            df_daily["date"] = pd.to_datetime(df_daily["date"])
            df_daily = df_daily.sort_values("date")

            st.line_chart(df_daily.set_index("date")["count"])
        else:
            st.info("No daily data available yet.")
    else:
        st.error("Failed to fetch daily counts")

    st.markdown("---")

    # ── Section 4: Summary Metrics ──
    st.header("📋 Summary")
    col1, col2, col3 = st.columns(3)

    weekly_data = weekly_resp.json() if weekly_resp.status_code == 200 else []
    daily_data = daily_resp.json() if daily_resp.status_code == 200 else []

    total_questions_week = sum(t.get("count", 0) for t in weekly_data)
    total_topics = len(weekly_data)
    total_questions_month = sum(d.get("count", 0) for d in daily_data)

    with col1:
        st.metric("Questions This Week", total_questions_week)
    with col2:
        st.metric("Unique Topics This Week", total_topics)
    with col3:
        st.metric("Questions This Month", total_questions_month)

except httpx.ConnectError:
    st.error("❌ Backend server not running! Run `python run.py` first.")
