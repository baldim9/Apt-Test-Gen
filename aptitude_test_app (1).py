import streamlit as st
import pandas as pd
import random

# Title
st.title("🧠 Aptitude Test Generator for Kids (Ages 8–16)")

# Upload question bank
uploaded_file = st.file_uploader("📤 Upload your question bank CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Select age group and category
    age_group = st.selectbox("Select Age Group", sorted(df["age_group"].unique()))
    category = st.selectbox("Select Category", sorted(df["category"].unique()))

    # Filter questions
    filtered = df[(df["age_group"] == age_group) & (df["category"] == category)]

    # Randomly select 5 questions
    questions = filtered.sample(n=min(5, len(filtered)), random_state=42)

    st.subheader("📝 Your Aptitude Test")

    user_answers = {}

    for i, row in questions.iterrows():
        st.markdown(f"**Q{i+1}: {row['question']}**")
        options = row["options"].split(";")
        user_answers[i] = st.radio(
            label="Choose your answer:",
            options=options,
            index=None,
            key=f"question_{i}"
        )

    if st.button("Submit Answers"):
        score = 0
        for i, row in questions.iterrows():
            correct = row["answer"]
            if user_answers[i] == correct:
                score += 1
        st.success(f"✅ You scored {score} out of {len(questions)}.")
else:
    st.info("Please upload a question bank CSV to begin.")

