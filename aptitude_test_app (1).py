import pandas as pd
import streamlit as st

# Title of the app
st.title("Aptitude Test Generator")

# File uploader for user to upload their own question bank
uploaded_file = st.file_uploader("Upload your question bank (CSV format)", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file into a DataFrame
        question_bank = pd.read_csv(uploaded_file)

        # Display the first few rows of the uploaded question bank
        st.subheader("Preview of Uploaded Question Bank")
        st.dataframe(question_bank.head())

        # Display basic stats
        st.write(f"Total questions uploaded: {len(question_bank)}")
        st.write("Available age groups:", question_bank['age_group'].unique())
        st.write("Available categories:", question_bank['category'].unique())

        # Additional logic for test generation can be added here

    except Exception as e:
        st.error(f"Error reading the uploaded file: {e}")
else:
    st.info("Please upload a CSV file to begin.")

