from typing import Dict

from fameio.source.logs import log_error_and_raise
from fameio.source.schema.agenttype import AgentType
from fameio.source.schema.exception import SchemaException
from fameio.source.tools import keys_to_lower


class Schema:
    """Definition of a schema"""

    _AGENT_TYPES_MISSING = "Keyword AgentTypes not found in Schema."
    _KEY_AGENT_TYPE = "AgentTypes".lower()

    def __init__(self, definitions: dict):
        # the current Schema class design is read-only, so it's much simpler to remember the original schema dict
        # in order to implement to_dict()
        self._original_input_dict = definitions

        # fill the agent types
        self._agent_types = dict()
        for agent_type_name, agent_definition in definitions[
            Schema._KEY_AGENT_TYPE
        ].items():
            agent_type = AgentType.from_dict(agent_type_name, agent_definition)
            self._agent_types[agent_type_name] = agent_type

    @classmethod
    def from_dict(cls, definitions: dict) -> "Schema":
        """Load definitions from given `schema`"""
        definitions = keys_to_lower(definitions)
        if Schema._KEY_AGENT_TYPE not in definitions:
            log_error_and_raise(SchemaException(Schema._AGENT_TYPES_MISSING))
        return cls(definitions)

    def to_dict(self) -> dict:
        """Serializes the schema content to a dict"""
        return self._original_input_dict

    @property
    def agent_types(self) -> Dict[str, AgentType]:
        """Returns all the agent types by their name"""
        return self._agent_types
