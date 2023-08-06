import logging as log
import os.path
import pathlib as pt
from typing import Any, Dict

import pandas as pd
from fameio.source.logs import log_error_and_raise
from fameio.source.scenario import (
    Agent,
    Attribute,
    Contract,
    GeneralProperties,
    Scenario,
)
from fameio.source.path_resolver import PathResolver
from fameio.source.schema.attribute import AttributeSpecs, AttributeType
from fameio.source.series import TimeSeriesManager
from fameio.source.time import START_IN_REAL_TIME, ConversionException, FameTime
from fameio.source.tools import ensure_is_list
from fameprotobuf import DataStorage_pb2


class ProtoWriterException(Exception):
    """Indicates an error during writing of protobuffer file"""

    pass


class ProtoWriter:
    """Writes a given scenario to protobuffer file"""

    _TYPE_NOT_IMPLEMENTED = "AttributeType '{}' not implemented."
    _NOT_TIME_SERIES = "Cannot convert value '{}' to TimeSeries."
    _CONTRACT_UNSUPPORTED = (
        "Unsupported value for Contract Attribute '{}'; "
        "Only support `int`, `float`, `enum` or `dict` types are supported here."
    )
    _USING_DEFAULT = "Using provided Default for Attribute: '{}'."
    _CORRUPT_TIME_SERIES_VALUE = "TimeSeries file '{}' is corrupt: At least one entry in value column is not numeric."
    _CORRUPT_TIME_SERIES_KEY = "TimeSeries file '{}' is corrupt: At least one entry in first column is not a timestamp."
    _TIMESERIES_FILE_NOT_FOUND = "Cannot find TimeSeries file '{}'."

    def __init__(self, file_path: str, path_resolver=PathResolver()) -> None:
        self.file_path = file_path
        self.time_series_manager = TimeSeriesManager()
        self._path_resolver = path_resolver

    def write_validated_scenario(self, scenario: Scenario) -> None:
        """Writes given validated Scenario to file"""
        log.info("Writing scenario to protobuf file `{}`".format(self.file_path))
        pb_data_storage = DataStorage_pb2.DataStorage()
        pb_input = pb_data_storage.input

        log.info("Adding General Properties")
        ProtoWriter._set_general_properties(pb_input, scenario.general_properties)

        log.info("Adding Agents")
        schema = scenario.schema
        for agent in scenario.agents:
            pb_agent = ProtoWriter._set_agent(pb_input.agent.add(), agent)
            attribute_specs = schema.agent_types[agent.type_name].attributes
            self._set_attributes(pb_agent, agent.attributes, attribute_specs)

        log.info("Adding Contracts")
        for contract in scenario.contracts:
            pb_contract = ProtoWriter._set_contract(pb_input.contract.add(), contract)
            ProtoWriter._set_contract_attributes(pb_contract, contract.attributes)

        log.info("Adding TimeSeries")
        self._set_time_series(pb_input)
        log.info("Writing to disk")
        self._write_protobuf_to_disk(pb_data_storage)

    @staticmethod
    def _set_general_properties(pb_input, gen_props: GeneralProperties) -> None:
        """Saves Scenario's general properties to specified protobuffer `pb_input` container"""
        pb_input.runId = gen_props.run_id
        pb_input.simulation.startTime = gen_props.simulation_start_time
        pb_input.simulation.stopTime = gen_props.simulation_stop_time
        pb_input.simulation.randomSeed = gen_props.simulation_random_seed
        pb_input.output.interval = gen_props.output_interval
        pb_input.output.process = gen_props.output_process

    @staticmethod
    def _set_agent(pb_agent, agent: Agent):
        """Saves type and id of given `agent` to protobuffer `pb_agent` container. Returns given `pb_agent`."""
        pb_agent.className = agent.type_name
        pb_agent.id = agent.id
        return pb_agent

    def _set_attributes(
        self,
        pb_parent,
        attributes: Dict[str, Attribute],
        specs: Dict[str, AttributeSpecs],
    ) -> None:
        """Assigns `attributes` to protobuffer fields of given `pb_parent` - cascades for nested Attributes"""
        values_not_set = [key for key in specs.keys()]
        for name, attribute in attributes.items():
            pb_field = ProtoWriter._add_field(pb_parent, name)
            attribute_specs = specs[name]
            values_not_set.remove(name)
            attribute_type = attribute_specs.attr_type
            if attribute_type is AttributeType.BLOCK:
                if attribute_specs.is_list:
                    for index, entry in enumerate(attribute.nested_list):
                        pb_inner = ProtoWriter._add_field(pb_field, str(index))
                        self._set_attributes(
                            pb_inner, entry, attribute_specs.nested_attributes
                        )
                else:
                    self._set_attributes(
                        pb_field,
                        attribute.nested,
                        attribute_specs.nested_attributes,
                    )
            else:
                self._set_attribute(pb_field, attribute.value, attribute_type)
        for name in values_not_set:
            attribute_specs = specs[name]
            if attribute_specs.is_mandatory:
                pb_field = ProtoWriter._add_field(pb_parent, name)
                self._set_attribute(
                    pb_field, attribute_specs.default_value, attribute_specs.attr_type
                )
                log.info(ProtoWriter._USING_DEFAULT.format(name))

    @staticmethod
    def _add_field(pb_parent, name: str) -> Any:
        """Returns new field with given `name` that is added to given `pb_parent`"""
        pb_field = pb_parent.field.add()
        pb_field.fieldName = name
        return pb_field

    def _set_attribute(self, pb_field, value, attribute_type: AttributeType) -> None:
        """Sets given `value` to given protobuffer `pb_field` depending on specified `attribute_type`"""
        if attribute_type is AttributeType.INTEGER:
            pb_field.intValue.extend(ensure_is_list(value))
        elif attribute_type is AttributeType.DOUBLE:
            pb_field.doubleValue.extend(ensure_is_list(value))
        elif attribute_type is AttributeType.LONG:
            pb_field.longValue.extend(ensure_is_list(value))
        elif attribute_type is AttributeType.TIME_STAMP:
            pb_field.longValue.extend(
                ensure_is_list(FameTime.convert_string_if_is_datetime(value))
            )
        elif attribute_type in (AttributeType.ENUM, AttributeType.STRING):
            pb_field.stringValue.extend(ensure_is_list(value))
        elif attribute_type is AttributeType.TIME_SERIES:
            self._set_time_series_from_value(pb_field, value)
        else:
            log_error_and_raise(
                ProtoWriterException(
                    ProtoWriter._TYPE_NOT_IMPLEMENTED.format(attribute_type)
                )
            )

    def _set_time_series_from_value(self, pb_field, value):
        """Hands given `value` to TimeSeriesManager to assign a unique id which is then set to `pb_field`.seriesId"""
        if not isinstance(value, (str, int, float)):
            log_error_and_raise(
                ProtoWriterException(ProtoWriter._NOT_TIME_SERIES.format(str(value)))
            )
        elif isinstance(value, str):
            value = pt.Path(value).as_posix()
        pb_field.seriesId = self.time_series_manager.save_get_time_series_id(value)

    def _set_time_series(self, pb_input):
        """Adds all time series from TimeSeriesManager to given `pb_input`"""
        ids_of_series_by_name = self.time_series_manager.get_ids_of_series_by_name()
        for identifier, unique_id in ids_of_series_by_name.items():
            pb_series = pb_input.timeSeries.add()
            pb_series.seriesId = unique_id
            series_name, data_frame = self._get_series_as_dataframe(identifier)
            pb_series.seriesName = series_name
            try:
                ProtoWriter._add_rows_to_series(pb_series, data_frame)
            except TypeError:
                log_error_and_raise(
                    ProtoWriterException(
                        ProtoWriter._CORRUPT_TIME_SERIES_VALUE.format(identifier)
                    )
                )
            except ConversionException:
                log_error_and_raise(
                    ProtoWriterException(
                        ProtoWriter._CORRUPT_TIME_SERIES_KEY.format(identifier)
                    )
                )

    def _get_series_as_dataframe(self, identifier) -> (str, pd.DataFrame):
        """Returns a DataFrame containing the series obtained from the given `identifier` and an associated name"""
        if isinstance(identifier, str):
            # expect the string to be a file path
            series_path = self._path_resolver.resolve_series_file_path(identifier)
            if series_path and os.path.exists(series_path):
                return identifier, pd.read_csv(series_path, sep=";", header=None)
            log_error_and_raise(
                ProtoWriterException(
                    ProtoWriter._TIMESERIES_FILE_NOT_FOUND.format(identifier)
                )
            )
        else:
            name = "Constant value: {}".format(identifier)
            return name, pd.DataFrame(
                {"time": [START_IN_REAL_TIME], "value": [identifier]}
            )

    @staticmethod
    def _add_rows_to_series(series, data_frame):
        for (key, value) in data_frame.itertuples(index=False):
            row = series.row.add()
            row.timeStep = FameTime.convert_string_if_is_datetime(key)
            row.value = value

    def _write_protobuf_to_disk(self, pb_data_storage) -> None:
        """Writes given `protobuf_input_data` to disk"""
        with open(self.file_path, "wb") as file:
            file.write(pb_data_storage.SerializeToString())
        log.info("Saved protobuf file `{}` to disk".format(self.file_path))

    @staticmethod
    def _set_contract(pb_contract, contract: Contract):
        """Saves given `contract` details to protobuffer container `pb_contract`. Returns given `pb_contract`"""
        pb_contract.senderId = contract.sender_id
        pb_contract.receiverId = contract.receiver_id
        pb_contract.productName = contract.product_name
        pb_contract.firstDeliveryTime = contract.first_delivery_time
        pb_contract.deliveryIntervalInSteps = contract.delivery_interval
        if contract.expiration_time:
            pb_contract.expirationTime = contract.expiration_time
        return pb_contract

    @staticmethod
    def _set_contract_attributes(pb_parent, attributes: Dict[str, Attribute]) -> None:
        """Assign (nested) Attributes to given protobuffer container `pb_parent`"""
        for name, attribute in attributes.items():
            log.debug("Assigning contract attribute `{}`.".format(name))
            pb_field = ProtoWriter._add_field(pb_parent, name)

            if attribute.has_value:
                value = attribute.value
                if isinstance(value, int):
                    pb_field.intValue.extend([value])
                elif isinstance(value, float):
                    pb_field.doubleValue.extend([value])
                elif isinstance(value, str):
                    pb_field.stringValue.extend([value])
                else:
                    log_error_and_raise(
                        ProtoWriterException(
                            ProtoWriter._CONTRACT_UNSUPPORTED.format(str(attribute))
                        )
                    )
            elif attribute.has_nested:
                ProtoWriter._set_contract_attributes(pb_field, attribute.nested)
