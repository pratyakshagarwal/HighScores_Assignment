import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Adaptive IQ", page_icon="◈", layout="wide")

# ---- state init ----
defaults = {
    "session_id": None, "question": None,
    "answered": False, "result": None,
    "ability": 0.5, "total_correct": 0,
    "total_attempted": 0, "max_streak": 0,
    "current_streak": 0, "history": [],
    "finished": False, "finish_data": None
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.title("Adaptive IQ")

# ===== START SCREEN =====
if st.session_state.session_id is None:
    st.write("Click below to begin the adaptive test. Questions adapt to your ability in real time.")
    if st.button("Start Test"):
        res = requests.post(f"{API_URL}/start-session")
        print(res)
        st.session_state.session_id = res.json()["session_id"]
        st.rerun()
    st.stop()

# ===== FINISHED SCREEN =====
if st.session_state.finished and st.session_state.finish_data:
    d = st.session_state.finish_data

    st.subheader("Assessment Complete")

    correct = d.get("total_correct", 0)
    attempted = d.get("total_attempted", 0)
    acc = round(correct / attempted * 100) if attempted else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Final Ability", f"{d.get('final_ability', 0):.3f}")
    col2.metric("Accuracy", f"{correct}/{attempted}")
    col3.metric("Score", f"{acc}%")
    col4.metric("Best Streak", d.get("max_streak", 0))
    col5.metric("Avg Difficulty", f"{d.get('avg_difficulty_attempted', 0):.2f}")

    traj = d.get("ability_trajectory", [])
    if traj:
        st.subheader("Ability Trajectory")
        st.line_chart({"Ability": traj}, height=150)

    topic_acc = d.get("topic_accuracy", {})
    topic_stats = d.get("topic_stats", {})
    weak = d.get("weak_topics", [])
    strong = d.get("strong_topics", [])

    if topic_acc:
        st.subheader("Topic Breakdown")
        for topic, info in topic_acc.items():
            if isinstance(info, dict):
                acc_val = info.get("accuracy", 0)
                attempted_t = info.get("attempted", 0)
                correct_t = info.get("correct", 0)
                avg_diff = info.get("avg_difficulty", 0)
            else:
                acc_val = info
                attempted_t = topic_stats.get(topic, {}).get("attempted", "?")
                correct_t = topic_stats.get(topic, {}).get("correct", "?")
                avg_diff = 0

            tag = "🔴 WEAK" if topic in weak else "🟢 STRONG" if topic in strong else "🟡"
            st.write(f"**{topic}** {tag} — {int(acc_val*100)}% ({correct_t}/{attempted_t} correct, avg difficulty {avg_diff:.2f})")
            st.progress(acc_val)

    st.subheader("AI Study Plan")
    st.write(d.get("study_plan", ""))

    st.divider()
    if st.button("Start New Test"):
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()
    st.stop()

# ===== IN-PROGRESS HUD =====
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ability", f"{st.session_state.ability:.3f}")
col2.metric("Correct", f"{st.session_state.total_correct}/{st.session_state.total_attempted}")
col3.metric("Streak", st.session_state.current_streak)
col4.metric("Best Streak", st.session_state.max_streak)

st.progress(st.session_state.ability)

# fetch question
if st.session_state.question is None and not st.session_state.answered:
    res = requests.get(f"{API_URL}/next-question/{st.session_state.session_id}")
    data = res.json()
    if "question_id" not in data:
        st.info("No more questions available.")
        st.stop()
    st.session_state.question = data

# display question
if st.session_state.question:
    q = st.session_state.question
    diff = q.get("difficulty", 0)
    diff_label = "Easy" if diff < 0.4 else "Medium" if diff < 0.65 else "Hard"

    st.divider()
    st.caption(f"Q{st.session_state.total_attempted + 1}  ·  {q.get('topic', '')}  ·  Difficulty {diff:.2f} ({diff_label})")
    st.subheader(q["question"])

    options = q["options"]
    answer_key = st.radio("Choose your answer:", list(options.keys()),
                          format_func=lambda x: f"{x})  {options[x]}",
                          disabled=st.session_state.answered)

    if not st.session_state.answered:
        if st.button("Submit Answer"):
            payload = {
                "session_id": st.session_state.session_id,
                "question_id": q["question_id"],
                "answer": answer_key
            }
            res = requests.post(f"{API_URL}/submit-answer", json=payload)
            result = res.json()
            st.session_state.result = result
            st.session_state.answered = True
            st.session_state.ability = result["new_ability"]
            st.session_state.total_attempted += 1
            if result["correct"]:
                st.session_state.total_correct += 1
                st.session_state.current_streak += 1
                st.session_state.max_streak = max(st.session_state.max_streak, st.session_state.current_streak)
            else:
                st.session_state.current_streak = 0
            st.rerun()

# feedback + next
if st.session_state.answered and st.session_state.result:
    r = st.session_state.result
    if r["correct"]:
        st.success(f"Correct! New ability: {r['new_ability']:.3f}")
    else:
        st.error(f"Incorrect. New ability: {r['new_ability']:.3f}")

    if st.button("Next Question →"):
        st.session_state.question = None
        st.session_state.answered = False
        st.session_state.result = None
        st.rerun()

# finish button
st.divider()
if st.button("Finish & Get Study Plan"):
    with st.spinner("Analyzing your performance and generating study plan..."):
        res = requests.get(f"{API_URL}/finish-test/{st.session_state.session_id}")
        data = res.json()
    st.session_state.finish_data = data
    st.session_state.finished = True
    st.rerun()