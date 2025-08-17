import re
import ast 

FENCED_CODE_BLOCK_RE = re.compile(r"```(?:python)?\s*([\s\S]*?)```", re.IGNORECASE)

def extract_fenced_code_block(text: str) -> str:
    """Extract the first triple-backtick code block; fallback to trimmed raw text."""
    if not text:
        return ""
    match = FENCED_CODE_BLOCK_RE.search(text)
    return match.group(1).strip() if match else text.strip()

def check_syntax(py_code: str) -> tuple[bool, str]:
    """Return (ok, error_message). ok=True if the code parses; does not execute anything."""
    try:
        # Try to parse the code using Python's Abstract Syntax Tree (AST) module
        ast.parse(py_code)
        return True, ""
    except SyntaxError as e:
        # If parsing fails, include details about line and column to help the user
        msg = f"{e.msg} (line {e.lineno}, col {e.offset})"
        return False, msg

