from abc import ABC


class Preset(ABC):
    pass


class PresetBackgroundMaps(Preset):
    """
    Preset for MapBackgound
    """
    CartoDB_LightNoLabels = {
        "key": "cartoDB_LightNoLabels",
        "type": "wmts",
        "options": {
            "url": "https://{s}.basemaps.cartocdn.com/rastertiles/light_nolabels/{z}/{x}/{y}{r}.png"
        }}


class PresetMapSynchronization(Preset):
    AllTrue = {"roll": True,
               "tilt": True,
               "range": True,
               "center": True,
               "heading": True,
               "boxRange": True}


class PresetMapSettingView(Preset):
    Europe = {"center": {"lat": 45.77, "lon": 14.77}, "boxRange": 2103667}
