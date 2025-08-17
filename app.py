import os
from typing import get_args

import streamlit as st
from dotenv import load_dotenv  # NEW: allow local .env usage

# Local modules
from core.types import ModelName
from core.llm import ensure_api_key
from core.pipeline import generate_initial_function

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="PyFunc Generator", page_icon="🐍", layout="wide")

# -----------------------------
# Sidebar (options)
# -----------------------------
st.sidebar.header("⚙️ Options")

# Take model options from the ModelName Literal (keeps things in sync)
model_options = list(get_args(ModelName))

# Ordered from cheaper → more expensive (adjust texts if you change models)
model_cost_info = {
    "gpt-3.5-turbo": "💲 Cheapest (good for basic tasks)",
    "o3-mini": "💲 Low cost, better than 3.5",
    "gpt-4o-mini": "💲💲 Mid-tier, faster and accurate",
    "gpt-4o": "💲💲💲 Highest quality, most expensive",
}

model: ModelName = st.sidebar.selectbox("Model", model_options, index=0)  # type: ignore[assignment]
st.sidebar.caption(model_cost_info.get(model, ""))

temperature: float = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.2, 0.05)
test_framework = st.sidebar.selectbox("Test framework", ["unittest", "pytest"], index=0)

st.sidebar.markdown("---")
st.sidebar.caption("Models ordered from cheaper → more expensive")

# -----------------------------
# Main content
# -----------------------------
st.title("🐍 PyFunc Generator")
st.caption("Mini-agent that generates Python functions with documentation and tests.")

description = st.text_area(
    "Describe the function you want to generate",
    placeholder="Example: 'A function that calculates the median of a list of numbers (handle empty lists and non-numeric values)'",
    height=110,
)

col1, col2 = st.columns([1, 1])
run = col1.button("🚀 Generate")
clear = col2.button("🧹 Clear")

# -----------------------------
# Session state
# -----------------------------
if "initial_fn" not in st.session_state:
    st.session_state.initial_fn = ""
if "doc_fn" not in st.session_state:
    st.session_state.doc_fn = ""
if "tests" not in st.session_state:
    st.session_state.tests = ""

if clear:
    st.session_state.initial_fn = ""
    st.session_state.doc_fn = ""
    st.session_state.tests = ""
    st.experimental_rerun()

# -----------------------------
# API key setup: .env (local) → env var → st.secrets (Cloud)
# -----------------------------
def get_openai_api_key() -> str | None:
    # 1) Load .env if present (local dev)
    load_dotenv()
    # 2) Try environment variable
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    # 3) Try Streamlit secrets (Cloud)
    try:
        return st.secrets["OPENAI_API_KEY"]  # raises if not configured
    except Exception:
        return None

OPENAI_API_KEY = get_openai_api_key()
try:
    ensure_api_key(OPENAI_API_KEY)
except Exception:
    st.error(
        "Missing OpenAI API key. Set it in a local `.env` (OPENAI_API_KEY=...) "
        "or in Streamlit Cloud → App → Settings → Secrets."
    )
    st.stop()

# -----------------------------
# Generate (initial function only for now)
# -----------------------------
if run:
    if not description.strip():
        st.warning("Please write a short description of the function.")
    else:
        with st.spinner("Generating initial function..."):
            st.session_state.initial_fn = generate_initial_function(
                description=description,
                model=model,
                temperature=temperature,
                style_extras="",  # future: toggles for type hints / docstring style
            )

# -----------------------------
# Results area (tabs)
# -----------------------------
st.markdown("---")
tabs = st.tabs(["🔧 Initial Function", "📘 Documented Function", "✅ Tests"])

with tabs[0]:
    if st.session_state.initial_fn:
        st.code(st.session_state.initial_fn, language="python")
    else:
        st.info("No results yet. Generate a function to see the output here.")

with tabs[1]:
    st.info("Coming next: documented function (docstrings, type hints, examples).")

with tabs[2]:
    st.info(f"Coming next: {test_framework} tests for the generated function.")
