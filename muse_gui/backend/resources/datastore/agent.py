from typing import Dict, List

from muse_gui.backend.resources.datastore.base import BaseDatastore
from muse_gui.backend.resources.datastore.exceptions import DependentNotFound, KeyNotFound
from muse_gui.backend.data.agent import Agent

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Datastore


class AgentDatastore(BaseDatastore[Agent]):
    def __init__(self, parent: "Datastore", agents: List[Agent] = []) -> None:
        super().__init__(parent, 'share', data = agents)

    def back_dependents(self, model: Agent) -> Dict[str,List[str]]:
        try:
            region = self._parent.region.read(model.region)
        except KeyNotFound:
            raise DependentNotFound(model, model.region, self._parent.region)
        regions = [region.name]
        sectors = []
        for sector in model.sectors:
            try:
                sector = self._parent.sector.read(sector)
            except KeyNotFound:
                raise DependentNotFound(model, sector, self._parent.sector)
            sectors.append(sector)
        return {
            'region': regions,
            'sector': sectors
        }

    def forward_dependents(self, model: Agent) -> Dict[str, List[str]]:
        processes = []
        for key, process in self._parent.process._data.items():
            for technodata in process.technodatas:
                for agent in technodata.agents:
                    if agent.agent_name == model.share:
                        processes.append(key)
        return {
            'process': processes
        }
