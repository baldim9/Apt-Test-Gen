import streamlit as st
import pandas as pd
import random

# Load the question bank CSV
@st.cache_data
def load_question_bank():
    return pd.read_csv("verified_question_bank_complete.csv")

df = load_question_bank()

st.title("Aptitude Test Generator")

# Dropdowns for age group and subject
age_group = st.selectbox("Select Age Group", options=[""] + sorted(df['age_group'].unique().tolist()))
subject = st.selectbox("Select Subject", options=[""] + sorted(df['category'].unique().tolist()))

# Show buttons only when both dropdowns are selected
if age_group and subject:
    if "questions" not in st.session_state or st.button("Refresh Questions"):
        filtered_df = df[(df['age_group'] == age_group) & (df['category'] == subject)].copy()
        filtered_df = filtered_df.sample(frac=1).reset_index(drop=True)  # Shuffle questions
        filtered_df.insert(0, "Q#", ["Q" + str(i+1) for i in range(len(filtered_df))])
        st.session_state.questions = filtered_df

    if st.button("Generate Questions"):
        filtered_df = df[(df['age_group'] == age_group) & (df['category'] == subject)].copy()
        filtered_df = filtered_df.sample(frac=1).reset_index(drop=True)  # Shuffle questions
        filtered_df.insert(0, "Q#", ["Q" + str(i+1) for i in range(len(filtered_df))])
        st.session_state.questions = filtered_df

# Display questions if available
if "questions" in st.session_state:
    for idx, row in st.session_state.questions.iterrows():
        st.markdown(f"**{row['Q#']}. {row['question']}**")
        options = row['options'].split(';')
        st.radio(f"Select an answer for {row['Q#']}", options, key=f"q_{idx}")

