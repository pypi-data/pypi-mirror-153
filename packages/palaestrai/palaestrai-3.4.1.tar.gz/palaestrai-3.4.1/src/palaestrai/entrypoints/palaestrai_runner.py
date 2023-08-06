import asyncio
from itertools import chain
from pathlib import Path
from typing import Union, TextIO, Tuple, List

import nest_asyncio

from palaestrai.core import RuntimeConfig
from palaestrai.experiment import ExperimentRun, Executor, ExecutorState

ExperimentRunInputTypes = Union[ExperimentRun, TextIO, str, Path]


def execute(
    experiment_run_definition: Union[
        ExperimentRunInputTypes, List[ExperimentRunInputTypes]
    ],
    runtime_config: Union[str, TextIO, dict, None] = None,
) -> Tuple[List[str], ExecutorState]:
    """Provides a single-line command to start an experiment and set a
    runtime configuration

    Parameters
    ----------
    experiment_run_definition: 1. Already set ExperimentRun object
                               2. Any text stream
                               3. The path to a file

        The configuration from which the experiment is loaded.

    runtime_config:            1. Any text stream
                               2. dict
                               3. None

        The Runtime configuration applicable for the run.
        Note that even when no additional source is provided, runtime will load
        a minimal configuration from build-in defaults.

    Returns
    -------
    typing.Tuple[Sequence[str], ExecutorState]
        A tuple containing:
        1. The list of all experiment run IDs
        2. The final state of the executor
    """
    if runtime_config:
        RuntimeConfig().load(runtime_config)

    # There is an implicit loading of the default config. The object returned
    # by RuntimeConfig() has at least the default loaded, and tries to load
    # from the search path. So there is no reason to have an explicit load()
    # here.

    if not isinstance(experiment_run_definition, List):
        experiment_run_definition = [experiment_run_definition]
    experiment_run_definition = [
        Path(i) if isinstance(i, str) else i for i in experiment_run_definition
    ]
    experiment_run_definition = list(
        chain.from_iterable(
            i.rglob("*.y*ml") if isinstance(i, Path) and i.is_dir() else [i]
            for i in experiment_run_definition
        )
    )
    experiment_runs = [
        ExperimentRun.load(i) if not isinstance(i, ExperimentRun) else i
        for i in experiment_run_definition
    ]

    nest_asyncio.apply()
    executor = Executor()
    executor.schedule(experiment_runs)
    executor_final_state = asyncio.run(executor.execute())

    return [e.uid for e in experiment_runs], executor_final_state
