def validate_payload(data: dict, required_keys: list) -> bool:
    """
    Validate that required keys exist in a payload.

    Parameters
    ----------
    data : dict
        Input JSON payload
    required_keys : list
        Keys that must be present

    Returns
    -------
    bool
        True if valid, False otherwise
    """
    return all(key in data for key in required_keys)
