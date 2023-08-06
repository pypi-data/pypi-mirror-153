import logging as log

from fameio.source.logs import log_error_and_raise


def log_and_raise(message: str):
    """Raises ScenarioException with given `message`"""
    log_error_and_raise(ScenarioException(message))


def get_or_raise(dictionary: dict, key: str, message: str):
    """Returns value associated with `key` in given `dictionary`, or raises ScenarioException if key is missing"""
    if key not in dictionary or dictionary[key] is None:
        log_error_and_raise(ScenarioException(message.format(key)))
    else:
        return dictionary[key]


def assert_or_raise(assertion: bool, message: str):
    """Raises ScenarioException with given `message` if `assertion` is `False`"""
    if not assertion:
        log_error_and_raise(ScenarioException(message))


def get_or_default(dictionary: dict, key: str, default_value):
    """Returns value associated with `key` in given `dictionary`, or the given `default_value` if key is missing"""
    if key in dictionary and dictionary[key] is not None:
        return dictionary[key]
    else:
        log.debug(
            "Using default value '{}' for missing key '{}'".format(default_value, key)
        )
        return default_value


class ScenarioException(Exception):
    """Indicates an error while parsing a scenario or one of its components"""

    pass
