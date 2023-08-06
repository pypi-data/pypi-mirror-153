class AgentShutdownRequest:
    def __init__(self, run_id, agent_id, complete_shutdown):
        self.experiment_run_id = run_id
        self.agent_id = agent_id
        self.complete_shutdown = complete_shutdown
