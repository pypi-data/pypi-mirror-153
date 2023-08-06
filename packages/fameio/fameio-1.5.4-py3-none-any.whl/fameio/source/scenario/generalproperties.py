import logging as log

from fameio.source.scenario.exception import get_or_default, get_or_raise
from fameio.source.time import FameTime
from fameio.source.tools import keys_to_lower


class GeneralProperties:
    """Hosts general properties of a scenario"""

    _KEY_RUN = "RunId".lower()
    _KEY_SIMULATION = "Simulation".lower()
    _KEY_START = "StartTime".lower()
    _KEY_STOP = "StopTime".lower()
    _KEY_SEED = "RandomSeed".lower()
    _KEY_OUTPUT = "Output".lower()
    _KEY_INTERVAL = "Interval".lower()
    _KEY_PROCESS = "Process".lower()

    _MISSING_KEY = "General Properties requires key '{}' but it is missing."
    _SIMULATION_DURATION = (
        "Simulation starts after its end time - check start and stop times."
    )

    def __init__(
        self,
        run_id: int,
        simulation_start_time: int,
        simulation_stop_time: int,
        simulation_random_seed: int,
        output_interval: int,
        output_process: int,
    ) -> None:
        if simulation_stop_time < simulation_start_time:
            log.warning(GeneralProperties._SIMULATION_DURATION)
        self._run_id = run_id
        self._simulation_start_time = simulation_start_time
        self._simulation_stop_time = simulation_stop_time
        self._simulation_random_seed = simulation_random_seed
        self._output_interval = output_interval
        self._output_process = output_process

    @classmethod
    def from_dict(cls, definitions: dict) -> "GeneralProperties":
        """Parse general properties from provided `definitions`"""
        definitions = keys_to_lower(definitions)
        run_id = get_or_default(definitions, GeneralProperties._KEY_RUN, 1)

        simulation_definition = keys_to_lower(
            get_or_raise(
                definitions,
                GeneralProperties._KEY_SIMULATION,
                GeneralProperties._MISSING_KEY,
            )
        )
        start_time = FameTime.convert_string_if_is_datetime(
            get_or_raise(
                simulation_definition,
                GeneralProperties._KEY_START,
                GeneralProperties._MISSING_KEY,
            )
        )
        stop_time = FameTime.convert_string_if_is_datetime(
            get_or_raise(
                simulation_definition,
                GeneralProperties._KEY_STOP,
                GeneralProperties._MISSING_KEY,
            )
        )
        random_seed = get_or_default(
            simulation_definition, GeneralProperties._KEY_SEED, 1
        )

        output_definitions = keys_to_lower(
            get_or_default(definitions, GeneralProperties._KEY_OUTPUT, dict())
        )
        output_interval = get_or_default(
            output_definitions, GeneralProperties._KEY_INTERVAL, 100
        )
        output_process = get_or_default(
            output_definitions, GeneralProperties._KEY_PROCESS, 0
        )

        return cls(
            run_id, start_time, stop_time, random_seed, output_interval, output_process
        )

    def to_dict(self) -> dict:
        """Serializes the general properties to a dict"""
        result = dict()

        result[self._KEY_RUN] = self.run_id

        simulation_dict = dict()
        simulation_dict[self._KEY_START] = self.simulation_start_time
        simulation_dict[self._KEY_STOP] = self.simulation_stop_time
        simulation_dict[self._KEY_SEED] = self.simulation_random_seed
        result[self._KEY_SIMULATION] = simulation_dict

        output_dict = dict()
        output_dict[self._KEY_INTERVAL] = self.output_interval
        output_dict[self._KEY_PROCESS] = self.output_process
        result[self._KEY_OUTPUT] = output_dict

        return result

    @property
    def run_id(self) -> int:
        """Returns the run ID"""
        return self._run_id

    @property
    def simulation_start_time(self) -> int:
        """Returns the simulation start time"""
        return self._simulation_start_time

    @property
    def simulation_stop_time(self) -> int:
        """Returns the simulation stop time"""
        return self._simulation_stop_time

    @property
    def simulation_random_seed(self) -> int:
        """Returns the simulation random seed"""
        return self._simulation_random_seed

    @property
    def output_interval(self) -> int:
        """Returns the output interval"""
        return self._output_interval

    @property
    def output_process(self) -> int:
        """Returns the output process"""
        return self._output_process
