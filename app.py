import os
import re  # NEW
from typing import get_args

import streamlit as st
from dotenv import load_dotenv

# Local modules
from core.types import ModelName
from core.llm import ensure_api_key
from core.pipeline import generate_documented_function, generate_tests

# -----------------------------
# Helpers (filenames)  # NEW
# -----------------------------
def _infer_function_name(code: str) -> str | None:
    """Try to infer the first function name from the code."""
    m = re.search(r"^\s*def\s+([a-zA-Z_]\w*)\s*\(", code, flags=re.MULTILINE)
    return m.group(1) if m else None

def _sanitize_basename(name: str, fallback: str = "generated_function") -> str:
    """Sanitize a string to be used as a safe filename base."""
    if not name:
        name = fallback
    name = name.lower()
    name = re.sub(r"[^a-z0-9_]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name or fallback

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
st.caption("Generate a documented Python function (docstring + type hints) and tests.")

description = st.text_area(
    "Describe the function you want to generate",
    placeholder="Example: 'A function that calculates the median of a list of numbers (handle empty lists and non-numeric values)'",
    height=110,
)

col1, col2, col3 = st.columns([1, 1, 1])
run = col1.button("📘 Generate documented function")
gen_tests_btn = col2.button("✅ Generate tests")
clear = col3.button("🧹 Clear")

# -----------------------------
# Session state
# -----------------------------
if "doc_fn" not in st.session_state:
    st.session_state.doc_fn = ""
if "tests" not in st.session_state:
    st.session_state.tests = ""

if clear:
    st.session_state.doc_fn = ""
    st.session_state.tests = ""
    st.rerun()

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
# Generate documented function
# -----------------------------
if run:
    if not description.strip():
        st.warning("Please write a short description of the function.")
    else:
        with st.spinner("Generating documented function..."):
            st.session_state.doc_fn = generate_documented_function(
                description=description,
                model=model,
                temperature=temperature,
                style_extras="",  # future: toggles for docstring style, etc.
            )
        st.success("Documented function generated.")

# -----------------------------
# Generate tests
# -----------------------------
if gen_tests_btn:
    if not st.session_state.doc_fn.strip():
        st.warning("Generate the documented function first.")
    else:
        with st.spinner(f"Generating {test_framework} tests..."):
            st.session_state.tests = generate_tests(
                documented_code=st.session_state.doc_fn,
                model=model,
                temperature=temperature,
                framework=test_framework,
            )
        st.success("Tests generated.")

# -----------------------------
# Results area (tabs)
# -----------------------------
st.markdown("---")
tabs = st.tabs(["📘 Documented Function", "✅ Tests"])

with tabs[0]:
    if st.session_state.doc_fn:
        st.code(st.session_state.doc_fn, language="python")

        # --- Download documented function (.py)  # NEW
        base = _sanitize_basename(_infer_function_name(st.session_state.doc_fn) or "generated_function")
        st.download_button(
            label="⬇️ Download function (.py)",
            data=st.session_state.doc_fn,
            file_name=f"{base}.py",
            mime="text/x-python",
            use_container_width=True,
        )
    else:
        st.info("No documented function yet. Click '📘 Generate documented function'.")

with tabs[1]:
    if st.session_state.tests:
        st.code(st.session_state.tests, language="python")

        # --- Download tests (.py)  # NEW
        base = _sanitize_basename(_infer_function_name(st.session_state.doc_fn) or "generated_function")
        test_file = f"test_{base}.py" if test_framework == "pytest" else f"tests_{base}.py"
        st.download_button(
            label=f"⬇️ Download {test_framework} tests (.py)",
            data=st.session_state.tests,
            file_name=test_file,
            mime="text/x-python",
            use_container_width=True,
        )
    else:
        st.info(f"No tests yet. Click '✅ Generate tests'.")
