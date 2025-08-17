import streamlit as st

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="PyFunc Generator", page_icon="🐍", layout="wide")

# -----------------------------
# Sidebar (options)
# -----------------------------
st.sidebar.header("⚙️ Options")

# Dictionary with model cost info
model_cost_info = {
    "gpt-3.5-turbo": "💲 Cheapest (good for basic tasks)",
    "o3-mini": "💲 Low cost, better than 3.5",
    "gpt-4o-mini": "💲💲 Mid-tier, faster and accurate",
    "gpt-4o": "💲💲💲 Highest quality, most expensive"
}

# Dropdown ordered from cheaper → expensive
model = st.sidebar.selectbox(
    "Model",
    list(model_cost_info.keys()),
    index=0
)

# Show cost info dynamically
st.sidebar.caption(model_cost_info[model])

temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.2, 0.05)

test_framework = st.sidebar.selectbox(
    "Test framework",
    ["unittest", "pytest"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("Models ordered from cheaper → more expensive")

# -----------------------------
# Main content
# -----------------------------
st.title("🐍 PyFunc Generator")
st.caption("Mini-agent that generates Python functions with documentation and tests.")

# Function description input
description = st.text_area(
    "Describe the function you want to generate",
    placeholder="Example: 'A function that calculates the median of a list of numbers'",
    height=100
)

col1, col2 = st.columns([1, 1])
run = col1.button("🚀 Generate")
clear = col2.button("🧹 Clear")

# -----------------------------
# Results area (tabs)
# -----------------------------
st.markdown("---")
tabs = st.tabs(["🔧 Initial Function", "📘 Documented Function", "✅ Tests"])

with tabs[0]:
    st.info("No results yet. Generate a function to see the output here.")
with tabs[1]:
    st.info("No results yet. Documentation will appear here.")
with tabs[2]:
    st.info("No results yet. Tests will appear here.")
