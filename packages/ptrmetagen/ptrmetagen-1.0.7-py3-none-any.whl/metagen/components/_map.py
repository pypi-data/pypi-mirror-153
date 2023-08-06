from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List, Union
from metagen.base import BaseModelWithDynamicKey
from metagen.presets import PresetBackgroundMaps, PresetMapSynchronization, PresetMapSettingView, Preset
from metagen.components._general import BaseModelArbitrary


class MapDefinitions(BaseModel):
    key: str
    data: dict = Field(default={"view": {}, "layers": []})
    name: Optional[str]


class Map(BaseModelWithDynamicKey):
    __root__: Dict[str, MapDefinitions]


class MapSynchronizationSetting(BaseModelArbitrary):
    roll: bool
    tilt: bool
    range: bool
    center: bool
    heading: bool
    boxRange: bool


class MapBackgroundLayer(BaseModelArbitrary):
    key: str
    type: str
    options: dict


class MapViewSetting(BaseModelArbitrary):
    center: dict
    boxRange: int


class MapSetDefinitionsData(BaseModelArbitrary):
    backgroundLayer: Optional[Union[MapBackgroundLayer, PresetBackgroundMaps]]
    view: Optional[Union[MapViewSetting, PresetMapSettingView]]
    viewLimits: dict = Field(default={})

    @validator('backgroundLayer', pre=True)
    def set_backgroundLayer(cls, value):
        if isinstance(value, dict):
            return MapBackgroundLayer(**value)

    @validator('view', pre=True)
    def set_view(cls, value):
        if isinstance(value, dict):
            return MapViewSetting(**value)


class MapSetDefinitions(BaseModelArbitrary):
    key: str
    data: MapSetDefinitionsData
    maps: List[str]
    sync: Optional[Union[MapSynchronizationSetting, PresetMapSynchronization]]
    activeMapKey: str

    @validator('sync', pre=True)
    def set_sync(cls, value):
        if isinstance(value, dict):
            return MapSynchronizationSetting(**value)
        return value


class MapSet(BaseModelWithDynamicKey):
    __root__: Dict[str, MapSetDefinitions]


class Maps(BaseModel):
    maps: Optional[Map]
    sets: Optional[MapSet]
    activeSetKey: Optional[str]

    @classmethod
    def set(cls, mapKey: str, mapSetKey: str, activeSetKey: str,
            background: Union[MapBackgroundLayer, PresetBackgroundMaps],
            view_setting: Union[MapViewSetting, PresetMapSettingView],
            map_synchronisation: Union[MapSynchronizationSetting, PresetMapSynchronization]):

        maps = Map(**{mapKey: MapDefinitions(key=mapKey)})
        map_set_data = MapSetDefinitionsData(backgroundLayer=background, view=view_setting)
        map_set_def = MapSetDefinitions(key=mapSetKey, data=map_set_data, maps=[mapKey], sync=map_synchronisation,
                                        activeMapKey=mapKey)

        sets = MapSet(**{mapSetKey: map_set_def})
        return cls(maps=maps, sets=sets, activeSetKey=activeSetKey)

