import streamlit as st
import pandas as pd
import random

st.title("Aptitude Test Generator")

# File uploader for the question bank
uploaded_file = st.file_uploader("Upload your question bank CSV", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Dropdowns for age group and subject
        age_group = st.selectbox("Select Age Group", options=[""] + sorted(df['age_group'].unique().tolist()))
        subject = st.selectbox("Select Subject", options=[""] + sorted(df['category'].unique().tolist()))

        if age_group and subject:
            # Filter questions
            filtered_df = df[(df['age_group'] == age_group) & (df['category'] == subject)]

            if 'questions' not in st.session_state or st.button("Refresh Questions"):
                st.session_state.questions = filtered_df.sample(n=min(10, len(filtered_df))).reset_index(drop=True)

            if st.button("Generate Questions") or 'questions' in st.session_state:
                if 'questions' not in st.session_state:
                    st.session_state.questions = filtered_df.sample(n=min(10, len(filtered_df))).reset_index(drop=True)

                for idx, row in st.session_state.questions.iterrows():
                    st.markdown(f"**Q{idx+1}. {row['question']}**")
                    options = row['options'].split(';')
                    st.radio(f"Options for Q{idx+1}", options, key=f"q_{idx}")
        else:
            st.info("Please select both age group and subject to generate questions.")
    except Exception as e:
        st.error(f"Error reading the uploaded file: {e}")
else:
    st.warning("Please upload the question bank CSV file to begin.")

