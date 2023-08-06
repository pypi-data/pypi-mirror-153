from __future__ import annotations

import logging
from io import TextIOWrapper
from os import getcwd
from pathlib import Path
from typing import Any, Dict, Union, TextIO

import appdirs
import ruamel.yaml

from . import LOG


class DebugLogFilter:
    """Only allows debug messages; works as a filter for the debug_handler"""

    def __call__(self, log_message):
        if log_message.levelno == logging.DEBUG:
            return True
        else:
            return False


class _RuntimeConfig:
    """Application-wide runtime configuration.

    This singleton class provides an application-wide runtime configuration
    and transparently hides all sources from the rest of the application.
    """

    CONFIG_FILE_PATHS = [
        "%s/runtime-conf.yaml"
        % appdirs.site_config_dir("palaestrai", "OFFIS"),
        "%s/runtime-conf.yaml"
        % appdirs.user_config_dir("palaestrai", "OFFIS"),
        "%s/palaestrai-runtime.conf.yaml" % getcwd(),
        "%s/runtime.conf.yaml" % getcwd(),
    ]
    DEFAULT_CONFIG = {
        "store_uri": "sqlite:///palaestrai.db",
        "executor_bus_port": 4242,
        "logger_port": 4243,
        "public_bind": False,
        "major_domo_client_timeout": 300_000,
        "major_domo_client_retries": 3,
        "logging": {
            "version": 1,
            "formatters": {
                "simple": {
                    "format": "%(asctime)s %(name)s[%(process)d]: "
                    "%(levelname)s - %(message)s"
                },
                "debug": {
                    "format": "%(asctime)s %(name)s[%(process)d]: "
                    "%(levelname)s - %(message)s (%(module)s.%(funcName)s "
                    "in %(filename)s:%(lineno)d)"
                },
            },
            "filters": {
                "debug_filter": {
                    "()": "palaestrai.core.runtime_config.DebugLogFilter",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout",
                },
                "console_debug": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "debug",
                    "filters": ["debug_filter"],
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "palaestrai.agent": {"level": "ERROR"},
                "palaestrai.agent.brain": {"level": "ERROR"},
                "palaestrai.agent.muscle": {"level": "ERROR"},
                "palaestrai.agent.agent_conductor": {"level": "ERROR"},
                "palaestrai.core": {"level": "ERROR"},
                "palaestrai.experiment": {"level": "ERROR"},
                "palaestrai.store": {"level": "ERROR"},
                "palaestrai.environment": {"level": "ERROR"},
                "palaestrai.simulation": {"level": "ERROR"},
                "palaestrai.types": {"level": "ERROR"},
                "palaestrai.util": {"level": "ERROR"},
                "palaestrai.visualization": {"level": "ERROR"},
                "sqlalchemy.engine": {"level": "ERROR"},
            },
            "root": {
                "level": "ERROR",
                "handlers": ["console", "console_debug"],
            },
        },
        "profile": False,
    }
    _instance = None

    def __init__(self):
        self._config_file_path = None
        self.config_search_path = _RuntimeConfig.CONFIG_FILE_PATHS
        # The loaded configuration is what RuntimeConfig.load gave us. It
        # remains immutable after loading.
        self._loaded_configuration = {}

    def _get(self, key: str, default=None, exception=None) -> Any:
        """Retrieves a config key

        Retrieves any config key; if not set, it queries the config dictionary;
        if it isn't present there, it returns the given default value. It also
        sets the value in the current object as a side-effect.
        """
        lkey = "_%s" % key
        if lkey not in self.__dict__:
            try:
                self.__dict__[lkey] = self._loaded_configuration[key]
            except KeyError:
                if default:
                    self.__dict__[lkey] = default
                else:
                    self.__dict__[lkey] = _RuntimeConfig.DEFAULT_CONFIG[key]
                if exception:
                    raise KeyError(exception)
        return self.__dict__[lkey]

    def reset(self):
        """Resets the runtime configuration to empty state"""
        for key in list(self._loaded_configuration.keys()) + list(
            _RuntimeConfig.DEFAULT_CONFIG.keys()
        ):
            try:
                del self.__dict__[f"_{key}"]
            except KeyError:
                pass
        self._loaded_configuration = {}
        self._config_file_path = None

    @property
    def logging(self) -> Dict:
        """Configuration of all subsystem loggers

        :return: A logging configuration that can be fed into
            `logging.DictConfig`.
        :rtype: dict
        """
        return self._get(
            "logging",
            exception="Sorry, no logging config in the config file",
        )

    @property
    def store_uri(self) -> str:
        """URI to the store database for results

        This must be any standards-compliant string in the form of
        `transport://user:password@host-or-path:port/db`. For example,
        `postgresql://myuser:mypass@localhost/arl`.

        :return: The URI string.
        :rtype: str
        """
        return self._get("store_uri")

    @property
    def executor_bus_port(self) -> int:
        """Port of the executor's messaging bus

        palaestrai needs one bus to start it all, which is managed by the
        executor. All other buses and topics can be communicated over this
        initial bus.

        :return: The bus port, default: 4242
        :rtype: int
        """
        return self._get("executor_bus_port")

    @property
    def public_bind(self) -> bool:
        """Indicates whether to bind to all public adresses or to localhost

        This configuration setting allows the Executor and all other message
        buses to bind to all public IP addresses if set to `True`. If not,
        the buses will bind to `localhost` only.

        :return: Whether to bind to all available IP adresses (`True`) or not.
        :rtype: bool
        """
        return self._get("public_bind")

    @property
    def profile(self) -> bool:
        """Whether to enable profiling or not."""
        return self._get("profile")

    @property
    def major_domo_client_timeout(self) -> int:
        """Timeout used by the MajorDomoClient

        Returns
        -------
        int
            The timeout, in seconds
        """
        return self._get("major_domo_client_timeout")

    @property
    def major_domo_client_retries(self) -> int:
        """The number of retries the MajorDomoClient will try

        :return: the number of retries
        :rtype: int
        """
        return self._get("major_domo_client_retries")

    @property
    def logger_port(self) -> int:
        """Destination port the internal log server should use

        All spawned submodules of palaestrAI communicate their log messages
        back to the main process. This log message receiver binds to the given
        port.

        Returns
        -------
        int
            The port of the internal log server
        """
        return self._get("logger_port")

    def load(
        self, stream_or_dict: Union[dict, TextIO, str, Path, None] = None
    ):
        """Loads the configuration from an external source.

        The runtime configuration is initialized from the default configuration
        in ::`_RuntimeConfig.DEFAULT_CONFIG`. This method then iterates through
        the list in ::`_RuntimeConfig.CONFIG_FILE_PATHS`, subsequently updating
        the existing configuration with new values found. Finally, the given
        ::`stream_or_dict` parameter is used if present, ultimately taking
        preference over all other values.

        That means that each config file can contain only a portion of the
        overall configuration; it gets updated subsequently.

        Parameters
        ----------
        stream_or_dict : Union[dict, TextIO, str, Path, None]
            Loads the runtime configuration directly from a dictionary or as
            YAML-encoded stream. If no stream is given, the default files in
            ::`.CONFIG_FILE_PATHS` will be tried as described.
        """

        if not isinstance(self._loaded_configuration, dict):
            self._loaded_configuration = {}
        if not stream_or_dict and len(self._loaded_configuration) > 0:
            # Don't load a default config if we already have something; use
            # reset() instead.
            return

        yml = ruamel.yaml.YAML(typ="safe")
        has_seen_nondefault_config = False
        self._loaded_configuration.update(_RuntimeConfig.DEFAULT_CONFIG)

        for file in _RuntimeConfig.CONFIG_FILE_PATHS:
            try:
                LOG.debug("Trying to open configuration file: %s", file)
                with open(file, "r") as fp:
                    deserialized = yml.load(fp)
                    if not isinstance(deserialized, dict):
                        LOG.warning(
                            "The contents of %s could not be deserialized "
                            "to dict, skipping it.",
                            file,
                        )
                        continue
                    self._loaded_configuration.update(deserialized)
                    self._config_file_path = file
                    has_seen_nondefault_config = True
            except IOError:
                continue

        if isinstance(stream_or_dict, dict):
            self._loaded_configuration.update(stream_or_dict)
            self._config_file_path = "(dict)"
            return

        if isinstance(stream_or_dict, str):
            stream_or_dict = Path(stream_or_dict)
        if isinstance(stream_or_dict, Path):
            try:
                stream_or_dict = open(stream_or_dict, "r")
            except OSError:
                LOG.warning(
                    "Failed to load runtime configuration from file at %s, "
                    "ignoring.",
                    stream_or_dict,
                )
        if stream_or_dict is not None:
            try:
                deserialized = yml.load(stream_or_dict)  # Can raise
                if not isinstance(deserialized, dict):
                    raise TypeError
                self._loaded_configuration.update(deserialized)
                try:
                    self._config_file_path = stream_or_dict.name
                except AttributeError:
                    self._config_file_path = str(stream_or_dict)
                has_seen_nondefault_config = True
            except TypeError:
                LOG.warning(
                    "Failed to load runtime configuration from stream "
                    'at "%s", ignoring.',
                    repr(stream_or_dict),
                )
            finally:
                if isinstance(stream_or_dict, TextIOWrapper):
                    stream_or_dict.close()

        if not has_seen_nondefault_config:
            LOG.info(
                "No runtime configuration given, loaded built-in defaults."
            )
            self._config_file_path = "(DEFAULT)"

    def to_dict(self) -> Dict:
        return {key: self._get(key) for key in _RuntimeConfig.DEFAULT_CONFIG}

    def __str__(self):
        return "<RuntimeConfig id=0x%x> at %s" % (
            id(self),
            self._config_file_path,
        )

    def __repr__(self):
        return str(self.to_dict())


def RuntimeConfig():
    if _RuntimeConfig._instance is None:
        _RuntimeConfig._instance = _RuntimeConfig()
        try:
            _RuntimeConfig._instance.load()
        except FileNotFoundError:
            from copy import deepcopy

            _RuntimeConfig._instance._loaded_configuration = deepcopy(
                _RuntimeConfig.DEFAULT_CONFIG
            )
    return _RuntimeConfig._instance
