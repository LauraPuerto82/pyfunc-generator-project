from .types import Messages, ModelName, TestFramework, DocstringStyle
from .llm import gen_response
from .parsing import extract_fenced_code_block

SYSTEM_PROMPT = "You are a senior Python developer. Produce clean, correct, secure code."


def build_initial_messages(
    description: str,
    style: DocstringStyle = "google",
    style_extras: str = "",
    add_type_hints: bool = True,
) -> Messages:
    """Build messages to generate a documented function from a description."""
    style_line = (
        "Use Google-style docstrings (sections: Args, Returns, Raises, Examples)."
        if style == "google"
        else "Use NumPy-style docstrings (Parameters, Returns, Raises, Examples)."
    )
    hints_line = "Add Python type hints for all parameters and the return type. " if add_type_hints else ""

    user_prompt = (
        f"Write a self-contained Python function that {description}. "
        "Use clear variable names and follow PEP 8. "
        f"{style_line} {hints_line}"
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
    docstring_style: DocstringStyle = "google",
    add_type_hints: bool = True,
) -> str:
    """Generate a documented function (docstring + optional type hints) from the description."""
    messages = build_initial_messages(
        description=description,
        style=docstring_style,
        style_extras=style_extras,
        add_type_hints=add_type_hints,
    )
    response = gen_response(messages, model_name=model, max_tokens=1200, temperature=temperature)
    return extract_fenced_code_block(response)


def generate_tests(
    documented_code: str,
    model: ModelName,
    temperature: float = 0.2,
    framework: TestFramework = "unittest",
) -> str:
    """
    Generate unit tests for the documented function provided.
    The function code is passed as context to avoid drift. The function itself must NOT be rewritten.
    """
    if framework == "unittest":
        guidance = (
            "Use Python's built-in unittest framework. "
            "Create a TestCase class with multiple test methods. "
            "Cover: basic cases, edge cases, invalid inputs, and exceptions. "
            "Include a main guard to run the tests: if __name__ == '__main__': unittest.main(). "
        )
    else:  # framework == "pytest"
        guidance = (
            "Use pytest-style tests (simple functions starting with 'test_'). "
            "Cover: basic cases, edge cases, invalid inputs, and exceptions. "
            "Use pytest.raises for exception assertions. "
        )

    messages: Messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": f"```python\n{documented_code}\n```"},
        {
            "role": "user",
            "content": (
                "Write comprehensive unit tests for the function shown above. "
                "Do NOT modify or reprint the original function — only produce the tests. "
                f"{guidance}"
                "Assume the function is importable from the same package/module. "
                "Output only the tests in a ```python code block```."
            ),
        },
    ]
    response = gen_response(messages, model_name=model, max_tokens=1400, temperature=temperature)
    return extract_fenced_code_block(response)
