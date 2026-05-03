import streamlit as st
from datetime import date
from dotenv import load_dotenv
from utils import predict_priority, explain_priority, save_user_data
from llm import generate_tips

load_dotenv()

st.set_page_config(page_title="NEB Plus Two Study Planner", layout="centered")

st.title("NEB Plus Two Study Planner")
st.caption("Simple NEB Class 12 exam planning for Science, Management, and Humanities.")

st.divider()

st.header("Student inputs")
cols = st.columns(2)
with cols[0]:
    subjects = st.text_input("Subjects", placeholder="mathematics, nepali, physics, accountancy")
    department = st.selectbox("Department", ["Science", "Management", "Humanities"])
    exam_date = st.date_input("Exam Date")
with cols[1]:
    confidence = st.text_input("Confidence level (1–5)", placeholder="1, 2, 3, 4")
    study_hours = st.text_input("Study hours available", placeholder="2, 1, 3, 4")
    past_scores = st.text_input("Past scores (out of 100)", placeholder="73, 21, 55, 68")
    st.caption("Enter NEB marks on a 100-point scale: theory + practical = 100.")

hours_per_day = st.slider("Hours per day", 1, 12, 4)

st.divider()

if st.button("Generate Plan", use_container_width=True):

    try:
        subjects = [s.strip() for s in subjects.split(",") if s.strip()]
        confidence = [int(c.strip()) for c in confidence.split(",") if c.strip()]
        study_hours = [int(h.strip()) for h in study_hours.split(",") if h.strip()]
        past_scores = [int(p.strip()) for p in past_scores.split(",") if p.strip()]

        # Validate inputs
        if not (len(subjects) == len(confidence) == len(study_hours) == len(past_scores)):
            st.error("❌ Error: All inputs must have the same number of values.")
            st.stop()

        days_left = (exam_date - date.today()).days

        if days_left <= 0:
            st.error("❌ Error: Exam date must be in the future.")
            st.stop()

        avg_confidence = sum(confidence) / len(confidence)
        total_study_hours = sum(study_hours)
        ideal_study_time = hours_per_day * days_left
        study_ratio = min(1.0, total_study_hours / max(1, ideal_study_time))
        readiness = int(min(100, avg_confidence * 18 + study_ratio * 55 + (10 if days_left >= 7 else 5)))

        weak_subjects = [s for s, c in zip(subjects, confidence) if c <= 2]
        low_score_subjects = [s for s, score in zip(subjects, past_scores) if score < 50]
        weak_ratio = len(weak_subjects) / len(subjects)
        low_score_ratio = len(low_score_subjects) / len(subjects)
        focus_score = int(max(0, min(100, 100 - (weak_ratio * 40 + low_score_ratio * 30 + (1 - study_ratio) * 30))))

        st.subheader("Exam readiness")
        st.progress(readiness / 100)
        st.write(f"Estimated readiness score: **{readiness}%**")
        st.caption("Based on confidence, study hours, and remaining days.")

        st.subheader("Focus score")
        st.progress(focus_score / 100)
        st.write(f"Focus score: **{focus_score}%**")
        st.caption("Higher focus means you are working on the right weak subjects.")

        df = predict_priority(subjects, confidence, study_hours, past_scores)

        st.subheader("Priority ranking")
        st.table(df)

        st.subheader("Why these priorities")
        for exp in explain_priority(df):
            st.write(exp)

        st.write(f"**Department:** {department}")

        save_user_data(df)

        st.subheader("Study recommendations")
        with st.spinner("Generating recommendations..."):
            tips = generate_tips(subjects, confidence, days_left, department)
            st.markdown(tips)

    except Exception as e:
        st.error(f"Error: {e}")