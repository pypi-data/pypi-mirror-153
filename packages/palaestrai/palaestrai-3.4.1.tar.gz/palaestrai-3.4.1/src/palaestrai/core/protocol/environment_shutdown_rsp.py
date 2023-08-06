class EnvironmentShutdownResponse:
    def __init__(self, run_id, environment_id, termination):
        self._run_id = run_id
        self._environment_id = environment_id
        self._termination = termination

    @property
    def run_id(self):
        return self._run_id

    @run_id.setter
    def run_id(self, value):
        self._run_id = value

    @property
    def environment_id(self):
        return self._environment_id

    @environment_id.setter
    def environment_id(self, value):
        self._environment_id = value

    @property
    def termination(self):
        return self._termination

    @termination.setter
    def termination(self, value):
        self._termination = value
