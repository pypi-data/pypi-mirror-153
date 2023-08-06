import pytest
from metagen.components import Timeline, TimelineLayer, TimelineItem, TimelineLegend
from metagen import LayerTemplate
from test.fixtures import TIME_LAYER_1, TIME_LAYER_2, LAYER_TEMPLATE_1
from datetime import datetime


@pytest.fixture
def time_layer_1():
    return TimelineLayer(**TIME_LAYER_1)


@pytest.fixture
def time_layer_2():
    return TimelineLayer(**TIME_LAYER_2)


@pytest.fixture
def layer_template_1():
    return LayerTemplate(**LAYER_TEMPLATE_1)


# timeline_item
def test_set_timeline_item_by_layer_template(layer_template_1):
    assert TimelineItem.set_by_layerTemplate(mapZIndex=1, layerTemplate=layer_template_1)


# timelineLayer
def test_set_timelinelayer_set(layer_template_1):
    legend = TimelineLegend(layerTemplateKey=layer_template_1)
    item = TimelineItem.set_by_layerTemplate(mapZIndex=1, layerTemplate=layer_template_1)
    assert TimelineLayer.set(legend, item)


# timeline
def test_timeline_set_classmethod():
    tile_layer_1 = TimelineLayer(**TIME_LAYER_1)
    end = datetime(year=2022, month=1, day=1)
    assert Timeline.set(start='2000-01-01', end=end, timelineLayers=tile_layer_1)


def test_timeline_set_classmethod_with_list(time_layer_1, time_layer_2):
    end = datetime(year=2022, month=1, day=1)
    assert Timeline.set(start='2000-01-01', end=end, timelineLayers=[time_layer_1, time_layer_2])


def test_timeline_partial_creation(time_layer_1):
    tm1 = Timeline()
    tm1.set_timePeriod(start='2000-01-01', end='2000-02-01')
    tm1.add_timelineLayer(time_layer_1)
    assert tm1


def test_timeline_partial_creation_with_list(time_layer_1, time_layer_2):
    tm1 = Timeline()
    tm1.set_timePeriod(start='2000-01-01', end='2000-02-01')
    tm1.add_timelineLayer([time_layer_1, time_layer_2])
    assert tm1


def test_timeline_from_scratch(layer_template_1):
    tm1 = Timeline()
    tm1.set_timePeriod(start='2000-01-01', end='2000-02-01')
    legend_1 = TimelineLegend(layerTemplateKey=layer_template_1)
    item_1 = TimelineItem.set_by_layerTemplate(mapZIndex=1, layerTemplate=layer_template_1)
    tm_layer1 = TimelineLayer.set(legend=legend_1,item=item_1)
    tm1.add_timelineLayer(tm_layer1)
    assert tm1
