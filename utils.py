import pandas as pd
import joblib
import os

model = joblib.load("model.pkl")
USER_DATA_PATH = "user_data.csv"

def predict_priority(subjects, confidence, study_hours, past_scores):
    df = pd.DataFrame({
        "Subject": subjects,
        "confidence": confidence,
        "study_hours": study_hours,
        "past_score": past_scores
    })

    preds = model.predict(df[["confidence", "study_hours", "past_score"]])
    df["priority_score"] = preds
    df["priority_score"] /= df["priority_score"].sum()

    display_df = df.rename(columns={
        "confidence": "Confidence",
        "study_hours": "Study Hours",
        "past_score": "Past Score",
        "priority_score": "Priority Score"
    })

    return display_df.sort_values(by="Priority Score", ascending=False)


def explain_priority(df):
    explanations = []

    for _, row in df.iterrows():
        reasons = []

        if row["Confidence"] <= 2:
            reasons.append(f"Low confidence ({row['Confidence']}/5)")
        if row["Past Score"] < 50:
            reasons.append(f"Weak previous performance ({row['Past Score']}%)")
        if row["Study Hours"] < 2:
            reasons.append(f"Limited study time ({row['Study Hours']} hrs)")

        if not reasons:
            reasons.append("Strong performance - maintain current level")

        explanation = f"**{row['Subject']}** → High priority because: {', '.join(reasons)}"
        explanations.append(explanation)

    return explanations


def save_user_data(df):
    data = df[["Confidence", "Study Hours", "Past Score", "Priority Score"]]
    data.columns = ["confidence", "study_hours", "past_score", "priority_score"]

    if os.path.exists(USER_DATA_PATH):
        data.to_csv(USER_DATA_PATH, mode="a", header=False, index=False)
    else:
        data.to_csv(USER_DATA_PATH, index=False)