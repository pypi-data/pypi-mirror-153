from .muscle import Muscle


class DummyMuscle(Muscle):
    def __init__(self, broker_uri, brain_uri, uid, brain_id, path):
        super().__init__(broker_uri, brain_uri, uid, brain_id, path)

    def setup(self):
        pass

    def propose_actions(self, sensors, actuators_available, is_terminal=False):
        for actuator in actuators_available:
            actuator(actuator.action_space.sample())
        return (
            actuators_available,
            actuators_available,
            [1 for _ in actuators_available],
            {},
        )

    def update(self, update):
        pass

    @property
    def parameters(self) -> dict:
        params = {
            "uid": self.uid,
            "brain_uri": self._brain_uri,
            "broker_uri": self._broker_uri,
        }
        return params

    def __repr__(self):
        pass

    def prepare_model(self):
        pass
