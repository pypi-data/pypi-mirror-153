from typing import List

from fameio.source.scenario.agent import Agent
from fameio.source.scenario.contract import Contract
from fameio.source.scenario.exception import get_or_default, get_or_raise
from fameio.source.scenario.fameiofactory import FameIOFactory
from fameio.source.scenario.generalproperties import GeneralProperties
from fameio.source.schema.schema import Schema
from fameio.source.tools import keys_to_lower


class Scenario:
    """Definition of a scenario"""

    _KEY_SCHEMA = "Schema".lower()
    _KEY_GENERAL = "GeneralProperties".lower()
    _KEY_AGENTS = "Agents".lower()
    _KEY_CONTRACTS = "Contracts".lower()

    _MISSING_KEY = "Scenario definition misses required key '{}'."

    def __init__(self, schema: Schema, general_props: GeneralProperties) -> None:
        self._schema = schema
        self._general_props = general_props
        self._agents = []
        self._contracts = []

    @classmethod
    def from_dict(cls, definitions: dict, factory=FameIOFactory()) -> "Scenario":
        """Parse scenario from provided `definitions` using given `factory`"""
        definitions = keys_to_lower(definitions)

        schema = factory.new_schema_from_dict(
            get_or_raise(definitions, Scenario._KEY_SCHEMA, Scenario._MISSING_KEY)
        )
        general_props = factory.new_general_properties_from_dict(
            get_or_raise(definitions, Scenario._KEY_GENERAL, Scenario._MISSING_KEY)
        )
        result = cls(schema, general_props)

        for agent_definition in get_or_default(definitions, Scenario._KEY_AGENTS, []):
            result.add_agent(factory.new_agent_from_dict(agent_definition))

        for multi_definition in get_or_default(
            definitions, Scenario._KEY_CONTRACTS, []
        ):
            for single_contract_definition in Contract.split_contract_definitions(
                multi_definition
            ):
                result.add_contract(
                    factory.new_contract_from_dict(single_contract_definition)
                )

        return result

    def to_dict(self) -> dict:
        """Serializes the scenario content to a dict"""
        result = {
            Scenario._KEY_GENERAL: self.general_properties.to_dict(),
            Scenario._KEY_SCHEMA: self.schema.to_dict(),
            Scenario._KEY_AGENTS: [],
        }
        for agent in self.agents:
            result[Scenario._KEY_AGENTS].append(agent.to_dict())
        result[Scenario._KEY_CONTRACTS] = []
        for contract in self.contracts:
            result[Scenario._KEY_CONTRACTS].append(contract.to_dict())
        return result

    @property
    def agents(self) -> List[Agent]:
        """Returns all the agents of this scenario as a list"""
        return self._agents

    def add_agent(self, agent: Agent) -> None:
        """Adds a new agent to this scenario"""
        self._agents.append(agent)

    @property
    def contracts(self) -> List[Contract]:
        """Returns all the contracts of this scenario as a list"""
        return self._contracts

    def add_contract(self, contract: Contract) -> None:
        """Adds a new contract to this scenario"""
        self._contracts.append(contract)

    @property
    def schema(self) -> Schema:
        """Returns Schema associated with this scenario"""
        return self._schema

    @property
    def general_properties(self) -> GeneralProperties:
        """Returns General properties of this scenario"""
        return self._general_props
