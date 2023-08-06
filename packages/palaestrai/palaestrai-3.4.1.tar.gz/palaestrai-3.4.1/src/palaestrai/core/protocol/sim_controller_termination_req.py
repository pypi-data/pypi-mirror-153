class SimControllerTerminationRequest:
    def __init__(
        self,
        sc_id,
        run_id,
        is_terminal,
        env_terminal,
        last_reward,
        additional_results,
    ):
        self.sc_id = sc_id
        self.additional_results = additional_results
        self.last_reward = last_reward
        self.env_terminal = env_terminal
        self.is_terminal = is_terminal
        self.run_id = run_id
