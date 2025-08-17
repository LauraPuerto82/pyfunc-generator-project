import os
from dotenv import load_dotenv
import streamlit as st

def get_openai_api_key() -> str | None:
    """Load API key from .env (local), env var, or Streamlit secrets (Cloud)."""
    load_dotenv()  # local dev
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    try:
        return st.secrets["OPENAI_API_KEY"]  # Cloud
    except Exception:
        return None
