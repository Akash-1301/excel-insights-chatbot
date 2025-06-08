# app.py

import streamlit as st
import pandas as pd
from llm_utils import process_query
import os

st.set_page_config(page_title="NeoStats Excel Chatbot", layout="wide")

st.title("NeoStats Excel Insights Chatbot")
st.write("Upload an Excel file and ask questions in plain English.")

# Create charts folder if missing
if not os.path.exists("charts"):
    os.makedirs("charts")

uploaded_file = st.file_uploader("Upload your Excel (.xlsx) file here", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("File loaded successfully!")
        st.write("### Preview of your data:")
        st.dataframe(df.head(10))

        st.write("---")
        user_question = st.text_input("Ask your question:", "")

        if user_question:
            response = process_query(df, user_question)

            # If response is a path to a PNG chart, display the image
            if isinstance(response, str) and response.endswith(".png"):
                st.image(response)
            # If response is a list of dicts (filtered rows), show as a table
            elif isinstance(response, list):
                st.write("Filtered rows:")
                st.dataframe(pd.DataFrame(response))
            else:
                st.write("Answer:")
                st.write(response)

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
else:
    st.info("Please upload an Excel file to begin.")
