import streamlit as st
import pandas as pd
import random

# Load the question bank
df = pd.read_csv("verified_question_bank_complete.csv")

# App title
st.title("🧠 Aptitude Test Generator for Kids")

# Dropdowns for age group and category (no default selection)
age_group = st.selectbox("Select Age Group", options=["", "8-10", "11-13", "14-16"])
category = st.selectbox("Select Subject", options=["", "Math", "Logic", "Verbal"])

# Function to generate questions
def generate_questions(age_group, category, num_questions=5):
    filtered = df[(df['age_group'] == age_group) & (df['category'] == category)]
    return filtered.sample(n=min(num_questions, len(filtered))).reset_index(drop=True)

# Session state to store questions
if 'questions' not in st.session_state:
    st.session_state.questions = pd.DataFrame()

# Generate or refresh questions
if age_group and category:
    if st.button("Generate Questions") or st.button("Refresh Questions"):
        st.session_state.questions = generate_questions(age_group, category)

# Display questions
if not age_group or not category:
    st.info("Please select both age group and subject to generate questions.")
elif not st.session_state.questions.empty:
    st.subheader("Your Questions")
    for idx, row in st.session_state.questions.iterrows():
        st.markdown(f"**Q{idx+1}. {row['question']}**")
        options = row['options'].split(';')
        st.radio(f"Options for Q{idx+1}", options, key=f"q{idx+1}")

