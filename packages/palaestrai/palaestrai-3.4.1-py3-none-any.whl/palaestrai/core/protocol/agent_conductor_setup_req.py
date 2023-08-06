from dataclasses import dataclass


class AgentConductorSetupRequest:
    """Initiates setup of an :class:`AgentConductor`.

    * Sender:
    * Receiver:
    """

    def __init__(self, run_id, conductor_id, agent_config):
        self._run_id = run_id
        self._agent_conductor_id = conductor_id
        self._agent_config = agent_config

    @property
    def run_id(self):
        return self._run_id

    @property
    def agent_conductor_id(self):
        return self._agent_conductor_id

    @property
    def agent_config(self):
        return self._agent_config
