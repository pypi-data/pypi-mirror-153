class AgentConductorSetupResponse:
    def __init__(self, run_id, conductor_id):
        self._run_id = run_id
        self._agent_conductor_id = conductor_id

    @property
    def run_id(self):
        return self._run_id

    @property
    def agent_conductor_id(self):
        return self._agent_conductor_id
