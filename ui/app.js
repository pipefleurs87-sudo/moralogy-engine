import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide")

html = Path("ui/index.html").read_text(encoding="utf-8")

st.components.v1.html(html, height=900, scrolling=True)
