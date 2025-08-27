import os
from litellm import completion
from .types import Messages, ModelName

def ensure_api_key(api_key: str | None) -> None:
    """Ensure GEMINI_API_KEY is present in environment for LiteLLM."""
    if not api_key:
        raise ValueError(
            "Missing API key. Add it to `.streamlit/secrets.toml` as "
            'GEMINI_API_KEY = "your_key" or set the GEMINI_API_KEY env var.'
        )
    os.environ["GEMINI_API_KEY"] = api_key

def gen_response(
    messages: Messages,
    model_name: ModelName,
    max_tokens: int = 1200,
    temperature: float = 0.2,
) -> str:
    """Call the selected model via LiteLLM and return the assistant content."""
    resp = completion(
        model=model_name,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content
