#!/usr/bin/env python

import logging as log
import os

from fameio.source.cli import (
    Config,
    arg_handling_convert_results,
    get_config_or_default,
)
from fameio.source.logs import log_and_raise_critical, set_up_logger
from fameio.source.reader import ProtoReader

DEFAULT_CONFIG = {
    Config.LOG_LEVEL: "info",
    Config.LOG_FILE: None,
    Config.AGENT_LIST: None,
    Config.OUTPUT: None,
    Config.SINGLE_AGENT_EXPORT: False,
}


def build_output_folder_name(config_output: str, input_file_path: str) -> str:
    """Returns the name of the output folder - derived either from the specified `config_output` or `input_file_path`"""
    if config_output:
        log.info("Using specified output path: {}".format(config_output))
        output_folder_name = config_output
    else:
        file_name_without_folder = input_file_path.split("\\")[-1]
        output_folder_name = file_name_without_folder.replace(".pb", "")
        log.info("No output path specified - writing to: {}".format(output_folder_name))
    return output_folder_name


def write_csv_files(output_folder: str, agent_data: dict, single_export: bool) -> None:
    """Writes given `agent_data` to .csv files at given `output_folder` grouping for `agent_id` if enabled"""
    for class_name, class_data in agent_data.items():
        class_data.sort_index(inplace=True)
        if single_export:
            for agent_id, data in class_data.groupby("AgentId"):
                out_file_name = (
                    output_folder + "/" + class_name + "_" + str(agent_id) + ".csv"
                )
                data.to_csv(out_file_name, sep=";", header=True, index=True)
        else:
            out_file_name = output_folder + "/" + class_name + ".csv"
            class_data.to_csv(out_file_name, sep=";", header=True, index=True)


def run(file_path: str, config: dict = None) -> None:
    """Reads file in protobuf format at given `file_path` and extracts its content to .csv file(s)"""
    config = get_config_or_default(config, DEFAULT_CONFIG)
    set_up_logger(
        level_name=config[Config.LOG_LEVEL], file_name=config[Config.LOG_FILE]
    )

    log.info("Reading protobuffer file...")
    proto_reader = ProtoReader(file_path)
    if not proto_reader.has_agent_data():
        log_and_raise_critical(
            "Provided protobuf file contains no data in output section."
        )

    log.info("Extracting agent data...")
    agent_data = proto_reader.extract_agent_data(config[Config.AGENT_LIST])

    output_folder = build_output_folder_name(config[Config.OUTPUT], file_path)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    log.info("Writing data to .csv files...")
    write_csv_files(output_folder, agent_data, config[Config.SINGLE_AGENT_EXPORT])
    log.info("Data conversion completed.")


if __name__ == "__main__":
    input_file, run_config = arg_handling_convert_results(DEFAULT_CONFIG)
    run(input_file, run_config)
