"""This module contains the class :class:`ExperimentRun` that defines
an experiment run and contains all the information needed to execute
it.
"""
from __future__ import annotations

import collections.abc
import importlib.resources
import io
import uuid
from io import StringIO
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, IO, Union

import pkg_resources  # TODO: Strip at some point: deprecated.
import ruamel.yaml as yml
from ruamel.yaml.constructor import ConstructorError

from numpy.random import RandomState

from ..agent import AgentConductor
from ..environment import EnvironmentConductor
from ..types.mode import Mode
from ..util import seeding
from ..util.dynaloader import load_with_params
from ..util.exception import UnknownModeError, EnvironmentHasNoUIDError
from ..util.syntax_validation import (
    SyntaxValidationResult,
    SyntaxValidationError,
)

if TYPE_CHECKING:
    from palaestrai.simulation import SimulationController
    from palaestrai.experiment import TerminationCondition

from . import LOG


class RunDefinitionError(RuntimeError):
    def __init__(self, run: ExperimentRun, message):
        super().__init__(message)

        self.message = message
        self.run = run

    def __str__(self):
        return "%s (%s)" % (self.message, self.run)


class ExperimentRun:
    """Defines an experiment run and stores information.

    The experiment run class defines a run in palaestrAI. It contains
    all information needed to execute the run. With the setup function
    the experiment run can be build.

    Parameters
    ----------

    """

    SCHEMA_FILE = "run_schema.yaml"

    def __init__(
        self,
        uid: Union[str, None],
        seed: Union[int, None],
        version: Union[str, None],
        schedule: List[Dict],
        run_config: dict,
    ):
        if seed is None:
            # numpy expects a seed between 0 and 2**32 - 1
            self.seed: int = seeding.create_seed(max_bytes=4)
        else:
            self.seed = seed
        self.rng: RandomState = seeding.np_random(self.seed)[0]

        if uid is None:
            self.uid = f"ExperimentRun-{uuid.uuid4()}"
            LOG.warning(
                "Experiment run has no uid, please set one to "
                "identify it (assign the 'uid' key). Generated: "
                "'%s', so that you can find it in the store.",
                self.uid,
            )
        else:
            self.uid = uid

        palaestrai_version = pkg_resources.require("palaestrai")[0].version
        if version is None:
            self.version = palaestrai_version
            LOG.warning(
                "No version has been specified. There is no guarantee "
                "that this run will be executed without errors. Please "
                "set the version (assign the 'version' key) in the run "
                "file. Current palaestrAI version is '%s'.",
                self.version,
            )
        elif version != palaestrai_version:
            self.version = version
            LOG.warning(
                "Your palaestrAI installation has version %s but your "
                "run file uses version %s, which may be incompatible.",
                palaestrai_version,
                version,
            )
        else:
            self.version = version

        yaml = yml.YAML(typ="safe")
        yaml.representer.add_representer(
            RandomState, ExperimentRun.repr_randomstate
        )
        yaml.constructor.add_constructor(
            "rng", ExperimentRun.constr_randomstate
        )

        self.schedule_config = schedule
        self.run_config = run_config
        self.run_governor_termination_condition: TerminationCondition
        self.schedule: list
        self._instance_uid = str(uuid.uuid4())

    @property
    def instance_uid(self):
        """The unique ID of this particular experiment run instance

        As an ::`ExperimentRun` object is transferred via network, stored in
        the DB, etc., it still remains the same instance, but it becomes
        different objects in memory. This UID identifies it even if it travels
        over the network.

        Returns
        -------

        str
            The instances unique ID
        """
        return self._instance_uid

    def create_subseed(self) -> int:
        """uses the seeded random number generator to create reproducible sub-seeds"""
        # number 5000 is arbitrary, for the numpy RandomState, could be any integer between 0 and 2**32 - 1
        a = self.rng.randint(0, 5000)
        return a

    @staticmethod
    def repr_randomstate(representer, data):
        """Custom serializer and deserializer so we can dump our subseed
        Data = rng"""
        serializedData = str(data)
        return representer.represent_scalar("rng", serializedData)

    @staticmethod
    def constr_randomstate(constructor, node):
        value = yml.loader.Constructor().construct_scalar(node)
        a = map(int, value.split(" "))
        return map(RandomState, a)

    def setup(self, broker_uri):
        """Set up an experiment run.

        Creates and configures relevant actors.
        """
        LOG.debug("ExperimentRun(id=0x%x, uid=%s) setup.", id(self), self.uid)
        rgtc = self.run_config["condition"]
        LOG.debug(
            "ExperimentRun(id=0x%x, uid=%s) loading RunGovernor "
            "TerminationCondition: %s.",
            id(self),
            self.uid,
            rgtc["name"],
        )
        try:
            rgtc = load_with_params(rgtc["name"], rgtc["params"])
        except Exception as err:
            LOG.critical(
                "Could not load termination condition '%s' with params "
                "%s for RunGovernor: %s",
                rgtc["name"],
                rgtc["params"],
                err,
            )
            raise err
        self.run_governor_termination_condition = rgtc

        self.schedule = list()
        config = dict()
        for num, phase in enumerate(self.schedule_config):
            if len(phase) > 1:
                raise RunDefinitionError(
                    self,
                    (
                        "Only one phase per phase allowed but "
                        f"found {len(phase)} phases."
                    ),
                )
            elif len(phase) < 1:
                LOG.warning(
                    "ExperimentRun(id=0x%x, uid=%s) found empty phase: "
                    "%d, skipping this one.",
                    id(self),
                    self.uid,
                    num,
                )
                continue
            phase_name = list(phase.keys())[0]
            config = update_dict(config, phase[phase_name])
            agent_configs = dict()

            self.schedule.append(dict())
            self.schedule[num]["phase_config"] = config["phase_config"].copy()
            for env_config in config["environments"]:
                self.schedule[num].setdefault("environment_conductors", dict())

                env_uid = env_config["environment"].get("uid", None)
                if env_uid is None or env_uid == "":
                    LOG.critical(
                        "ExperimentRun(id=0x%x, uid=%s): One of your "
                        "environments has no UID configured. Please "
                        "provide UIDs for all of your environments. "
                        "PalaestrAI, over and out!",
                        id(self),
                        self.uid,
                    )
                    raise EnvironmentHasNoUIDError()

                ec = EnvironmentConductor(
                    env_config["environment"],
                    broker_uri,
                    self.create_subseed(),
                )
                self.schedule[num]["environment_conductors"][ec.uid] = ec
            LOG.debug(
                "ExperimentRun(id=0x%x, uid=%s) set up %d "
                "EnvironmentConductor object(s) for phase %d: '%s'",
                id(self),
                self.uid,
                len(self.schedule[num]["environment_conductors"]),
                num,
                phase_name,
            )
            if len(self.schedule[num]["environment_conductors"]) == 0:
                raise RunDefinitionError(
                    self, f"No environments defined for phase {num}."
                )

            for agent_config in config["agents"]:
                self.schedule[num].setdefault("agent_conductors", dict())

                ac_conf = {key: value for key, value in agent_config.items()}
                ac = AgentConductor(
                    broker_uri,
                    ac_conf,
                    self.create_subseed(),
                    phase_name,
                    str(id(self)),
                )
                self.schedule[num]["agent_conductors"][ac.uid] = ac
                agent_configs[ac.uid] = ac_conf

            LOG.debug(
                "ExperimentRun(id=0x%x, uid=%s) set up %d AgentConductor "
                "object(s) for phase %d: '%s'.",
                id(self),
                self.uid,
                len(self.schedule[num]["agent_conductors"]),
                num,
                phase_name,
            )
            if len(self.schedule[num]["agent_conductors"]) == 0:
                raise RunDefinitionError(
                    self, f"No agents defined for phase {num}."
                )

            for _ in range(int(config["phase_config"].get("worker", 1))):
                self.schedule[num].setdefault("simulation_controllers", dict())
                try:
                    mode = Mode[
                        config["phase_config"].get("mode", "train").upper()
                    ]
                except KeyError as err:
                    raise UnknownModeError(err)

                sc: SimulationController = load_with_params(
                    config["simulation"]["name"],
                    {
                        "sim_connection": broker_uri,
                        "rungov_connection": broker_uri,
                        "agent_conductor_ids": list(
                            self.schedule[num]["agent_conductors"].keys()
                        ),
                        "environment_conductor_ids": list(
                            self.schedule[num]["environment_conductors"].keys()
                        ),
                        "termination_conditions": config["simulation"][
                            "conditions"
                        ],
                        "agents": agent_configs,
                        "mode": mode,
                    },
                )
                self.schedule[num]["simulation_controllers"][sc.uid] = sc
            LOG.debug(
                "ExperimentRun(id=0x%x, uid=%s) set up %d "
                "SimulationController object(s) for phase %d: '%s'.",
                id(self),
                self.uid,
                len(self.schedule[num]["simulation_controllers"]),
                num,
                phase_name,
            )
            if len(self.schedule[num]["simulation_controllers"]) == 0:
                raise RunDefinitionError(
                    self,
                    "No simulation controller defined. Either "
                    "'workers' < 1 or 'name' of key 'simulation' is "
                    "not available.",
                )
        LOG.info(
            "ExperimentRun(id=0x%x, uid=%s) setup complete.",
            id(self),
            self.uid,
        )

    def environment_conductors(self, phase=0):
        return self.schedule[phase]["environment_conductors"]

    def agent_conductors(self, phase=0):
        return self.schedule[phase]["agent_conductors"]

    def simulation_controllers(self, phase=0):
        return self.schedule[phase]["simulation_controllers"]

    def get_phase_name(self, phase: int):
        return list(self.schedule_config[phase].keys())[0]

    def get_episodes(self, phase: int):
        return self.schedule[phase]["phase_config"].get("episodes", 1)

    def phase_configuration(self, phase: int):
        return self.schedule[phase]["phase_config"]

    @property
    def num_phases(self):
        """The number of phases in this experiment run's schedule."""
        return len(self.schedule)

    def has_next_phase(self, current_phase):
        """Return if this run has a subsequent phase.

        Parameters
        ----------
        current_phase: int
            Index of the phase that is being executed.

        Returns
        -------
        bool
            True if at least one phase is taking place after
            the current phase.
        """
        return current_phase + 1 < self.num_phases

    @staticmethod
    def check_syntax(
        path_or_stream: Union[str, IO[str], PathLike]
    ) -> SyntaxValidationResult:
        """Checks if the provided experiment configuration conforms
        with our syntax.

        Parameters
        ----------
        path_or_stream: 1. str - Path to an experiment configuration file
                        2. Path - Same as above
                        3. Any text stream

        Returns
        ----------
        SyntaxValidationResult:
        Custom object that contains the following information:

            1. SyntaxValidationResult.is_valid: Whether the provided experiment
                is valid or not (::`bool`).
            2. SyntaxValidationResult.error_message: Contains ::`None` if the
                experiment is valid or the corresponding error message
                if it is invalid.

        """
        with importlib.resources.path(
            __package__, ExperimentRun.SCHEMA_FILE
        ) as path:
            validation_result = SyntaxValidationResult.validate_syntax(
                path_or_stream, path
            )
        return validation_result

    @staticmethod
    def load(str_path_stream_or_dict: Union[str, Path, Dict, IO[str]]):
        """Load an ::`ExerimentRun` object from a serialized representation.

        This method serves as deserializing constructor. It takes a
        path to a file, a dictionary representation, or a stream and creates
        a new ::`ExperimentRun` object from it.

        This method also validates the string/stream representation.

        Parameters
        ----------
        str_path_stream_or_dict : Union[str, Path, Dict, IO[str]]
            * If `str`, it is interpreted as a file path, and the file is
              resolved and loaded;
            * if `Path`, the same happens as above;
            * if `Dict`, the ::`ExperimentRun` object is initialized directly
              from the values of the `Dict`;
            * if `TextIO`, the method assumes that it is a serialzed
              representation of the ::`ExperimentRun` object (e.g., from an
              open file stream) and interprets it as YAML (with a prior
              syntax/schema check).

        Returns
        -------
        ExperimentRun
            An initialized, de-serialized ::`ExperimentRun` object
        """
        LOG.debug("Loading configuration from %s.", str_path_stream_or_dict)

        # If we get a dict directly, we syntax check nevertheless.
        if isinstance(str_path_stream_or_dict, dict):
            sio = StringIO()
            yml.YAML(typ="safe", pure=True).dump(str_path_stream_or_dict, sio)
            str_path_stream_or_dict = sio

        if isinstance(str_path_stream_or_dict, (str, Path)):
            try:
                str_path_stream_or_dict = open(str_path_stream_or_dict, "r")
            except OSError as err:
                LOG.error("Could not open run configuration: %s.", err)
                raise err

        # Load from YAML + schema check:

        validation_result = ExperimentRun.check_syntax(str_path_stream_or_dict)
        if not validation_result:
            LOG.error(
                "ExperimentRun definition did not schema validate: %s",
                validation_result.error_message,
            )
            raise SyntaxValidationError(validation_result)
        try:
            str_path_stream_or_dict.seek(0)
            conf = yml.YAML(typ="safe", pure=True).load(
                str_path_stream_or_dict
            )
            str_path_stream_or_dict.close()
        except ConstructorError as err:
            LOG.error("Could not load run configuration: %s.", err)
            raise err
        finally:
            if isinstance(str_path_stream_or_dict, io.TextIOBase):
                str_path_stream_or_dict.close()

        LOG.debug("Loaded configuration: %s.", conf)
        return ExperimentRun(
            uid=conf.get("uid", conf.get("id", None)),
            seed=conf.get("seed", None),
            version=conf.get("version", None),
            schedule=conf["schedule"],
            run_config=conf["run_config"],
        )


def update_dict(src, upd):
    """Recursive update of dictionaries.

    See stackoverflow:

        https://stackoverflow.com/questions/3232943/
        update-value-of-a-nested-dictionary-of-varying-depth

    """
    for key, val in upd.items():
        if isinstance(val, collections.abc.Mapping):
            src[key] = update_dict(src.get(key, {}), val)
        else:
            src[key] = val
    return src
