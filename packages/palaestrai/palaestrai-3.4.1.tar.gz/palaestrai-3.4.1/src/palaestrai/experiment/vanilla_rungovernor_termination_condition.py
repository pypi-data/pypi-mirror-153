from .termination_condition import TerminationCondition


class VanillaRunGovernorTerminationCondition(TerminationCondition):
    def check_termination(self, message, component):
        if component:
            return False
        return True
