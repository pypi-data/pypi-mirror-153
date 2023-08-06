class MuscleUpdateResponse:
    def __init__(self, is_updated, updates):
        self._is_updated = is_updated
        self._updates = updates

    @property
    def is_updated(self):
        return self._is_updated

    @is_updated.setter
    def is_updated(self, value):
        self._is_updated = value

    @property
    def updates(self):
        return self._updates

    @updates.setter
    def updates(self, value):
        self._updates = value
