from abc import ABC, abstractmethod


class TerminationCondition(ABC):
    """
    The base class for termination conditions.

    Parameters
    ----------

    message:
        termination request message object

    component:
        Component for which the termination condition is to be checked. Only
        needed if terminiation condition can not be derived from termination
        request alone.


    """

    @abstractmethod
    def check_termination(self, message, component):
        raise NotImplementedError
