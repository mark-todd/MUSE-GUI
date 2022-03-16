from dataclasses import dataclass
from typing import Dict, List

from .base import BaseBackDependents, BaseDatastore, BaseForwardDependents
from muse_gui.data_defs.timeslice import Timeslice
from .exceptions import KeyAlreadyExists, KeyNotFound, LevelNameMismatch

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Datastore

class TimesliceBackDependents(BaseBackDependents):
    level_name: List[str]

class TimesliceForwardDependents(BaseForwardDependents):
    pass

class TimesliceDatastore(BaseDatastore[Timeslice, TimesliceBackDependents, TimesliceForwardDependents]):
    def __init__(self, parent: "Datastore", timeslices: List[Timeslice] = []) -> None:
        self._parent = parent
        self._data = {}
        for timeslice in timeslices:
            self.create(timeslice)

    def create(self, model: Timeslice) -> Timeslice:
        return super().create(model, model.name)

    def update(self, key: str, model: Timeslice) -> Timeslice:
        if key not in self._data:
            raise KeyNotFound(key, self)
        else:
            existing = self.read(key)
            self.back_dependents(existing)
            self.back_dependents(model)
            self._data[key] = model
            return model
    def read(self, key: str) -> Timeslice:
        if key not in self._data:
            raise KeyNotFound(key, self)
        else:
            return self._data[key]

    def delete(self, key: str) -> None:
        self._data.pop(key)
        return None
    
    def back_dependents(self, model: Timeslice) -> TimesliceBackDependents:
        level_names = self._parent.level_name.list()
        provided_levels = model.name.split('.')
        if len(level_names) != len(provided_levels):
            raise LevelNameMismatch(level_names, provided_levels)
        else:
            return TimesliceBackDependents(level_name = level_names)

    def forward_dependents(self, model: Timeslice) -> TimesliceForwardDependents:
        return TimesliceForwardDependents()
