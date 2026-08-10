# Security helper foundation

def sanitize_input(text: str) -> str:
    """Sanitizes raw string inputs."""
    if not text:
        return ""
    return text.strip()
