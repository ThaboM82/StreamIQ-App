# src/utils/validators.py
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

# -------------------------------
# Supported Values
# -------------------------------
SUPPORTED_LANGUAGES = ["English", "isiZulu", "Sepedi", "Xitsonga"]
SUPPORTED_DOMAINS = ["Banking", "Insurance", "CallCenter"]
SUPPORTED_THEMES = ["light", "dark"]
SUPPORTED_SIDEBAR_STATES = ["expanded", "collapsed"]
SUPPORTED_PAGES = [
    "Home",
    "Pipeline",
    "Call Center Results",
    "Insurance Claims Results",
    "Multilingual Processor",
    "Mock Data Demo",
    "NLP Demo",
    "Logs",
    "History",
    "Download Center",
    "Audit Trail",
    "Settings",
    "About"
]

# -------------------------------
# Generic Validator
# -------------------------------
def validate_choice(value: str, supported_list: list) -> bool:
    return value in supported_list

# -------------------------------
# Specific Validators
# -------------------------------
def validate_language(lang: str) -> bool:
    return validate_choice(lang, SUPPORTED_LANGUAGES)

def validate_non_empty(text: str) -> bool:
    return bool(text and text.strip())

def validate_domain(domain: str) -> bool:
    return validate_choice(domain, SUPPORTED_DOMAINS)

def validate_theme(theme: str) -> bool:
    return validate_choice(theme, SUPPORTED_THEMES)

def validate_sidebar_state(state: str) -> bool:
    return validate_choice(state, SUPPORTED_SIDEBAR_STATES)

def validate_page(page: str) -> bool:
    return validate_choice(page, SUPPORTED_PAGES)

# -------------------------------
# Supported Options Helper
# -------------------------------
def get_supported_options() -> dict:
    return {
        "languages": SUPPORTED_LANGUAGES,
        "domains": SUPPORTED_DOMAINS,
        "themes": SUPPORTED_THEMES,
        "sidebar_states": SUPPORTED_SIDEBAR_STATES,
        "pages": SUPPORTED_PAGES,
    }

# -------------------------------
# Module Load Confirmation
# -------------------------------
from src.utils.branding import cli_confirm
cli_confirm("Validators module loaded")
