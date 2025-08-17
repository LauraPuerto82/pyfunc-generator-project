# PyFunc Generator (mini-agent) 🐍

Generate **Python functions** from a natural language description, and
return: 1) documented function (docstrings + type hints), 2) **tests**
(unittest/pytest).

**Stack:** Streamlit + LiteLLM (OpenAI)\
**Status:** MVP in progress (UI working, function + docstrings).

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

## API Key configuration

-   **Local:** create a `.env` file with:

        OPENAI_API_KEY=your_api_key

    (this file is ignored by git and not pushed to repo).

-   **Cloud (Streamlit):** configure the key in `Settings → Secrets`
    (TOML format).

The code automatically detects if it's running locally or in the cloud.

## Roadmap

-   [ ] MVP: pipeline function → doc → tests
-   [ ] Selector unittest/pytest
-   [ ] File download (.py)
-   [ ] Syntax validation (AST) without execution
-   [ ] Docstring styles (Google/NumPy)
-   [ ] Deploy on Streamlit Cloud + README with screenshots

## License

MIT
