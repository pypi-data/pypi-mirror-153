from typing import Dict, Union

from fameio.source.logs import log_error_and_raise


class SeriesManagementException(Exception):
    """Indicates that an error occurred during management of time series"""

    pass


class TimeSeriesManager:
    """Manages matching of files to time series ids and their protobuf representation"""

    _ALREADY_REGISTERED = "File '{}' was already registered."

    def __init__(self):
        self._id_count = -1
        self._ids_of_time_series = {}

    def _get_time_series_id(self, name: Union[str, int, float]) -> int:
        """Returns the id assigned to the given file name"""
        return self._ids_of_time_series.get(name)

    def _time_series_is_registered(self, name: Union[str, int, float]) -> bool:
        """Returns True if the file is already registered"""
        return name in self._ids_of_time_series.keys()

    def _register_time_series(self, name: Union[str, int, float]) -> None:
        """Assigns an id to the given file or raises an Exception if the file is already registered"""
        if not self._time_series_is_registered(name):
            self._id_count += 1
            self._ids_of_time_series[name] = self._id_count
        else:
            log_error_and_raise(
                SeriesManagementException(
                    TimeSeriesManager._ALREADY_REGISTERED.format(name)
                )
            )

    def save_get_time_series_id(self, name: Union[str, int, float]) -> int:
        """Returns the id of the time series file name - if the file is not yet registered, assigns an id"""
        if not self._time_series_is_registered(name):
            self._register_time_series(name)
        return self._get_time_series_id(name)

    def get_ids_of_series_by_name(self) -> Dict[Union[str, int, float], int]:
        return self._ids_of_time_series
