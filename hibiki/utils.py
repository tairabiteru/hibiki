import typing as t

def replace_all(
        text: str,
        matching_chars: t.Union[str, t.List[str]],
        replacing_char: str
    ) -> str:
    """Replace all instances of matching chars with replacing chars."""
    if not isinstance(matching_chars, list):
        matching_chars = list(matching_chars)
    
    for i in range(0, len(matching_chars)):
        text = text.replace(matching_chars[i], replacing_char)
    return text