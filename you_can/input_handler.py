def sanitize(text: str) -> str:
    return " ".join(text.split()).strip()


def get_user_input(prompt: str = "") -> str:
    try:
        raw = input(prompt)
        cleaned = sanitize(raw)
        return cleaned
    except EOFError:
        return ""
