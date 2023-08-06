import logging as log
from pathlib import Path
from typing import List

from fameprotobuf.DataStorage_pb2 import DataStorage
from fameprotobuf.Services_pb2 import Output
from pandas import DataFrame


class ProtoReader:
    """Reads protobuffer at given `file_path` and extracts its contents"""

    def __init__(self, file_path: str) -> None:
        self.pb_output = self._read_output_from_proto_file(file_path)

    @staticmethod
    def _read_output_from_proto_file(proto_file_name: str) -> Output:
        """Reads protobuf `DataStorage` of given `proto_file_name` and returns its `output` content"""
        proto_data_storage = DataStorage()
        with open(Path(proto_file_name).as_posix(), "rb") as file:
            proto_data_storage.ParseFromString(file.read())
        return proto_data_storage.output

    def has_agent_data(self):
        """Returns True if data for any agent is present"""
        return len(self.pb_output.agentType) > 0

    def extract_agent_data(self, requested_agents: List[str]) -> dict:
        """Returns dict of DataFrames containing all data of agents listed in `requested_agents` by their class name"""
        agents_to_extract = self._get_agents_to_extract(requested_agents)
        data_frames = dict()
        for agent_type in self.pb_output.agentType:
            class_name = agent_type.className
            if class_name not in agents_to_extract:
                log.info("Ignoring not selected AgentType `{}`".format(class_name))
                continue
            agent_data = self._extract_agent_data(class_name)
            data_frame = DataFrame.from_dict(agent_data, orient="index")
            data_frame.rename(columns=self._get_column_map(agent_type), inplace=True)
            if not data_frame.empty:
                data_frame.rename_axis(("AgentId", "TimeStep"), inplace=True)
                data_frames[class_name] = data_frame
        return data_frames

    def _get_agents_to_extract(self, requested_agents: List[str]) -> List[str]:
        """Returns existing agent types that match `requested_agents` or all available types if given list is emtpy"""
        agents_to_extract = list()
        agent_types = self.pb_output.agentType
        available_agent_types = {
            agent_type.className.upper(): agent_type.className
            for agent_type in agent_types
        }
        if requested_agents:
            for agent in requested_agents:
                if agent.upper() in available_agent_types.keys():
                    agents_to_extract.append(available_agent_types[agent.upper()])
                else:
                    log.error(
                        "No output present for AgentType `{}` - Please check agent type spelling".format(
                            agent
                        )
                    )
        else:
            agents_to_extract = available_agent_types.values()
        return agents_to_extract

    @staticmethod
    def _get_column_map(agent_type) -> dict:
        """Returns dictionary of column IDs mapping to their name"""
        return {field.fieldId: field.fieldName for field in agent_type.field}

    def _extract_agent_data(self, class_name: str) -> dict:
        """Returns dict containing output of all output columns of given `class_name` by agentId and timeStep"""
        series_data = dict()
        for series in self.pb_output.series:
            if class_name == series.className:
                self._add_series_data_to(series, series_data)
        return series_data

    @staticmethod
    def _add_series_data_to(series, container: dict) -> None:
        """Adds data from given protobuffer `series` to specified `container` dict"""
        agent_id = series.agentId
        for line in series.line:
            index = (agent_id, line.timeStep)
            values = {column.fieldId: column.value for column in line.column}
            container[index] = values
