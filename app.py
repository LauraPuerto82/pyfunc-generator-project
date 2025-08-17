from typing import get_args
import streamlit as st

# Local modules
from core.types import ModelName, DocstringStyle
from core.llm import ensure_api_key
from core.pipeline import generate_documented_function, generate_tests
from core.parsing import check_syntax
from core.secrets import get_openai_api_key
from core.filenames import infer_function_name, sanitize_basename

st.set_page_config(page_title="PyFunc Generator", page_icon="🐍", layout="wide")

# ---------- Small helpers ----------
def init_state() -> None:
    st.session_state.setdefault("doc_fn", "")
    st.session_state.setdefault("doc_fn_ok", None)
    st.session_state.setdefault("doc_fn_err", "")
    st.session_state.setdefault("tests", "")
    st.session_state.setdefault("tests_ok", None)
    st.session_state.setdefault("tests_err", "")

def clear_state() -> None:
    for k in ("doc_fn", "doc_fn_err", "tests", "tests_err"):
        st.session_state[k] = ""
    st.session_state["doc_fn_ok"] = None
    st.session_state["tests_ok"] = None
    st.rerun()

def render_sidebar() -> tuple[ModelName, float, str, DocstringStyle]:  # ⬅️ typed return
    st.sidebar.header("⚙️ Options")
    model_options = list(get_args(ModelName))
    model_cost_info = {
        "gpt-3.5-turbo": "💲 Cheapest (good for basic tasks)",
        "o3-mini": "💲 Low cost, better than 3.5",
        "gpt-4o-mini": "💲💲 Mid-tier, faster and accurate",
        "gpt-4o": "💲💲💲 Highest quality, most expensive",
    }
    model: ModelName = st.sidebar.selectbox("Model", model_options, index=0)  # type: ignore[assignment]
    st.sidebar.caption(model_cost_info.get(model, ""))

    temperature: float = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.2, 0.05)
    framework: str = st.sidebar.selectbox("Test framework", ["unittest", "pytest"], index=0)

    # Docstring style selector (typed)
    doc_style_label = st.sidebar.selectbox("Docstring style", ["Google", "NumPy"], index=0)
    docstring_style: DocstringStyle = "google" if doc_style_label == "Google" else "numpy"  # ⬅️ typed

    st.sidebar.markdown("---")
    st.sidebar.caption("Models ordered from cheaper → more expensive")
    return model, temperature, framework, docstring_style

def generate_doc_fn(
    description: str,
    model: ModelName,
    temperature: float,
    docstring_style: DocstringStyle,  # ⬅️ typed
) -> None:
    with st.spinner("Generating documented function..."):
        st.session_state.doc_fn = generate_documented_function(
            description=description,
            model=model,
            temperature=temperature,
            style_extras="",
            docstring_style=docstring_style,  # ⬅️ typed style flows through
            add_type_hints=True,
        )
    ok, err = check_syntax(st.session_state.doc_fn)
    st.session_state.doc_fn_ok, st.session_state.doc_fn_err = ok, err
    (st.success if ok else st.error)(
        "Documented function generated. ✓ Syntax OK" if ok else f"Generated function has syntax errors: {err}"
    )

def generate_tests_fn(model: ModelName, temperature: float, framework: str) -> None:
    with st.spinner(f"Generating {framework} tests..."):
        st.session_state.tests = generate_tests(
            documented_code=st.session_state.doc_fn, model=model, temperature=temperature, framework=framework
        )
    ok, err = check_syntax(st.session_state.tests)
    st.session_state.tests_ok, st.session_state.tests_err = ok, err
    (st.success if ok else st.error)(
        "Tests generated. ✓ Syntax OK" if ok else f"Generated tests have syntax errors: {err}"
    )

def render_code_tab(code: str, ok, err, download_label: str, filename_builder) -> None:
    if ok is True:
        st.caption("✅ Syntax: OK")
    elif ok is False:
        st.caption(f"❌ Syntax error: {err}")
    st.code(code, language="python")
    fname = filename_builder(code)
    st.download_button(
        label=download_label, data=code, file_name=fname, mime="text/x-python",
        use_container_width=True, disabled=(ok is False),
    )

# ---------- Init + API key ----------
init_state()
OPENAI_API_KEY = get_openai_api_key()
try:
    ensure_api_key(OPENAI_API_KEY)
except Exception:
    st.error("Missing OpenAI API key. Set it in a local `.env` (OPENAI_API_KEY=...) "
             "or in Streamlit Cloud → App → Settings → Secrets.")
    st.stop()

# ---------- Sidebar / Main ----------
model, temperature, test_framework, docstring_style = render_sidebar()

st.title("🐍 PyFunc Generator")
st.caption("Generate a documented Python function (docstring + type hints) and tests.")

description = st.text_area(
    "Describe the function you want to generate",
    placeholder="Example: 'A function that calculates the median of a list of numbers (handle empty lists and non-numeric values)'",
    height=110,
)

col1, col2, col3 = st.columns([1, 1, 1])
if col1.button("📘 Generate documented function"):
    if not description.strip():
        st.warning("Please write a short description of the function.")
    else:
        generate_doc_fn(description, model, temperature, docstring_style)

if col2.button("✅ Generate tests"):
    if not st.session_state.doc_fn.strip():
        st.warning("Generate the documented function first.")
    else:
        generate_tests_fn(model, temperature, test_framework)

if col3.button("🧹 Clear"):
    clear_state()

# ---------- Results ----------
st.markdown("---")
tabs = st.tabs(["📘 Documented Function", "✅ Tests"])

with tabs[0]:
    if st.session_state.doc_fn:
        def _fname_func(code: str) -> str:
            base = sanitize_basename(infer_function_name(code) or "generated_function")
            return f"{base}.py"
        render_code_tab(
            st.session_state.doc_fn,
            st.session_state.doc_fn_ok,
            st.session_state.doc_fn_err,
            "⬇️ Download function (.py)",
            _fname_func,
        )
    else:
        st.info("No documented function yet. Click '📘 Generate documented function'.")

with tabs[1]:
    if st.session_state.tests:
        def _test_fname(_: str) -> str:
            base = sanitize_basename(infer_function_name(st.session_state.doc_fn) or "generated_function")
            return f"test_{base}.py" if test_framework == "pytest" else f"tests_{base}.py"
        render_code_tab(
            st.session_state.tests,
            st.session_state.tests_ok,
            st.session_state.tests_err,
            f"⬇️ Download {test_framework} tests (.py)",
            _test_fname,
        )
    else:
        st.info("No tests yet. Click '✅ Generate tests'.")
