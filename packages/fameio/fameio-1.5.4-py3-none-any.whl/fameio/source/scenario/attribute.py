import logging as log
from typing import Any, Dict, List

from fameio.source.scenario.exception import log_and_raise


class Attribute:
    """An Attribute of an agent in a scenario"""

    _VALUE_MISSING = "Value not specified for Attribute '{}' - leave out if default shall be used (if defined)."
    _OVERWRITE = (
        "Value already defined for Attribute '{}' - overwriting value with new one!"
    )
    _LIST_EMPTY = "Attribute '{}' was assigned an empty list - please remove or fill empty assignments."
    _DICT_EMPTY = "Attribute '{}' was assigned an empty dictionary - please remove or fill empty assignments."
    _MIXED_DATA = "Attribute '{}' was assigned a list with mixed complex and simple entries - please fix."

    def __init__(self, name: str, definitions) -> None:
        """Parses an Attribute's definition"""
        self._full_name = name

        if definitions is None:
            log_and_raise(Attribute._VALUE_MISSING.format(name))

        if isinstance(definitions, dict):
            self._value = None
            self._nested_list = None
            self._nested = Attribute._build_attribute_dict(name, definitions)
        elif Attribute._is_list_of_dict(name, definitions):
            self._nested = None
            self._value = None
            self._nested_list = list()
            for entry in definitions:
                self._nested_list.append(Attribute._build_attribute_dict(name, entry))
        else:
            self._nested = None
            self._nested_list = None
            self._value = definitions

    @staticmethod
    def _build_attribute_dict(
        name: str, definitions: Dict[str, Any]
    ) -> Dict[str, "Attribute"]:
        """Returns a new dictionary containing Attributes generated from given `definitions`"""
        if not definitions:
            log_and_raise(Attribute._DICT_EMPTY.format(name))

        dictionary = dict()
        for nested_name, value in definitions.items():
            full_name = name + "." + nested_name
            if nested_name in dictionary:
                log.warning(Attribute._OVERWRITE.format(full_name))
            dictionary[nested_name] = Attribute(full_name, value)
        return dictionary

    @staticmethod
    def _is_list_of_dict(name: str, definitions: Any) -> bool:
        """Returns True if given `definitions` is a list of dict"""
        if isinstance(definitions, list):
            if not definitions:
                log_and_raise(Attribute._LIST_EMPTY.format(name))

            all_dicts = no_dicts = True
            for item in definitions:
                if not isinstance(item, dict):
                    all_dicts = False
                else:
                    no_dicts = False
            if (not all_dicts) and (not no_dicts):
                log_and_raise(Attribute._MIXED_DATA.format(name))
            return all_dicts
        return False

    @property
    def generic_content(self) -> Any:
        """Returns the full content of the attribute (and its children) as a generic value"""
        if self.has_value:
            return self.value
        elif self.has_nested_list:
            result = []
            for attr_dict in self.nested_list:
                sub_dict = {}
                for name, attr in attr_dict.items():
                    sub_dict[name] = attr.generic_content
                result.append(sub_dict)
            return result
        elif self.has_nested:
            result = {}
            for name, attr in self.nested.items():
                result[name] = attr.generic_content
            return result
        else:
            log_and_raise(Attribute._VALUE_MISSING.format(self._full_name))

    @property
    def has_value(self) -> bool:
        """Returns True if Attribute has any value assigned"""
        return self._value is not None

    @property
    def value(self) -> Any:
        return self._value

    @property
    def has_nested(self) -> bool:
        """Returns True if nested Attributes are present"""
        return bool(self._nested)

    @property
    def nested(self) -> Dict[str, "Attribute"]:
        """Returns dictionary of all nested Attributes"""
        assert self.has_nested
        return self._nested

    def get_nested_by_name(self, key: str) -> "Attribute":
        """Returns nested Attribute by specified name"""
        return self._nested[key]

    @property
    def has_nested_list(self) -> bool:
        """Returns True if list of nested items is present"""
        return bool(self._nested_list)

    @property
    def nested_list(self) -> List[Dict[str, "Attribute"]]:
        """Return list of all nested Attribute dictionaries"""
        assert self.has_nested_list
        return self._nested_list

    def __repr__(self) -> str:
        return self._full_name
