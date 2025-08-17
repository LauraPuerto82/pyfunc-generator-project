# PyFunc Generator (mini-agent) 🐍

Generate **Python functions** from a natural language description, and
return: 1) initial function, 2) documented function (docstrings + type
hints), 3) **tests** (unittest/pytest).

**Stack:** Streamlit + LiteLLM (OpenAI)\
**Status:** MVP in progress (initial commit with minimal UI).

## What does this project showcase?

-   **Applied LLM app** with a prompt pipeline (function → documentation
    → tests).
-   Best practices: type hints, PEP8 style, separated tests, secrets
    management.
-   Simple and usable UI, ideal for portfolio demonstration.

## How to run locally

``` bash
# activate venv (already created)
# Windows (PowerShell)
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

# Add your API key (not pushed to repo)
mkdir -p .streamlit
# create .streamlit/secrets.toml with:
# OPENAI_API_KEY = "your_api_key"

streamlit run app.py
```

## Roadmap

-   [ ] MVP: pipeline function → doc → tests
-   [ ] Selector unittest/pytest
-   [ ] File download (.py)
-   [ ] Syntax validation (AST) without execution
-   [ ] Docstring styles (Google/NumPy)
-   [ ] Deploy on Streamlit Cloud + README with screenshots

## License

MIT
