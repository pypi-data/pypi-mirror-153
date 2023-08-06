import asyncio
import logging
import logging.config
import logging.handlers
import os
from pathlib import Path
from typing import Callable, Any, Union

from . import LOG
from ..core import RuntimeConfig


def _set_proctitle(process_name: str):
    try:
        import setproctitle

        setproctitle.setproctitle(f"palaestrAI[{process_name}")
    except ImportError:
        pass


def _restore_runtime_configuration(runtime_configuration_dict: dict):
    RuntimeConfig().reset()
    RuntimeConfig().load(runtime_configuration_dict)


def _reinitialize_logging():
    try:
        logging.config.dictConfig(RuntimeConfig().logging)
        logging.root.handlers.clear()
        logging.root.addHandler(
            logging.handlers.SocketHandler(
                "127.0.0.1", RuntimeConfig().logger_port
            )
        )
        logging.debug(
            "Reinitialized logging from RuntimeConfig(%s)", RuntimeConfig()
        )
    except (KeyError, ValueError) as e:
        logging.basicConfig(level=logging.INFO)
        logging.warning(
            "Could not load logging config (%s), continuing with defaults",
            e,
        )


async def spawn_wrapper(
    name: str,
    runtime_config: dict,
    callee: Callable,
    args: Union[list, None] = None,
    kwargs: Union[dict, None] = None,
) -> Any:
    """Wraps a target for fork/spawn and takes care of initialization.

    Whenever a new subprocess is created (regardless of whether spawn, fork,
    or forkserver is used), some caretaking needs to be done:

    * The runtime configuration needs to be transferred, and the
        ::`RuntimeConfig` properly reinitialized
    * Logging is reinitialized/rewired to send messages to the parent process
    * A proctitle is set

    Parameters
    ----------
    * name : str
        Name of the process; will lead to a proctitle in the form of
        ``palaestrai[%s]``
    * runtime_config : dict
        Runtime configuration dict, normally obtained from
        ::`RuntimeConfig.to_dict`
    * callee : Callable
        The target method
    * args : list, optional
        Positional arguments of ::`callee`.
    * kwargs : dict, optional
        Keyword arguments of ::`callee`

    Returns
    -------
    Any
        Whatever the target function returns.
    """
    if name:
        _set_proctitle(name)
    if not args:  # [] as default arg is mutable, workaround with None:
        args = []
    if not kwargs:  # {} as default arg is mutable, workaround with None:
        kwargs = {}
    _restore_runtime_configuration(runtime_config)
    _reinitialize_logging()

    profiler = None
    if RuntimeConfig().profile:
        import cProfile

        profiler = cProfile.Profile()
        profiler.enable()
    try:
        if asyncio.iscoroutinefunction(callee):
            ret = await callee(*args, **kwargs)
        else:
            ret = callee(*args, **kwargs)
    except Exception as e:
        LOG.critical("Running %s failed: %s", str(callee), e)
        raise e
    if profiler:
        profiler.disable()
        profiler.dump_stats(Path(os.curdir) / f"{name}.prof")
    return ret
