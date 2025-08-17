import re

FENCED_CODE_BLOCK_RE = re.compile(r"```(?:python)?\s*([\s\S]*?)```", re.IGNORECASE)

def extract_fenced_code_block(text: str) -> str:
    """Extract the first triple-backtick code block; fallback to trimmed raw text."""
    if not text:
        return ""
    match = FENCED_CODE_BLOCK_RE.search(text)
    return match.group(1).strip() if match else text.strip()

