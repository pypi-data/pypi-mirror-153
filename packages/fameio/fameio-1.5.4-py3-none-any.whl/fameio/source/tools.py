from typing import Any, Dict


def keys_to_lower(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    """Returns new dictionary content of given `dictionary` but its `keys` in lower case"""
    return {keys.lower(): value for keys, value in dictionary.items()}


def ensure_is_list(value: Any) -> list:
    """Returns a list: Either the provided `value` if it is a list, or a new list containing the provided value"""
    if isinstance(value, list):
        return value
    else:
        return [value]
