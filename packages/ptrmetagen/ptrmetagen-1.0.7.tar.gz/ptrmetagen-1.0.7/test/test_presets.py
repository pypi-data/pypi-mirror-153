import pytest
from metagen.presets import PresetBackgroundMaps
from metagen.components import MapBackgroundLayer


def test_background_use_enum():
    assert MapBackgroundLayer(**PresetBackgroundMaps.CartoDB_LightNoLabels)