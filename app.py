import streamlit as st

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="PyFunc Generator", page_icon="🐍", layout="wide")

# -----------------------------
# Main title
# -----------------------------
st.title("🐍 PyFunc Generator")

# -----------------------------
# Subtitle / short description
# -----------------------------
st.caption("Mini-agent that generates Python functions with documentation and tests.")

# -----------------------------
# Placeholder info box
# -----------------------------
st.info(
    "This is the initial version (MVP scaffold). "
    "In the next steps, we will add the LLM pipeline to generate functions, documentation, and tests."
)
