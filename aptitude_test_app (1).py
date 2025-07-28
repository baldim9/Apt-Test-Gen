
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Aptitude Test Generator", layout="centered")

st.title("🧠 Aptitude Test Generator for Kids (Ages 8–16)")

# Load or upload question bank
st.sidebar.header("📚 Question Bank")
uploaded_file = st.sidebar.file_uploader("Upload your question bank (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Sample question bank
    data = {
        "age_group": ["8-10", "8-10", "11-13", "11-13", "14-16", "14-16"],
        "category": ["Math", "Logic", "Math", "Verbal", "Logic", "Verbal"],
        "question": [
            "What is 7 + 5?",
            "Which shape has 3 sides?",
            "What is 12 × 3?",
            "Choose the synonym of 'happy'.",
            "If all bloops are razzies and all razzies are lazzies, are all bloops definitely lazzies?",
            "Choose the antonym of 'ancient'."
        ],
        "options": [
            "10;11;12;13",
            "Circle;Triangle;Square;Rectangle",
            "36;24;30;15",
            "Sad;Angry;Joyful;Tired",
            "Yes;No;Cannot say;Maybe",
            "Old;Modern;New;Young"
        ],
        "answer": ["12", "Triangle", "36", "Joyful", "Yes", "Modern"]
    }
    df = pd.DataFrame(data)

# Allow user to download the current question bank
st.sidebar.download_button("Download Sample Question Bank", df.to_csv(index=False), file_name="sample_question_bank.csv")

# Select age group and category
st.subheader("🎯 Select Test Parameters")
age_group = st.selectbox("Choose Age Group", sorted(df["age_group"].unique()))
category = st.selectbox("Choose Category", sorted(df["category"].unique()))

# Filter questions
filtered = df[(df["age_group"] == age_group) & (df["category"] == category)]

if filtered.empty:
    st.warning("No questions found for this combination. Try another.")
else:
    st.subheader("📝 Your Aptitude Test")
    questions = filtered.sample(min(5, len(filtered))).reset_index(drop=True)

    score = 0
    for i, row in questions.iterrows():
        st.markdown(f"**Q{i+1}: {row['question']}**")
        options = row["options"].split(";")
        user_answer = st.radio("", options, key=i)
        if user_answer == row["answer"]:
            score += 1

    if st.button("Submit Test"):
        st.success(f"You scored {score} out of {len(questions)}!")
