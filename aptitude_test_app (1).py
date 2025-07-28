import streamlit as st
import pandas as pd
import os

# Title
st.title("Aptitude Test Generator")

# Load question bank only if the file exists
@st.cache_data
def load_question_bank():
    file_path = "verified_question_bank_complete.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return None

df = load_question_bank()

if df is None:
    st.error("Question bank file 'verified_question_bank_complete.csv' not found. Please upload it to the app directory.")
    st.stop()

# Dropdowns for age group and subject
age_group = st.selectbox("Select Age Group", options=[""] + sorted(df['age_group'].dropna().unique().tolist()))
subject = st.selectbox("Select Subject", options=[""] + sorted(df['category'].dropna().unique().tolist()))

# Show buttons only if both selections are made
if age_group and subject:
    col1, col2 = st.columns([1, 1])
    with col1:
        generate = st.button("Generate Questions")
    with col2:
        refresh = st.button("Refresh Questions")

    if generate or refresh:
        filtered_df = df[(df['age_group'] == age_group) & (df['category'] == subject)].reset_index(drop=True)
        if filtered_df.empty:
            st.warning("No questions found for the selected age group and subject.")
        else:
            st.session_state.questions = filtered_df

# Display questions if available
if 'questions' in st.session_state:
    st.subheader("Your Questions")
    for idx, row in st.session_state.questions.iterrows():
        st.markdown(f"**Q{idx+1}. {row['question']}**")
        options = row['options'].split(';')
        st.radio(f"q_{idx}", options, key=f"q_{idx}_radio", label_visibility="collapsed")

