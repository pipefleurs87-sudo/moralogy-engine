import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide")

html_path = Path("ui/index.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

st.components.v1.html(
    html,
    height=900,
    scrolling=True
)
