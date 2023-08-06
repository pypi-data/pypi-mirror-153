from . import LOG


class AgentShutdownResponse:
    def __init__(self, run_id, agent_id, termination):
        self._experiment_run_id = run_id
        self._agent_id = agent_id
        self._termination = termination

    @property
    def run_id(self):
        """Deprecated: Use experiment_run_id instead."""
        LOG.debug(
            f"Run_id property deprecated in class {self.__class__}. Use experiment_run_id instead."
        )
        return self.experiment_run_id

    @run_id.setter
    def run_id(self, value):
        """Deprecated: Use experiment_run_id instead."""
        LOG.debug(
            f"Run_id property deprecated in class {self.__class__}. Use experiment_run_id instead."
        )
        self.experiment_run_id(value)

    @property
    def experiment_run_id(self):
        return self._experiment_run_id

    @experiment_run_id.setter
    def experiment_run_id(self, value):
        self._experiment_run_id = value

    @property
    def agent_id(self):
        return self._agent_id

    @agent_id.setter
    def agent_id(self, value):
        self._agent_id = value

    @property
    def termination(self):
        return self._termination

    @termination.setter
    def termination(self, value):
        self._termination = value
