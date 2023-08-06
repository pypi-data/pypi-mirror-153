from fameio.source.schema.schema import Schema
from fameio.source.scenario.generalproperties import GeneralProperties
from fameio.source.scenario.agent import Agent
from fameio.source.scenario.contract import Contract


class FameIOFactory:
    """Factory used to instantiate the types defined in a scenario file.
    This allows a client to subclass some types in order to extend what a scenario can contain.
    """

    @staticmethod
    def new_schema_from_dict(definitions: dict) -> Schema:
        """Constructs a new Schema from provided `definitions`"""
        return Schema.from_dict(definitions)

    @staticmethod
    def new_general_properties_from_dict(definitions: dict) -> GeneralProperties:
        """Constructs a new GeneralProperties instance from provided `definitions`"""
        return GeneralProperties.from_dict(definitions)

    @staticmethod
    def new_agent_from_dict(definitions: dict) -> Agent:
        """Constructs a new Agent from provided `definitions`"""
        return Agent.from_dict(definitions)

    @staticmethod
    def new_contract_from_dict(definitions: dict) -> Contract:
        """Constructs a new Contract from provided `definitions`"""
        return Contract.from_dict(definitions)
