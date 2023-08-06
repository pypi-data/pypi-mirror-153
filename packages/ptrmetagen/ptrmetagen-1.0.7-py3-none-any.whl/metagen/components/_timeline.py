from pydantic import BaseModel, Field, validator
from typing import List, Union, Optional
from uuid import UUID
from datetime import datetime

from metagen.base import Leaf, set_key_from_input
from metagen.components._general import Component
from metagen.components._general import Filter



# TODO: Verify layerState - application True
# TODO: how exactly works and by generated LayerState
# TODO: Timeline legent generalize
# TODO: Hashble TimilineItem, TimelineLayers check for duplicity
# TODO: add style definition to raster

class TimelinePeriod(BaseModel):
    start: Union[str, datetime]
    end: Union[str, datetime]


class LayerState(BaseModel):
    layerTemplateKey: Union[str, UUID, Leaf]
    styleKey: Optional[Union[str, UUID, Leaf]]
    filterByActive: dict = Field(default={"application": True})

    _set_key = validator('layerTemplateKey', pre=True, allow_reuse=True)(set_key_from_input)


class TimelineLegend(BaseModel):
    layerTemplateKey: Union[str, UUID, Leaf]

    _set_key = validator('layerTemplateKey', pre=True, allow_reuse=True)(set_key_from_input)


class TimelineItemPeriod(BaseModel):
    filter: Filter
    filterByActive: dict = Field(default={"application": True})


class TimelineItem(BaseModel):
    mapZIndex: int
    periods: TimelineItemPeriod
    layerState: LayerState

    @classmethod
    def set_by_layerTemplate(cls, mapZIndex: int, layerTemplate: Leaf, style: Optional[Leaf] = None):
        filter = Filter.set('layerTemplateKey', layerTemplate)
        periods = TimelineItemPeriod(filter=filter)
        layerstate = LayerState(layerTemplateKey=layerTemplate, styleKey=style)
        return cls(mapZIndex=mapZIndex, periods=periods, layerState=layerstate)


class TimelineLayer(BaseModel):
    legend: Optional[TimelineLegend]
    items: List[TimelineItem] = Field(default=[])

    @classmethod
    def set(cls, legend: TimelineLegend, item: Union[TimelineItem, List[TimelineItem]]):
        if isinstance(item, TimelineItem):
            item = [item]
        return cls(legend=legend, items=item)

    def set_legend(self, legend: TimelineLegend):
        self.legend = legend

    def add_item(self, item: Union[TimelineItem, List[TimelineItem]]):
        if isinstance(item, TimelineItem):
            self.items.append(item)
        elif isinstance(item, list):
            self.items += item


class Timeline(Component):
    timelinePeriod: Optional[TimelinePeriod]
    timelineLayers: List[TimelineLayer] = Field(default=[])

    @classmethod
    def set(cls, start: Union['str', datetime],
            end: Union['str', datetime],
            timelineLayers: Union[TimelineLayer, List[TimelineLayer]] = []):

        if isinstance(timelineLayers, TimelineLayer):
            timelineLayers = [timelineLayers]

        return cls(timelinePeriod=TimelinePeriod(start=start, end=end), timelineLayers=timelineLayers)

    def set_timePeriod(self, start: Union['str', datetime], end: Union['str', datetime]) -> None:
        """Set timeline time period range"""
        self.timelinePeriod = TimelinePeriod(start=start, end=end)

    def add_timelineLayer(self, timelineLayer: Union[TimelineLayer, List[TimelineLayer]]) -> None:
        """add TimeLayer into timelayer list"""
        if isinstance(timelineLayer, TimelineLayer):
            self.timelineLayers.append(timelineLayer)
        elif isinstance(timelineLayer, list):
            self.timelineLayers += timelineLayer

    def set_timelineLayer_by_layerTemplate(self, legend: Leaf, items: List[Leaf] ):
        """
        Work around to set and ad timelineLayer by layerTempalte. LayerTemplates as items are add into the timiline
        layer in order of the layertemplates listd. mapZindex is made in same order
        """
        timeline_layer = TimelineLayer(legend=TimelineLegend(layerTemplateKey=legend))
        for index, layer_template in enumerate(items):
            timeline_layer.add_item(TimelineItem.set_by_layerTemplate(mapZIndex=index, layerTemplate=layer_template))
        self.timelineLayers.append(timeline_layer)