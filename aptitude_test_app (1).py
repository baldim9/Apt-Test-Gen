import streamlit as st
import pandas as pd
import random

# Load the question bank
df = pd.read_csv("verified_question_bank_complete.csv")

# Set up the Streamlit app
st.title("Aptitude Test Generator")

# Dropdowns for age group and subject with no default selection
age_group = st.selectbox("Select Age Group", options=[""] + sorted(df['age_group'].unique().tolist()))
subject = st.selectbox("Select Subject", options=[""] + sorted(df['category'].unique().tolist()))

# Initialize session state for questions
if 'questions' not in st.session_state:
    st.session_state.questions = []

# Function to generate questions
def generate_questions():
    filtered_df = df[(df['age_group'] == age_group) & (df['category'] == subject)]
    st.session_state.questions = filtered_df.sample(n=min(10, len(filtered_df))).reset_index(drop=True)

# Show buttons only if both dropdowns are selected
if age_group and subject:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Generate Questions"):
            generate_questions()
    with col2:
        if st.button("Refresh Questions"):
            generate_questions()

# Display questions if available
if st.session_state.questions:
    st.subheader("Your Questions")
    for i, row in st.session_state.questions.iterrows():
        st.markdown(f"**Q{i+1}: {row['question']}**")
        options = row['options'].split(';')
        st.radio(f"Options for Q{i+1}", options, key=f"q{i+1}")

