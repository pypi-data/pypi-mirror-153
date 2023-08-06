from . import LOG


class EnvironmentShutdownRequest:
    def __init__(self, experiment_run_id, environment_id):
        self._experiment_run_id = experiment_run_id
        self._environment_id = environment_id

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
    def environment_id(self):
        return self._environment_id

    @environment_id.setter
    def environment_id(self, value):
        self._environment_id = value
