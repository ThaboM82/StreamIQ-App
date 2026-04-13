def validate_language(lang: str) -> bool:
    """Validate that the selected language is supported."""
    supported = ["English", "isiZulu", "Sepedi", "Xitsonga"]
    return lang in supported

def validate_non_empty(text: str) -> bool:
    """Ensure text input is not empty or just whitespace."""
    return bool(text and text.strip())

def validate_domain(domain: str) -> bool:
    """Validate that the selected domain is supported."""
    supported = ["Banking", "Insurance", "CallCenter"]
    return domain in supported
