import logging as log
from typing import Any, Dict, List, Optional

from fameio.source.scenario.attribute import Attribute
from fameio.source.scenario.exception import get_or_default, get_or_raise, log_and_raise
from fameio.source.time import FameTime
from fameio.source.tools import ensure_is_list, keys_to_lower


class Contract:
    """Contract between two Agents of a scenario"""

    _KEY_SENDER = "SenderId".lower()
    _KEY_RECEIVER = "ReceiverId".lower()
    _KEY_PRODUCT = "ProductName".lower()
    _KEY_FIRST_DELIVERY = "FirstDeliveryTime".lower()
    _KEY_INTERVAL = "DeliveryIntervalInSteps".lower()
    _KEY_EXPIRE = "ExpirationTime".lower()
    _KEY_ATTRIBUTES = "Attributes".lower()

    _MISSING_KEY = "Contract requires key '{}' but is missing it."
    _MULTI_CONTRACT_CORRUPT = (
        "Definition of Contracts is valid only for One-to-One, One-to-many, Many-to-one, "
        "or N-to-N sender-to-receiver numbers. Found M-to-N pairing in Contract with "
        "Senders: {} and Receivers: {}."
    )
    _NEGATIVE_INTERVAL = (
        "Contract delivery interval must be a positive integer but was: {}"
    )
    _SENDER_IS_RECEIVER = "Contract sender and receiver have the same id: {}"
    _DOUBLE_ATTRIBUTE = (
        "Cannot add attribute '{}' to contract because it already exists."
    )

    def __init__(
        self,
        sender_id: int,
        receiver_id: int,
        product_name: str,
        delivery_interval: int,
        first_delivery_time: int,
        expiration_time: Optional[int] = None,
    ):
        """Constructs a new Contract"""
        assert product_name != ""
        if sender_id == receiver_id:
            log.warning(self._SENDER_IS_RECEIVER.format(sender_id))
        if delivery_interval < 0:
            raise ValueError(self._NEGATIVE_INTERVAL.format(delivery_interval))
        self._sender_id = sender_id
        self._receiver_id = receiver_id
        self._product_name = product_name
        self._delivery_interval = delivery_interval
        self._first_delivery_time = first_delivery_time
        self._expiration_time = expiration_time
        self._attributes = dict()

    def _notify_data_changed(self):
        """Placeholder method used to signal data changes to derived types"""
        pass

    @property
    def product_name(self) -> str:
        """Returns the product name of the contract"""
        return self._product_name

    @property
    def sender_id(self) -> int:
        """Returns the sender ID of the contract"""
        return self._sender_id

    @property
    def display_sender_id(self) -> str:
        """Returns the sender ID of the contract as a string for display purposes"""
        return "#{}".format(self._sender_id)

    @property
    def receiver_id(self) -> int:
        """Returns the receiver ID of the contract"""
        return self._receiver_id

    @property
    def display_receiver_id(self) -> str:
        """Returns the receiver ID of the contract as a string for display purposes"""
        return "#{}".format(self._receiver_id)

    @property
    def delivery_interval(self) -> int:
        """Returns the delivery interval of the contract (in steps)"""
        return self._delivery_interval

    @property
    def first_delivery_time(self) -> int:
        """Returns the first delivery time of the contract"""
        return self._first_delivery_time

    @property
    def expiration_time(self) -> Optional[int]:
        """Returns the expiration time of the contract if available, None otherwise"""
        return self._expiration_time

    @property
    def attributes(self) -> Dict[str, Attribute]:
        """Returns dictionary of all Attributes of the contract"""
        return self._attributes

    def add_attribute(self, name: str, value: Attribute):
        """Adds a new attribute to the Contract (raise an error if it already exists)"""
        if name in self._attributes:
            raise ValueError(self._DOUBLE_ATTRIBUTE.format(name))
        self._attributes[name] = value
        self._notify_data_changed()

    def __init_attributes_from_dict(self, attributes: Dict[str, Any]) -> None:
        """Resets Contract `attributes` from dict; Must only be called when creating a new Contract"""
        assert len(self._attributes) == 0
        self._attributes = {}
        for name, value in attributes.items():
            full_name = str(type) + "." + str(id) + name
            self.add_attribute(name, Attribute(full_name, value))

    @classmethod
    def from_dict(cls, definitions: dict) -> "Contract":
        """Parses Contract from given `definitions`"""
        definitions = keys_to_lower(definitions)
        sender_id = get_or_raise(
            definitions, Contract._KEY_SENDER, Contract._MISSING_KEY
        )
        receiver_id = get_or_raise(
            definitions, Contract._KEY_RECEIVER, Contract._MISSING_KEY
        )
        product_name = get_or_raise(
            definitions, Contract._KEY_PRODUCT, Contract._MISSING_KEY
        )
        first_delivery_time = FameTime.convert_string_if_is_datetime(
            get_or_raise(
                definitions, Contract._KEY_FIRST_DELIVERY, Contract._MISSING_KEY
            )
        )
        delivery_interval = get_or_raise(
            definitions, Contract._KEY_INTERVAL, Contract._MISSING_KEY
        )
        expiration_time = get_or_default(definitions, Contract._KEY_EXPIRE, None)
        expiration_time = (
            FameTime.convert_string_if_is_datetime(expiration_time)
            if expiration_time
            else None
        )
        result = cls(
            sender_id,
            receiver_id,
            product_name,
            delivery_interval,
            first_delivery_time,
            expiration_time,
        )
        attribute_definitions = get_or_default(
            definitions, Contract._KEY_ATTRIBUTES, dict()
        )
        result.__init_attributes_from_dict(attribute_definitions)
        return result

    def to_dict(self) -> dict:
        """Serializes the Contract content to a dict"""
        result = dict()
        result[self._KEY_SENDER] = self.sender_id
        result[self._KEY_RECEIVER] = self.receiver_id
        result[self._KEY_PRODUCT] = self.product_name
        result[self._KEY_FIRST_DELIVERY] = self.first_delivery_time
        result[self._KEY_INTERVAL] = self.delivery_interval

        if self.expiration_time is not None:
            result[self._KEY_EXPIRE] = self.expiration_time

        if len(self.attributes) > 0:
            attributes_dict = dict()
            for attr_name, attr_value in self.attributes.items():
                attributes_dict[attr_name] = attr_value.generic_content
            result[self._KEY_ATTRIBUTES] = attributes_dict

        return result

    @staticmethod
    def split_contract_definitions(multi_definition: dict) -> List[dict]:
        """Splits given `multi_definition` dictionary into list of individual Contract definitions"""
        contracts = list()
        base_data = dict()
        multi_definition = keys_to_lower(multi_definition)
        for key in [
            Contract._KEY_PRODUCT,
            Contract._KEY_FIRST_DELIVERY,
            Contract._KEY_FIRST_DELIVERY,
            Contract._KEY_INTERVAL,
            Contract._KEY_EXPIRE,
            Contract._KEY_ATTRIBUTES,
        ]:
            if key in multi_definition:
                base_data[key] = multi_definition[key]
        senders = ensure_is_list(
            get_or_raise(multi_definition, Contract._KEY_SENDER, Contract._MISSING_KEY)
        )
        receivers = ensure_is_list(
            get_or_raise(
                multi_definition, Contract._KEY_RECEIVER, Contract._MISSING_KEY
            )
        )
        if len(senders) > 1 and len(receivers) == 1:
            for index in range(len(senders)):
                contracts.append(
                    Contract._copy_contract(senders[index], receivers[0], base_data)
                )
        elif len(senders) == 1 and len(receivers) > 1:
            for index in range(len(receivers)):
                contracts.append(
                    Contract._copy_contract(senders[0], receivers[index], base_data)
                )
        elif len(senders) == len(receivers):
            for index in range(len(senders)):
                contracts.append(
                    Contract._copy_contract(senders[index], receivers[index], base_data)
                )
        else:
            log_and_raise(Contract._MULTI_CONTRACT_CORRUPT.format(senders, receivers))
        return contracts

    @staticmethod
    def _copy_contract(sender: int, receiver: int, base_data: dict) -> dict:
        """Returns a new contract definition dictionary, with given `sender` and `receiver` and copied `base_data`"""
        contract = dict()
        contract[Contract._KEY_SENDER] = sender
        contract[Contract._KEY_RECEIVER] = receiver
        contract.update(base_data)
        return contract
