import datetime

def clean_text(text: str) -> str:
    """
    Basic text cleaning: strip whitespace and lowercase.

    Parameters
    ----------
    text : str
        Input text

    Returns
    -------
    str
        Cleaned text
    """
    return text.strip().lower()

def format_timestamp(ts: datetime.datetime) -> str:
    """
    Format datetime into ISO string.

    Parameters
    ----------
    ts : datetime.datetime
        Datetime object

    Returns
    -------
    str
        ISO formatted string
    """
    return ts.isoformat()
