from pydantic import BaseModel, Field, root_validator, validator, AnyUrl
from typing import Optional, Union, List, Literal, Tuple
from uuid import UUID
from pathlib import Path
import geopandas as gpd
from inspect import signature

from metagen.base import Leaf, LeafABC
from metagen.utils import prepare_data_for_leaf
from metagen.register import exist_in_register
from metagen.components import State

#  elements
# metadata
@exist_in_register
class Application(Leaf):

    name: str = Field(...)
    nameInternal: Optional[str]
    description: Optional[str]
    color: Optional[str]

    @root_validator()
    def set_application_key(cls, values):
        if values.get('name'):
            values['key'] = values['name']
            return values

    def __nodes__(self) -> str:
        return 'application.applications'

    @property
    def hash_attrs(self) -> tuple:
        return tuple(['name'])


@exist_in_register
class Configuration(Leaf):
    applicationKey: Optional[Union[str, Leaf]]
    nameInternal: Optional[str]
    data:  Optional[dict]

    def __nodes__(self) -> str:
        return 'configurations'

    @property
    def hash_attrs(self) -> tuple:
        return 'applicationKey', 'data'


@exist_in_register
class Scope(Leaf):
    applicationKey: Optional[Union[str, Leaf]]
    nameInternal: Optional[str]
    nameDisplay: Optional[str]
    description: Optional[str]

    def __nodes__(self) -> str:
        return 'metadata.scopes'

    @property
    def hash_attrs(self) -> tuple:
        return 'applicationKey', 'nameDisplay'


@exist_in_register
class Place(Leaf):
    applicationKey: Optional[Union[str, Leaf]]
    scopeKey: Optional[UUID]
    nameInternal: Optional[str]
    nameDisplay: Optional[str]
    description: Optional[str]
    geometry: Optional[Union[dict, Path]]
    bbox: Optional[List[float]]

    @validator('geometry')
    def place_geometry(cls, v):
        if isinstance(v, Path):
            geodata = gpd.read_file(v)
            if geodata.__geo_interface__.get('type') == 'FeatureCollection':
                return geodata.__geo_interface__.get('features')[0].get('geometry')
        return v

    def __nodes__(self) -> str:
        return 'metadata.places'

    @property
    def hash_attrs(self) -> tuple:
        return 'applicationKey', 'nameDisplay', 'scopeKey'


@exist_in_register
class LayerTemplate(Leaf):
    applicationKey: Optional[Union[str, Leaf]]
    nameInternal: Optional[str]
    nameDisplay: Optional[str]
    description: Optional[str]

    def __nodes__(self) -> str:
        return 'metadata.layerTemplates'

    @property
    def hash_attrs(self) -> tuple:
        return 'applicationKey', 'nameDisplay'


@exist_in_register
class Attribute(Leaf):
    applicationKey: Optional[Union[str, Leaf]]
    nameInternal: Optional[str]
    nameDisplay: Optional[str]
    description: Optional[str]
    type: Optional[str]
    unit: Optional[str]
    valueType: Optional[str]
    color: Optional[str]

    def __nodes__(self) -> str:
        return 'metadata.attributes'

    @property
    def hash_attrs(self) -> tuple:
        return 'applicationKey', 'nameDisplay', 'type'


@exist_in_register
class Period(Leaf):
    applicationKey: Optional[Union[str, Leaf]]
    scopeKey: Optional[UUID]
    nameInternal: Optional[str]
    nameDisplay: Optional[str]
    description: Optional[str]
    start: Optional[str]
    end: Optional[str]
    period: Optional[str]

    @root_validator(pre=True)
    def handle_prtData_input(cls, values):
        if all([key not in values for key in ['period', 'start', 'end']]):
            raise ValueError('Period has to have period or start and end parameters')
        elif 'period' not in values and any([key not in values for key in ['start', 'end']]):
            raise ValueError('Period has to have defined start and end parameters')
        else:
            return values

    def __nodes__(self) -> str:
        return 'metadata.periods'

    @property
    def hash_attrs(self) -> tuple:
        return 'applicationKey', 'nameDisplay', 'period', 'start', 'end'


@exist_in_register
class Case(Leaf):
    applicationKey: Optional[Union[str, Leaf]]
    nameInternal: Optional[str]
    nameDisplay: Optional[str]
    description: Optional[str]

    def __nodes__(self) -> str:
        return 'metadata.cases'

    @property
    def hash_attrs(self) -> tuple:
        return 'applicationKey', 'nameDisplay'


@exist_in_register
class Style(Leaf):
    nameDisplay: Optional[str]
    nameInternal: Optional[str]
    description: Optional[str]
    source: Optional[str]
    nameGeoserver: Optional[str]
    definition: Optional[dict]
    applicationKey: Optional[Union[str, Leaf]]
    tagKeys: Optional[UUID]

    def __nodes__(self) -> str:
        return 'metadata.styles'

    @property
    def hash_attrs(self) -> tuple:
        return 'nameDisplay', 'nameInternal', 'description', 'source', 'nameGeoserver', \
               'applicationKey', 'tagKeys'


@exist_in_register
class Tag(Leaf):
    nameInternal: Optional[str]
    nameDisplay: Optional[str]
    description: Optional[str]
    color: Optional[str]
    tagKeys: Optional[List[UUID]]

    def __nodes__(self) -> str:
        return 'metadata.tags'

    @property
    def hash_attrs(self) -> tuple:
        return 'nameDisplay', 'tagKeys'


# datasource


@exist_in_register
class SpatialVector(Leaf):
    nameInternal: Optional[str]
    layerName: Optional[str]
    tableName: Optional[str]
    fidColumnName: Optional[str]
    geometryColumnName: Optional[str]
    type: Literal['vector'] = Field(default='vector')

    def __nodes__(self) -> str:
        return 'dataSources.spatial'

    @property
    def hash_attrs(self) -> tuple:
        return 'type', 'layerName', 'tableName', 'fidColumnName', 'geometryColumnName'


@exist_in_register
class SpatialWMS(Leaf):
    nameInternal: Optional[str]
    url: Optional[str]
    layers: Optional[str]
    styles: Optional[str]
    configuration: Optional[dict]
    params: Optional[dict]
    type: Literal['wms'] = Field(default='wms')

    def __nodes__(self) -> str:
        return 'dataSources.spatial'

    @property
    def hash_attrs(self) -> tuple:
        return 'url', 'layers', 'styles', 'params'


@exist_in_register
class SpatialWMTS(Leaf):
    nameInternal: Optional[str]
    urls: Optional[List[str]]
    type: Literal['wmts'] = Field(default='wmts')

    def __nodes__(self) -> str:
        return 'dataSources.spatial'

    @property
    def hash_attrs(self) -> tuple:
        return 'urls', 'types'


@exist_in_register
class SpatialCOG(Leaf):
    nameInternal: Optional[str]
    url: Optional[str]
    type: Literal['cog'] = Field(default='cog')

    def __nodes__(self) -> str:
        return 'dataSources.spatial'

    @property
    def hash_attrs(self) -> tuple:
        return tuple(['url'])


@exist_in_register
class SpatialAttribute(Leaf):
    nameInternal: Optional[str]
    attribution: Optional[str]
    tableName: Optional[str]
    columnName: Optional[str]
    fidColumnName: Optional[str]

    def __nodes__(self) -> str:
        return 'dataSources.attribute'

    @property
    def hash_attrs(self) -> tuple:
        return 'attribution', 'tableName', 'columnName', 'fidColumnName'


# relations
@exist_in_register
class RelationSpatial(Leaf):
    nameInternal: Optional[str]
    scopeKey: Optional[Union[UUID, LeafABC]]
    periodKey: Optional[Union[UUID, LeafABC]]
    placeKey: Optional[Union[UUID, LeafABC]]
    spatialDataSourceKey: Optional[Union[UUID, LeafABC]]
    layerTemplateKey: Optional[Union[UUID, LeafABC]]
    applicationKey: Optional[Union[str, LeafABC]]
    caseKey: Optional[Union[UUID, LeafABC]]

    def __nodes__(self) -> str:
        return 'relations.spatial'

    @property
    def hash_attrs(self) -> tuple:
        return 'scopeKey:', 'periodKey', 'placeKey', 'spatialDataSourceKey', 'layerTemplateKey', 'applicationKey', \
               'caseKey'


@exist_in_register
class RelationAttribute(Leaf):
    nameInternal: Optional[str]
    scopeKey: Optional[Union[UUID, LeafABC]]
    periodKey: Optional[Union[UUID, LeafABC]]
    placeKey: Optional[Union[UUID, LeafABC]]
    attributeDataSourceKey: Optional[Union[UUID, LeafABC]]
    layerTemplateKey: Optional[Union[UUID, LeafABC]]
    scenarioKey: Optional[Union[UUID, LeafABC]]
    caseKey: Optional[Union[UUID, LeafABC]]
    attributeSetKey: Optional[Union[UUID, LeafABC]]
    attributeKey: Optional[Union[UUID, LeafABC]]
    areaTreeLevelKey: Optional[Union[UUID, LeafABC]]
    applicationKey: Optional[Union[str, LeafABC]]

    def __nodes__(self) -> str:
        return 'relations.attribute'

    @property
    def hash_attrs(self) -> tuple:
        return 'scopeKey:', 'periodKey', 'placeKey', 'attributeDataSourceKey', 'layerTemplateKey', 'scenarioKey', \
               'caseKey', 'attributeSetKey', 'attributeKey', 'areaTreeLevelKey', 'applicationKey'

# views


@exist_in_register
class View(Leaf):
    nameInternal: Optional[str]
    applicationKey: Optional[Union[str, Leaf]]
    nameDisplay: Optional[str]
    description: Optional[str]
    state: Optional[State]
    tagKeys: Optional[List[Union[UUID, str, Leaf]]]

    def __nodes__(self) -> str:
        return 'views.views'

    @property
    def hash_attrs(self) -> tuple:
        return 'applicationKey', 'nameDisplay'

    @validator('tagKeys', pre=True)
    def set_tagKey(cls, values):
        return [value.key if isinstance(value, Leaf) else value for value in values]


class ElementSignature(BaseModel):
    parameters: Tuple[str, ...]
    type: Optional[str]

    @root_validator(pre=True)
    def get_pars_from_signature(cls, values)-> tuple:
        element = values.get('parameters')
        try:
            values['parameters'] = tuple([pars for pars in signature(element).parameters])
        except TypeError:
            values['parameters'] = tuple([pars for pars in signature(element.__wrapped__).parameters])

        try:
            values['type'] = element.__fields__.get('type').default
        except AttributeError:
            pass

        return values

    def check_signature(self, input_parameters: List[str]) -> bool:
        if self.type:
            if self.type != input_parameters.get('type'):
                return False

        return all([True if k in self.parameters else False for k in input_parameters.keys()])

    def __hash__(self):
        return hash(self.parameters)


class ElementFactory(BaseModel):
    elements_register: dict = Field(default_factory=dict)

    def add(self, element: Leaf) -> None:
        element_signature = ElementSignature(parameters=element)

        if not self.elements_register.get(element.__nodes__(self)):
            self.elements_register.update({element.__nodes__(self): {}})

        self.elements_register[element.__nodes__(self)].update({element_signature: element})

    def create_element(self, nodes: str, data: dict) -> Leaf:
        element_types = self.elements_register.get(nodes)

        if not element_types:
            raise NotImplementedError(f'No elements for node {nodes}')

        init_data = prepare_data_for_leaf(data)

        for signature, element in element_types.items():
            if signature.check_signature(init_data):
                return element(**init_data)



element_factory = ElementFactory()
element_factory.add(Application)
element_factory.add(Configuration)
element_factory.add(Scope)
element_factory.add(Place)
element_factory.add(LayerTemplate)
element_factory.add(Attribute)
element_factory.add(Period)
element_factory.add(Case)
element_factory.add(Style)
element_factory.add(SpatialVector)
element_factory.add(SpatialWMS)
element_factory.add(SpatialWMTS)
element_factory.add(SpatialAttribute)
element_factory.add(RelationSpatial)
element_factory.add(RelationAttribute)
element_factory.add(View)
element_factory.add(Tag)
element_factory.add(SpatialCOG)
