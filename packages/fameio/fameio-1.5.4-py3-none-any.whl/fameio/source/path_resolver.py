import glob
import os
from typing import List, Optional


class PathResolver:
    """Class responsible for locating files referenced in a scenario.

    Such files can be the ones referenced via the YAML `!include` extension, or simply the data files (timeseries)
    referenced in attributes.

    This class provides a default behaviour that can easily be customized by the caller."""

    def resolve_yaml_imported_file_pattern(
        self, root_path: str, file_pattern: str
    ) -> List[str]:
        """Returns a list of file paths matching the given `file_pattern` based on the configured resolver."""
        absolute_path = os.path.abspath(os.path.join(root_path, file_pattern))
        return glob.glob(absolute_path)

    def resolve_series_file_path(self, file_name: str) -> Optional[str]:
        """Returns the absolute file path for the given series (relative) file name, or None on failure."""
        if os.path.isabs(file_name):
            return file_name

        # try to locate in the current dir
        file_path = os.path.join(os.path.curdir, file_name)
        if os.path.exists(file_path):
            return file_path

        # not found
        return None
