import logging as log
from typing import Dict

from fameio.source.schema.attribute import AttributeSpecs
from fameio.source.tools import keys_to_lower


class AgentType:
    """Schema definitions for an Agent type"""

    _NO_ATTRIBUTES = "Agent '{}' has no specified 'Attributes'."
    _NO_PRODUCTS = "Agent '{}' has no specified Products."

    _KEY_ATTRIBUTES = "Attributes".lower()
    _KEY_PRODUCTS = "Products".lower()

    def __init__(self, name: str):
        self._name = name
        self._attributes = dict()
        self._products = list()

    @classmethod
    def from_dict(cls, name: str, definitions: dict) -> "AgentType":
        """Loads an agent type `definition` from the given input dict"""
        definition = keys_to_lower(definitions)

        result = cls(name)
        if AgentType._KEY_ATTRIBUTES in definition:
            for attribute_name, attribute_details in definition[
                AgentType._KEY_ATTRIBUTES
            ].items():
                full_name = name + "." + attribute_name
                result._attributes[attribute_name] = AttributeSpecs(
                    full_name, attribute_details
                )
        else:
            log.info(AgentType._NO_ATTRIBUTES.format(name))

        if AgentType._KEY_PRODUCTS in definition:
            products_to_add = definition[AgentType._KEY_PRODUCTS]
            if isinstance(products_to_add, list):
                result._products.extend(products_to_add)
            else:
                result._products.append(products_to_add)
        else:
            log.info(AgentType._NO_PRODUCTS.format(name))

        return result

    @property
    def name(self) -> str:
        """Returns the agent type name"""
        return self._name

    @property
    def products(self) -> list:
        """Returns list of products or an empty list if no products are defined"""
        return self._products

    @property
    def attributes(self) -> Dict[str, AttributeSpecs]:
        """Returns list of Attributes of this agent or an empty list if no attributes are defined"""
        return self._attributes
