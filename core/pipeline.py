from .types import Messages, ModelName
from .llm import gen_response
from .parsing import extract_fenced_code_block

SYSTEM_PROMPT = "You are a senior Python developer. Produce clean, correct, secure code."

def build_initial_messages(description: str, style_extras: str = "") -> Messages:
    """Build messages to generate the initial function from a user description.

    Args:
        description (str): User description of the function to generate.
        style_extras (str): Extra style instructions (optional).        
    """    
    user_prompt = (
        f"Write a self-contained Python function that {description}. "
        "Use clear variable names and follow PEP 8. "
        "Include a comprehensive Google-style docstring (sections: Args, Returns, Raises, Examples) "
        "and add Python type hints for all parameters and the return type. "
        "Do not include comments outside the docstring. "
        f"{style_extras} "
        "Output only the function in a ```python code block```."
    )    
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def generate_documented_function(
    description: str,
    model: ModelName,
    temperature: float = 0.2,
    style_extras: str = "",
) -> str:
    """Return the documented function code as plain Python (no backticks)."""
    messages = build_initial_messages(description, style_extras=style_extras)
    response = gen_response(messages, model_name=model, max_tokens=1200, temperature=temperature)
    return extract_fenced_code_block(response)

def generate_tests(documented_code: str, model: ModelName, temperature: float = 0.2, framework: str = "unittest") -> str:
    raise NotImplementedError