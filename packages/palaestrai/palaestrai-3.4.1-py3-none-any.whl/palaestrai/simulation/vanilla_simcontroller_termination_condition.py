from palaestrai.core.protocol import EnvironmentUpdateResponse
from palaestrai.experiment import TerminationCondition


class VanillaSimControllerTerminationCondition(TerminationCondition):
    """
    This is the Vanilla Simulation Controller Termination Condition.
    The Termination will return True if at least one Environment
    terminates.
    """

    def check_termination(self, message, component=None):
        if isinstance(message, EnvironmentUpdateResponse):
            if message.is_terminal:
                return True
            else:
                return False
