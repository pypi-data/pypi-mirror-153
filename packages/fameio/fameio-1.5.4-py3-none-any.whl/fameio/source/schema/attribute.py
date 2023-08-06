import logging as log
import typing
from enum import Enum, auto
from typing import Any, Dict, List

from fameio.source.schema.exception import SchemaException
from fameio.source.time import FameTime
from fameio.source.tools import keys_to_lower


class AttributeType(Enum):
    """Specifies known types that Attributes can take"""

    INTEGER = auto()
    DOUBLE = auto()
    LONG = auto()
    TIME_STAMP = auto()
    STRING = auto()
    ENUM = auto()
    TIME_SERIES = auto()
    BLOCK = auto()

    def convert_string_to_type(self, value: str):
        """Converts a given string to this AttributeType's data format"""
        if self is AttributeType.INTEGER or self is AttributeType.LONG:
            return int(value)
        elif self is AttributeType.DOUBLE:
            return float(value)
        elif self is AttributeType.TIME_STAMP:
            return FameTime.convert_string_if_is_datetime(value)
        elif self is AttributeType.ENUM or self is AttributeType.STRING:
            return str(value)
        elif self is AttributeType.TIME_SERIES:
            return float(value)
        else:
            raise ValueError("String conversion not supported for '{}'.".format(self))


class AttributeSpecs:
    """Schema Definition of a single Attribute (with possible inner Attributes) of an agent"""

    _MISSING_SPEC_DEFAULT = (
        "Missing '{}' specification for Attribute '{}' - assuming {}."
    )
    _MISSING_TYPE = "'AttributeType' not declare for Attribute '{}'."
    _INVALID_TYPE = "'{}' is not a valid type for an Attribute."
    _DEFAULT_NOT_LIST = "Attribute is list, but provided Default '{}' is not a list."
    _DEFAULT_INCOMPATIBLE = "Default '{}' can not be converted to AttributeType '{}'."
    _DEFAULT_DISALLOWED = "Default '{}' is not an allowed value."
    _LIST_DISALLOWED = "Attribute '{}' of type TIME_SERIES cannot be list."

    _KEY_MANDATORY = "Mandatory".lower()
    _KEY_LIST = "List".lower()
    _KEY_TYPE = "AttributeType".lower()
    _KEY_NESTED = "NestedAttributes".lower()
    _KEY_VALUES = "Values".lower()
    _KEY_DEFAULT = "Default".lower()

    def __init__(self, name: str, definition: dict):
        """Loads Attribute from given `definition`"""
        self._full_name = name
        definition = keys_to_lower(definition)

        if AttributeSpecs._KEY_MANDATORY in definition:
            self._is_mandatory = definition[AttributeSpecs._KEY_MANDATORY]
        else:
            self._is_mandatory = True
            log.warning(
                AttributeSpecs._MISSING_SPEC_DEFAULT.format(
                    AttributeSpecs._KEY_MANDATORY, name, True
                )
            )

        if AttributeSpecs._KEY_LIST in definition:
            self._is_list = definition[AttributeSpecs._KEY_LIST]
        else:
            self._is_list = False
            log.warning(
                AttributeSpecs._MISSING_SPEC_DEFAULT.format(
                    AttributeSpecs._KEY_LIST, name, False
                )
            )

        if AttributeSpecs._KEY_TYPE in definition:
            self._attr_type = AttributeSpecs._get_type_for_name(
                definition[AttributeSpecs._KEY_TYPE]
            )
        else:
            log.error(AttributeSpecs._MISSING_TYPE.format(name))
            raise SchemaException(AttributeSpecs._MISSING_TYPE.format(name))

        if self._attr_type == AttributeType.TIME_SERIES and self._is_list:
            raise SchemaException(AttributeSpecs._LIST_DISALLOWED.format(name))

        self._values = list()
        if AttributeSpecs._KEY_VALUES in definition:
            self._values = definition[AttributeSpecs._KEY_VALUES]

        self._default_value = None
        if AttributeSpecs._KEY_DEFAULT in definition:
            provided_value = definition[AttributeSpecs._KEY_DEFAULT]
            if self._is_list:
                self._default_value = self._convert_list(provided_value)
            else:
                self._default_value = self._convert_to_data_type(provided_value)

        self._nested_attributes = dict()
        if AttributeSpecs._KEY_NESTED in definition:
            for nested_name, nested_details in definition[
                AttributeSpecs._KEY_NESTED
            ].items():
                full_name = name + "." + nested_name
                self._nested_attributes[nested_name] = AttributeSpecs(
                    full_name, nested_details
                )

    def _convert_list(self, values) -> list:
        """Converts all entries in given `values` list to this attribute data type and returns this new list"""
        if isinstance(values, list):
            return [self._convert_to_data_type(item) for item in values]
        else:
            raise SchemaException(AttributeSpecs._DEFAULT_NOT_LIST.format(values))

    def _convert_to_data_type(self, value: str):
        """Converts a given single `value` to this Attribute's data type"""
        try:
            converted = self._attr_type.convert_string_to_type(value)
            if self._values and converted not in self._values:
                raise SchemaException(AttributeSpecs._DEFAULT_DISALLOWED.format(value))
            return converted
        except ValueError:
            raise SchemaException(
                AttributeSpecs._DEFAULT_INCOMPATIBLE.format(value, self._attr_type)
            )

    @property
    def attr_type(self) -> AttributeType:
        """Returns AttributeType of this attribute"""
        return self._attr_type

    @property
    def values(self) -> Any:
        """Returns the values of this attribute (single value or list).

        If is_list == False, a single value is expected.
        If is_list == True, a single value or a list of values can be returned.
        """
        return self._values

    @property
    def is_list(self) -> bool:
        """Return True if this attribute type is a list"""
        return self._is_list

    @property
    def has_nested_attributes(self) -> bool:
        """Returns True if nested attributes are defined"""
        return bool(self._nested_attributes)

    @property
    def nested_attributes(self) -> Dict[str, "AttributeSpecs"]:
        """Returns list of nested Attributes of this Attribute or an empty dict if no nested attributes are defined"""
        return self._nested_attributes

    @property
    def has_default_value(self) -> bool:
        """Return True if a default value is available"""
        return self._default_value is not None

    @property
    def default_value(self) -> typing.Optional[typing.Any]:
        """Return the default value of this attribute, if any"""
        return self._default_value

    @property
    def is_mandatory(self) -> bool:
        """Return True if this attribute is mandatory"""
        return self._is_mandatory

    @property
    def full_name(self) -> str:
        """Returns name including name of enclosing parent attributes"""
        return self._full_name

    @staticmethod
    def _get_type_for_name(name: str) -> "AttributeType":
        """Returns the AttributeType matching the given `name` converted to upper case"""
        try:
            return AttributeType[name.upper()]
        except KeyError:
            raise SchemaException(AttributeSpecs._INVALID_TYPE.format(name))
