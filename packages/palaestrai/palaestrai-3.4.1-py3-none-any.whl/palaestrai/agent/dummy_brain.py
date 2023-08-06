from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

from .brain import Brain
from ..core.protocol import MuscleUpdateResponse

if TYPE_CHECKING:
    import socket
    from .objective import Objective
    from .sensor_information import SensorInformation
    from .actuator_information import ActuatorInformation


class DummyBrain(Brain):
    def __init__(
        self,
        muscle_updates_listen_uri_or_socket: Union[str, socket.socket],
        sensors: List[SensorInformation],
        actuators: List[ActuatorInformation],
        objective: Objective,
        store_path: str,
        seed: int,
        **params,
    ):
        super().__init__(
            muscle_updates_listen_uri_or_socket,
            sensors,
            actuators,
            objective,
            store_path,
            seed,
            **params,
        )

    def thinking(
        self,
        muscle_id,
        readings,
        actions,
        reward,
        next_state,
        done,
        additional_data,
    ):
        response = MuscleUpdateResponse(False, None)
        return response

    def store_model(self, path):
        pass

    def load_model(self, path):
        pass
