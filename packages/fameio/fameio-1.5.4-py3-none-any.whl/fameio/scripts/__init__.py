#!/usr/bin/env python


from fameio.scripts.convert_results import DEFAULT_CONFIG as DEFAULT_CONVERT_CONFIG
from fameio.scripts.convert_results import run as convert_results
from fameio.scripts.make_config import DEFAULT_CONFIG as DEFAULT_MAKE_CONFIG
from fameio.scripts.make_config import run as make_config
from fameio.source.cli import arg_handling_convert_results, arg_handling_make_config


def makeFameRunConfig():
    input_file, run_config = arg_handling_make_config(DEFAULT_MAKE_CONFIG)
    make_config(input_file, run_config)


def convertFameResults():
    input_file, run_config = arg_handling_convert_results(DEFAULT_CONVERT_CONFIG)
    convert_results(input_file, run_config)
