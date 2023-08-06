import logging as log
from collections import Counter
from typing import Any, Dict, List

from fameio.source.logs import log_error_and_raise
from fameio.source.scenario import Agent, Attribute, Contract, Scenario
from fameio.source.schema.agenttype import AgentType
from fameio.source.schema.attribute import AttributeSpecs, AttributeType
from fameio.source.schema.schema import Schema
from fameio.source.time import FameTime


class ValidationException(Exception):
    """Indicates an error occurred during validation of any data with a connected schema"""

    pass


class SchemaValidator:
    """Handles validation of scenarios based on a connected `schema`"""

    _AGENT_ID_NOT_UNIQUE = "Agent ID(s) not unique: '{}'."
    _AGENT_TYPE_UNKNOWN = "Agent type '{}' not declared in Schema."
    _ATTRIBUTE_UNKNOWN = "Attribute '{}' not declared in Schema."
    _TYPE_NOT_IMPLEMENTED = "Validation not implemented for AttributeType '{}'."
    _INCOMPATIBLE = "Value '{}' incompatible with {} of Attribute '{}'."
    _DISALLOWED = "Value '{}' not in list of allowed values of Attribute '{}'"
    _AGENT_MISSING = "Contract mentions Agent with ID '{}' but Agent was not declared."
    _PRODUCT_MISSING = "Product '{}' not declared in Schema for AgentType '{}'."
    _KEY_MISSING = "Required key '{}' missing in dictionary '{}'."
    _ATTRIBUTE_MISSING = "Mandatory attribute '{}' is missing."
    _DEFAULT_IGNORED = "Optional Attribute: '{}': not specified - provided Default ignored for optional Attributes."
    _OPTIONAL_MISSING = "Optional Attribute: '{}': not specified."
    _IS_NO_LIST = "Attribute '{}' is list but assigned value '{}' is not a list."

    @staticmethod
    def _ensure_mandatory_present(
        attributes: Dict[str, Attribute], specifications: Dict[str, AttributeSpecs]
    ) -> None:
        """
        Raises Exception if in given list of `specifications` at least one item is mandatory,
        provides no defaults and is not contained in given `attributes` dictionary
        """
        for name, specification in specifications.items():
            if name not in attributes:
                if specification.is_mandatory:
                    if not specification.has_default_value:
                        log_error_and_raise(
                            ValidationException(
                                SchemaValidator._ATTRIBUTE_MISSING.format(name)
                            )
                        )
                else:
                    if specification.has_default_value:
                        log.warning(SchemaValidator._DEFAULT_IGNORED.format(name))
                    else:
                        log.info(SchemaValidator._OPTIONAL_MISSING.format(name))
            if name in attributes and specification.has_nested_attributes:
                attribute = attributes[name]
                if specification.is_list:
                    for entry in attribute.nested_list:
                        SchemaValidator._ensure_mandatory_present(
                            entry, specification.nested_attributes
                        )
                else:
                    SchemaValidator._ensure_mandatory_present(
                        attribute.nested, specification.nested_attributes
                    )

    @staticmethod
    def _get_agent(schema: Schema, name: str) -> AgentType:
        """Returns agent specified by `name` or raises Exception if this agent is not present in given `schema`"""
        if name in schema.agent_types:
            return schema.agent_types[name]
        else:
            log_error_and_raise(
                ValidationException(SchemaValidator._AGENT_TYPE_UNKNOWN.format(name))
            )

    @staticmethod
    def ensure_is_valid_agent(agent: Agent, schema: Schema) -> None:
        """Raises an exception if given `agent` does not meet the specified `schema` requirements"""
        scenario_attributes = agent.attributes
        schema_attributes = SchemaValidator._get_agent(
            schema, agent.type_name
        ).attributes
        SchemaValidator._ensure_mandatory_present(
            scenario_attributes, schema_attributes
        )
        SchemaValidator._ensure_attributes_exist(scenario_attributes, schema_attributes)
        SchemaValidator._ensure_value_matches_type(
            scenario_attributes, schema_attributes
        )

    @staticmethod
    def _ensure_attributes_exist(
        attributes: Dict[str, Attribute], specifications: Dict[str, AttributeSpecs]
    ) -> None:
        """Raises exception any entry of given `attributes` has no corresponding type `specification`"""
        for name, attribute in attributes.items():
            if name not in specifications:
                log_error_and_raise(
                    ValidationException(
                        SchemaValidator._ATTRIBUTE_UNKNOWN.format(attribute)
                    )
                )
            if attribute.has_nested:
                specification = specifications[name]
                SchemaValidator._ensure_attributes_exist(
                    attribute.nested, specification.nested_attributes
                )
            if attribute.has_nested_list:
                specification = specifications[name]
                for entry in attribute.nested_list:
                    SchemaValidator._ensure_attributes_exist(
                        entry, specification.nested_attributes
                    )

    @staticmethod
    def _ensure_value_matches_type(
        attributes: Dict[str, Attribute], specifications: Dict[str, AttributeSpecs]
    ) -> None:
        """Raises exception if in given list of `attributes` its value does not match associated type `specification`"""
        for name, attribute in attributes.items():
            specification = specifications[name]
            if attribute.has_value:
                value = attribute.value
                type_spec = specification.attr_type
                if not SchemaValidator._is_compatible(specification, value):
                    message = SchemaValidator._INCOMPATIBLE.format(
                        value, type_spec, specification.full_name
                    )
                    log_error_and_raise(ValidationException(message))
                if not SchemaValidator._is_allowed_value(specification, value):
                    log_error_and_raise(
                        ValidationException(
                            SchemaValidator._DISALLOWED.format(
                                value, specification.full_name
                            )
                        )
                    )
            if attribute.has_nested:
                SchemaValidator._ensure_value_matches_type(
                    attribute.nested, specification.nested_attributes
                )
            if attribute.has_nested_list:
                for entry in attribute.nested_list:
                    SchemaValidator._ensure_value_matches_type(
                        entry, specification.nested_attributes
                    )

    @staticmethod
    def _is_compatible(specification: AttributeSpecs, value_or_values: Any) -> bool:
        """Returns True if given `value_or_values` is compatible to specified `attribute_type` and `should_be_list`"""
        is_list = isinstance(value_or_values, list)
        attribute_type = specification.attr_type
        if specification.is_list:
            if not is_list:
                log.warning(
                    SchemaValidator._IS_NO_LIST.format(
                        specification.full_name, value_or_values
                    )
                )
                return SchemaValidator._is_compatible_value(
                    attribute_type, value_or_values
                )
            for value in value_or_values:
                if not SchemaValidator._is_compatible_value(attribute_type, value):
                    return False
            return True
        else:
            return (not is_list) and SchemaValidator._is_compatible_value(
                attribute_type, value_or_values
            )

    @staticmethod
    def _is_compatible_value(attribute_type: AttributeType, value) -> bool:
        """Returns True if given single value is compatible to specified `attribute_type`"""
        if attribute_type is AttributeType.INTEGER:
            if isinstance(value, int):
                return -2147483648 < value < 2147483647
            return False
        if attribute_type is AttributeType.LONG:
            return isinstance(value, int)
        elif attribute_type is AttributeType.DOUBLE:
            return isinstance(value, (int, float))
        elif attribute_type in (AttributeType.ENUM, AttributeType.STRING):
            return isinstance(value, str)
        elif attribute_type is AttributeType.TIME_STAMP:
            return FameTime.is_fame_time_compatible(value)
        elif attribute_type is AttributeType.TIME_SERIES:
            return isinstance(value, (str, int, float))
        else:
            log_error_and_raise(
                ValidationException(
                    SchemaValidator._TYPE_NOT_IMPLEMENTED.format(attribute_type)
                )
            )

    @staticmethod
    def _is_allowed_value(attribute: AttributeSpecs, value) -> bool:
        """Returns True if `value` matches an entry of given `Attribute`'s value list or if this list is empty"""
        if not attribute.values:
            return True
        else:
            return value in attribute.values

    @staticmethod
    def ensure_is_valid_contract(
        contract: Contract, schema: Schema, agent_types_by_id: Dict[int, str]
    ) -> None:
        """Raises exception if given `contract` does not meet the `schema`'s requirements, using `agent_types_by_id`"""
        sender_id = contract.sender_id
        if sender_id not in agent_types_by_id:
            log_error_and_raise(
                ValidationException(SchemaValidator._AGENT_MISSING.format(sender_id))
            )
        if contract.receiver_id not in agent_types_by_id:
            log_error_and_raise(
                ValidationException(
                    SchemaValidator._AGENT_MISSING.format(contract.receiver_id)
                )
            )
        sender_type_name = agent_types_by_id[sender_id]
        if sender_type_name not in schema.agent_types:
            log_error_and_raise(
                ValidationException(
                    SchemaValidator._AGENT_TYPE_UNKNOWN.format(sender_type_name)
                )
            )
        sender_type = schema.agent_types[sender_type_name]
        product = contract.product_name
        if product not in sender_type.products:
            log_error_and_raise(
                ValidationException(
                    SchemaValidator._PRODUCT_MISSING.format(product, sender_type_name)
                )
            )

    @staticmethod
    def ensure_unique_agent_ids(agents: List[Agent]) -> None:
        """Raises exception if any id for given `agents` is not unique"""
        list_of_ids = [agent.id for agent in agents]
        non_unique_ids = [
            agent_id for agent_id, count in Counter(list_of_ids).items() if count > 1
        ]
        if non_unique_ids:
            log_error_and_raise(
                ValidationException(
                    SchemaValidator._AGENT_ID_NOT_UNIQUE.format(non_unique_ids)
                )
            )

    @staticmethod
    def ensure_agent_type_in_schema(agent: Agent, schema: Schema) -> None:
        """Raises exception if type for given `agent` is not specified in given `schema`"""
        if agent.type_name not in schema.agent_types:
            log_error_and_raise(
                ValidationException(
                    SchemaValidator._AGENT_TYPE_UNKNOWN.format(agent.type_name)
                )
            )

    @staticmethod
    def ensure_is_valid_scenario(scenario: Scenario) -> None:
        """Raises exception if given `scenario` does not meet its own schema requirements"""
        schema = scenario.schema
        agents = scenario.agents

        SchemaValidator.ensure_unique_agent_ids(agents)
        for agent in agents:
            SchemaValidator.ensure_agent_type_in_schema(agent, schema)
            SchemaValidator.ensure_is_valid_agent(agent, schema)

        agent_types_by_id = {agent.id: agent.type_name for agent in agents}
        for contract in scenario.contracts:
            SchemaValidator.ensure_is_valid_contract(
                contract, schema, agent_types_by_id
            )
