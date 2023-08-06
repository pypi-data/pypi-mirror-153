import pytest

from metagen.utils import prepare_data_for_leaf
from metagen.metadata import View
from test.fixtures import VIEW, TAG_1, LAYER_TEMPLATE_1
from metagen.metadata import LayerTemplate, Tag
from metagen.components import Timeline, TimelineLegend, TimelineItem, TimelineLayer, State, StateComponents, Maps, \
    ViewComponent, MapDefinitions, Map, MapSetDefinitions, MapSetDefinitionsData, MapSet, MapBackgroundLayer,\
    MapViewSetting, MapSynchronizationSetting
from metagen.presets import PresetBackgroundMaps, PresetMapSynchronization, PresetMapSettingView
from metagen.components import Filter


@pytest.fixture(autouse=True)
def tag():
    return Tag(**prepare_data_for_leaf(TAG_1))


@pytest.fixture(autouse=True)
def layer_template_1():
    return LayerTemplate(**prepare_data_for_leaf(LAYER_TEMPLATE_1))


def test_filter_deserializations():
    assert Filter(**{"layerTemplateKey": "a0c8d936-2e52-4c31-8c55-ffefb1fed8c0"})


def test_set_fillter_from_Leaf(layer_template_1):
    assert Filter.set('layerTemplateKey', layer_template_1)


def test_element_view_model():
    view_obj = prepare_data_for_leaf(VIEW)
    assert View.__wrapped__.parse_obj(view_obj)


def test_set_view_with_timeline_from_sratch(layer_template_1):
    # timeline
    tm1 = Timeline()
    tm1.set_timePeriod(start='2000-01-01', end='2000-02-01')
    legend_1 = TimelineLegend(layerTemplateKey=layer_template_1)
    item_1 = TimelineItem.set_by_layerTemplate(mapZIndex=1, layerTemplate=layer_template_1)
    tm_layer1 = TimelineLayer.set(legend=legend_1, item=item_1)
    tm1.add_timelineLayer(tm_layer1)
    # view
    view_comp = ViewComponent(longDescription='test descrioption')
    #  state components
    state_comp = StateComponents(View=view_comp, Timeline=tm1)
    # maps
    map_def = MapDefinitions(key='map-1')
    map = Map(**{'map-1': map_def})
    map_background = MapBackgroundLayer(**PresetBackgroundMaps.CartoDB_LightNoLabels)
    map_view_setting = MapViewSetting(**PresetMapSettingView.Europe)
    map_sync_setting = MapSynchronizationSetting(**PresetMapSynchronization.AllTrue)
    map_set_data = MapSetDefinitionsData(backgroundLayer=map_background, view=map_view_setting)
    map_set_def = MapSetDefinitions(key='map-set-1', data=map_set_data, maps=['map-1'], sync=map_sync_setting,
                                    activeMapKey= "map-1")
    map_set = MapSet(**{'map-set-1': map_set_def})
    maps =Maps(maps=map, sets=map_set, activeSetKey='map-set')
    # state
    state = State(maps=maps, components=state_comp)
    assert View(nameInternal='test_view',
                applicationKey='test',
                nameDisplay='test',
                description='test description',
                state=state,
                tagKeys=[
            "478e5d14-d564-43d4-b982-978db868b1f0",
            "5ec6b453-046e-4f72-94b3-5f4146fe6224",
            "8fd34a09-bc19-4d97-9d4e-749ac2e8d735",
            "5474a30d-e5f1-4c67-bd12-6174be976893",
            "e08ded4a-9f1c-4aa2-bed7-e5620af10c33"
        ])


def test_set_view_with_timeline_by_methods(tag, layer_template_1):
    # timeline
    time_line = Timeline.set(start='2000-01-01', end='2000-02-01')
    time_line.set_timelineLayer_by_layerTemplate(legend=layer_template_1, items=[layer_template_1])
    # view
    view_comp = ViewComponent(longDescription='test descrioption')
    # maps
    maps = Maps.set(mapKey='map-1', mapSetKey='map-set-1', activeSetKey='map-set', background=PresetBackgroundMaps.CartoDB_LightNoLabels,
                   view_setting=PresetMapSettingView.Europe, map_synchronisation=PresetMapSynchronization.AllTrue)
    # state
    state = State()
    state.add_component(time_line)
    state.add_component(view_comp)
    state.add_maps(maps)


    assert View(nameInternal='test_view',
                applicationKey='test',
                nameDisplay='test',
                description='test description',
                state=state,
                tagKeys=[tag,
            "5ec6b453-046e-4f72-94b3-5f4146fe6224",
            "8fd34a09-bc19-4d97-9d4e-749ac2e8d735",
            "5474a30d-e5f1-4c67-bd12-6174be976893",
            "e08ded4a-9f1c-4aa2-bed7-e5620af10c33"
        ])