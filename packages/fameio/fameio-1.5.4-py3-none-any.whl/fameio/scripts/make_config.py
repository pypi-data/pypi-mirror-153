#!/usr/bin/env python
import logging as log

from fameio.source.cli import Config, arg_handling_make_config, get_config_or_default
from fameio.source.loader import load_yaml
from fameio.source.logs import set_up_logger
from fameio.source.scenario import Scenario
from fameio.source.validator import SchemaValidator
from fameio.source.writer import ProtoWriter

DEFAULT_CONFIG = {
    Config.LOG_LEVEL: "info",
    Config.LOG_FILE: None,
    Config.OUTPUT: "config.pb",
}


def run(file: str, config: dict = None) -> None:
    """Executes the main workflow for the building of a FAME configuration file"""
    config = get_config_or_default(config, DEFAULT_CONFIG)
    set_up_logger(
        level_name=config[Config.LOG_LEVEL], file_name=config[Config.LOG_FILE]
    )

    scenario = Scenario.from_dict(load_yaml(file))
    SchemaValidator.ensure_is_valid_scenario(scenario)
    writer = ProtoWriter(config[Config.OUTPUT])
    writer.write_validated_scenario(scenario)

    log.info("Configuration completed.")


if __name__ == "__main__":
    input_file, run_config = arg_handling_make_config(DEFAULT_CONFIG)
    run(input_file, run_config)
