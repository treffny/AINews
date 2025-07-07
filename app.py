import streamlit as st

st.set_page_config(layout="wide")

st.title("Daily AI News")

with open("daily_ai_news_report.md", "r") as f:
    report_content = f.read()

st.markdown(report_content)


