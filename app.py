import streamlit as st

st.set_page_config(layout="wide")

with open("daily_ai_news_report.md", "r") as f:
    report_content = f.read()

st.markdown(report_content)