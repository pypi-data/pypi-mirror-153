import enum


class BasicState(enum.Enum):
    """Basis for submodule states

    This enumeration is the basis for most submodules' states. It covers their
    basic live cycle.
    """

    PRISTINE = 0
    INITIALIZING = 1
    INITIALIZED = 2
    RUNNING = 3
    STOPPING = 4
    FINISHED = 5
    CANCELLED = 6
    ERROR = 7
    SIGINT = 8
    SIGABRT = 9
    SIGTERM = 10
