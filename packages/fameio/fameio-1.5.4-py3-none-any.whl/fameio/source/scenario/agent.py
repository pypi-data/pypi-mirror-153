from typing import Any, Dict

from fameio.source.scenario.attribute import Attribute
from fameio.source.scenario.exception import (
    assert_or_raise,
    get_or_default,
    get_or_raise,
)
from fameio.source.tools import keys_to_lower


class Agent:
    """Contains specifications for an agent in a scenario"""

    _KEY_TYPE = "Type".lower()
    _KEY_ID = "Id".lower()
    _KEY_ATTRIBUTES = "Attributes".lower()

    _MISSING_KEY = "Agent requires `key` '{}' but is missing it."
    _MISSING_TYPE = "Agent requires `type` but is missing it."
    _MISSING_ID = "Agent requires a positive integer `id` but was '{}'."
    _DOUBLE_ATTRIBUTE = (
        "Cannot add attribute '{}' to agent {} because it already exists."
    )

    def __init__(self, agent_id: int, type_name: str) -> None:
        """Constructs a new Agent"""
        assert_or_raise(
            type(agent_id) is int and agent_id >= 0, self._MISSING_ID.format(agent_id)
        )
        assert_or_raise(type_name and len(type_name.strip()) > 0, self._MISSING_TYPE)
        self._id = agent_id
        self._type_name = type_name.strip()
        self._attributes = dict()

    @classmethod
    def from_dict(cls, definitions: dict) -> "Agent":
        """Parses an agent from provided `definitions`"""
        definitions = keys_to_lower(definitions)
        agent_type = get_or_raise(definitions, Agent._KEY_TYPE, Agent._MISSING_KEY)
        agent_id = get_or_raise(definitions, Agent._KEY_ID, Agent._MISSING_KEY)
        result = cls(agent_id, agent_type)
        attribute_definitions = get_or_default(
            definitions, Agent._KEY_ATTRIBUTES, dict()
        )
        result.__init_attributes_from_dict(attribute_definitions)
        return result

    def to_dict(self) -> dict:
        """Serializes the Agent content to a dict"""
        result = dict()

        result[Agent._KEY_TYPE] = self.type_name
        result[Agent._KEY_ID] = self.id

        if len(self.attributes) > 0:
            attributes_dict = dict()
            for attr_name, attr_value in self.attributes.items():
                attributes_dict[attr_name] = attr_value.generic_content
            result[self._KEY_ATTRIBUTES] = attributes_dict

        return result

    def _notify_data_changed(self):
        """Placeholder method used to signal data changes to derived types"""
        pass

    @property
    def id(self) -> int:
        """Returns the ID of the Agent"""
        return self._id

    @property
    def display_id(self) -> str:
        """Returns the ID of the Agent as a string for display purposes"""
        return "#{}".format(self._id)

    @property
    def type_name(self) -> str:
        """Returns the name of the Agent type"""
        return self._type_name

    @property
    def attributes(self) -> Dict[str, Attribute]:
        """Returns dictionary of all Attributes of this agent"""
        return self._attributes

    def add_attribute(self, name: str, value: Attribute):
        """Adds a new attribute to the Agent (raise an error if it already exists)"""
        if name in self._attributes:
            raise ValueError(self._DOUBLE_ATTRIBUTE.format(name, self.display_id))
        self._attributes[name] = value
        self._notify_data_changed()

    def __init_attributes_from_dict(self, attributes: Dict[str, Any]) -> None:
        """Initialize Agent `attributes` from dict; Must only be called when creating a new Agent"""
        assert len(self._attributes) == 0
        self._attributes = {}
        for name, value in attributes.items():
            full_name = str(self.type_name) + "(" + str(self.id) + "): " + name
            self.add_attribute(name, Attribute(full_name, value))
