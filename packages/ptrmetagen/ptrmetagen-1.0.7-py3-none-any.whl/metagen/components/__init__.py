from pydantic import BaseModel, Field
from typing import Optional


from ._map import Maps, MapViewSetting, MapSynchronizationSetting, MapBackgroundLayer, MapDefinitions, Map, \
    MapSetDefinitions, MapSet, MapSetDefinitionsData
from ._timeline import Timeline, TimelineLayer, TimelineItem, TimelineLegend
from ._view import ViewComponent
from ._general import Filter, Component


class StateComponents(BaseModel):
    View: Optional[ViewComponent]
    Timeline: Optional[Timeline]

    def add_component(self, component: Component):
        for k, v in self.__annotations__.items():
            if isinstance(component, v.__args__[0]):
                setattr(self, k, component)


class State(BaseModel):
    maps: Optional[Maps]
    components: Optional[StateComponents] = Field(default_factory=StateComponents)

    def add_maps(self, maps: Maps):
        self.maps = maps

    def add_component(self, component: Component):
        self.components.add_component(component)



