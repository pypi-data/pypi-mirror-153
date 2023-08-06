import enum


class State(enum.Enum):
    """States of agent modules"""

    PRISTINE = 0
    INITIALIZED = 1
    RUNNING = 2
    STOPPING = 3
    FINISHED = 4
    CANCELLED = 5
    ERROR = 6
