# Excel Insights Chatbot

A natural language chatbot built with Streamlit that allows users to upload Excel files and ask questions about the data — receiving answers in the form of text, tables, or charts.

---

##  Project Objective

To help non-technical users extract insights from Excel sheets simply by asking questions in plain English. This assistant supports:
- Statistical summaries
- Filtered queries
- Grouped comparisons
- Visual insights like bar charts or histograms

---

##  Features

-  Upload `.xlsx` Excel files (single-sheet)
-  Ask natural language questions like:
  - “What is the average sales?”
  - “Show a bar chart of sales by region.”
  - “List all customers from the East region.”
-  Returns:
  - Text answers
  - Data tables
  - Charts (Bar, Histogram)

---

## Tech Stack

- Python 
- [Streamlit](https://streamlit.io/) for web app UI
- Pandas for data manipulation
- Matplotlib & Seaborn for chart generation
- Open-source LLM (no API used, compliant with Neo rules)

---

##  How to Use

1. Go to the [Live App on Streamlit](https://your-streamlit-link.streamlit.app)  <!--  Replace this link when hosted -->
2. Upload a `.xlsx` Excel file (with up to 500 rows and 10–20 columns)
3. Ask your question in plain English
4. View text, table, or chart answers instantly

---

##  Sample Excel Format

| CustomerID | Name       | Age | Sales | Region | Active |
|------------|------------|-----|-------|--------|--------|
| 101        | Akash   | 30  | 1200  | East   | Yes    |
| 102        | Aditya      | 25  | 900   | West   | No     |
| 103        | Rohan | 40  | 1500  | North  | Yes    |

---

##  Project Structure

##  Author

- **Akash Kumar** — AI Engineer  
- GitHub: [@Akash-1301](https://github.com/Akash-1301)

---

##  License

This project is for evaluation purposes under NeoStats' assessment. Do not copy or reuse without permission.
