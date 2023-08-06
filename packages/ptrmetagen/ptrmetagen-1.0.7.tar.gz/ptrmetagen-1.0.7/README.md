ptr-metagen

### Description 
Python package for creation of metastracture used within the Panther Framework  (https://github.com/gisat-panther)

### Install
```
pip install ptrmetagen
```

### Exaples
View generation example
    ... tags and layer template prepared

```
from metagen.elements import View
from metagen.elements import LayerTemplate, Tag
from metagen.components import Timeline, State, Maps
from metagen.presets import PresetBackgroundMaps, PresetMapSynchronization, PresetMapSettingView

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
View(nameInternal='test_view',applicationKey='test',nameDisplay='test',description='test description',state=state,tagKeys=[tag])
```