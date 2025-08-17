import re

def infer_function_name(code: str) -> str | None:
    """Return the first function name found in the code, or None."""
    m = re.search(r"^\s*def\s+([a-zA-Z_]\w*)\s*\(", code, flags=re.MULTILINE)
    return m.group(1) if m else None

def sanitize_basename(name: str, fallback: str = "generated_function") -> str:
    """Sanitize a string for safe filenames (lowercase, underscores)."""
    if not name:
        name = fallback
    name = name.lower()
    name = re.sub(r"[^a-z0-9_]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name or fallback

