import logging as log
import os
import pathlib as pt
from fnmatch import fnmatch
from typing import IO, Any, Callable

import yaml
from fameio.source.logs import log_and_raise_critical
from fameio.source.path_resolver import PathResolver

DISABLING_YAML_FILE_PREFIX = "IGNORE_"


class Args:
    def __init__(self, file_string, node_string):
        self.file_string = file_string
        self.node_string = node_string


def read_args(loader, args):
    """Returns two Strings to be interpreted as files to be read and a subnode_address from the given `args`"""
    node_string = ""
    file_string = None
    if isinstance(args, yaml.nodes.ScalarNode):
        file_string = loader.construct_scalar(args)
        log.debug("Found instance `ScalarNode` in {}".format(file_string))
    elif isinstance(args, yaml.nodes.SequenceNode):
        argument_list = loader.construct_sequence(args)
        if len(argument_list) not in [1, 2]:
            log_and_raise_critical("!include supports but one or two arguments in list")
        elif len(argument_list) == 2:
            node_string = argument_list[1]
        file_string = argument_list[0]
        log.debug("Found instance `SequenceNode` in {}".format(file_string))
    elif isinstance(args, yaml.nodes.MappingNode):
        argument_map = loader.construct_mapping(args)
        for key, value in argument_map.items():
            if key.lower() == "file":
                file_string = value
            elif key.lower() == "node":
                node_string = value
            else:
                log_and_raise_critical("!include supports only keys 'file' and 'node'")
        if not file_string:
            log_and_raise_critical("!include: file must be specified.")
    else:
        log_and_raise_critical("YAML node type not implemented: {}".format(args))
    return Args(file_string, node_string)


def split_nodes(node_string):
    """Returns a list of nodes created from the given `node_string`"""
    log.debug("Splitting given node_string `{}`".format(node_string))
    return node_string.split(":")


class FameYamlLoader(yaml.SafeLoader):
    """Custom YAML Loader for `!include` constructor"""

    def __init__(self, stream: IO, path_resolver=PathResolver()) -> None:
        log.debug("Initialize custom YAML loader")
        self._path_resolver = path_resolver
        try:
            self._root_path = os.path.split(stream.name)[0]
        except AttributeError:
            self._root_path = os.path.curdir
        super().__init__(stream)

    @property
    def root_path(self) -> str:
        return self._root_path

    @property
    def path_resolver(self) -> PathResolver:
        return self._path_resolver


def make_yaml_loader_builder(
    path_resolver: PathResolver,
) -> Callable[[IO], yaml.Loader]:
    """Utility function used to control the creation of a FameYamlLoader by the YAML library."""
    return lambda stream: FameYamlLoader(stream, path_resolver)


def resolve_imported_path(loader: FameYamlLoader, included_path: str):
    """
    Returns a list of file paths matching the given `included_path` based on path resolution performed by the loader.

    Ignores the files starting with `DISABLING_YAML_FILE_PREFIX`
    """
    file_list = loader.path_resolver.resolve_yaml_imported_file_pattern(
        loader.root_path, included_path
    )

    ignore_filter = "*" + DISABLING_YAML_FILE_PREFIX + "*"
    cleaned_file_list = []
    for file in file_list:
        if fnmatch(file, ignore_filter):
            log.debug(
                "Ignoring file {} due to prefix {}".format(
                    file, DISABLING_YAML_FILE_PREFIX
                )
            )
        else:
            cleaned_file_list.append(file)
    if not cleaned_file_list:
        log_and_raise_critical(
            "Failed to find any file matching the `!include` directive `{}`".format(
                included_path
            )
        )
    log.debug(
        "Collected file(s) `{}` from given included path `{}`".format(
            cleaned_file_list, included_path
        )
    )
    return cleaned_file_list


def read_data_from_file(file, node_address, path_resolver: PathResolver):
    """Returns data of the specified `node_address` from the specified `file`"""
    data = yaml.load(file, make_yaml_loader_builder(path_resolver))
    for node in node_address:
        if node:
            try:
                data = data[node]
            except KeyError:
                log_and_raise_critical(
                    "'!include_node [{}, {}]': Cannot find '{}'.".format(
                        file, node_address, node
                    )
                )
    log.debug("Searched file `{}` for node `{}`".format(file, node_address))
    return data


def join_data(new_data, previous_data):
    """Joins data from multiple files if both are in list format, otherwise returns"""
    if not previous_data:
        return new_data
    if isinstance(new_data, list) and isinstance(previous_data, list):
        previous_data.extend(new_data)
        return previous_data
    else:
        log_and_raise_critical(
            "!include can only combine list-like elements from multiple files!"
        )


def construct_include(loader: FameYamlLoader, args: yaml.Node) -> Any:
    """
    Loads one or many YAML file(s) with specifications provided in `args` in different formats
    To load all content of a specified file, use:
        !include "path/to/file.yaml"
    To load only specific content (e.g. data of "Super:Sub:Node") from a given file, use:
        !include ["path/to/file.yml", "Super:Sub:Node"]
    For a slightly more verbose version of the above commands, use a dictionary argument:
        !include {"file":"path/to/file.yml", "node": "Super:Sub:Node"}

    Instead of "path/to/file.yaml" one can also use asterisks to select multiple files, e.g. "path/to/files/*.yaml"
    The given file path is either
      * relative to the path of the including YAML file, if it starts with a character other than "/"
      * an absolute path if its starts with "/"
    """
    args = read_args(loader, args)
    nodes = split_nodes(args.node_string)
    files = resolve_imported_path(loader, args.file_string)

    joined_data = None
    for file_name in files:
        with open(file_name, "r") as open_file:
            data = read_data_from_file(open_file, nodes, loader.path_resolver)
            joined_data = join_data(data, joined_data)
    log.debug("Joined all files `{}` to joined data `{}`".format(files, joined_data))
    return joined_data


FameYamlLoader.add_constructor("!include", construct_include)


def load_yaml(yaml_file_path: str, path_resolver=PathResolver()):
    """Loads the yaml file from given `yaml_file_path` and returns its content"""
    log.info("Loading yaml from {}".format(yaml_file_path))
    with open(pt.Path(yaml_file_path), "r") as configfile:
        data = yaml.load(configfile, make_yaml_loader_builder(path_resolver))
    return data
