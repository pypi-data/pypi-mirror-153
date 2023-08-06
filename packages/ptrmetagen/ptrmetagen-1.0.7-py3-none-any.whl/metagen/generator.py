from pydantic import BaseModel, Field
from abc import ABC, abstractmethod, ABCMeta
from pathlib import Path
from typing import Union, List
import json

from metagen.base import Leaf
from metagen.utils import create_file, check_path, open_json, UUIDEncoder
from metagen.metadata import ElementFactory, element_factory
from metagen.register import register, Register


# serialization & deserialization
class Serializer(BaseModel, ABC):

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def to_json(self, path: Union[Path, str]) -> None:
        pass


class JSONSerializer(Serializer):
    structure: dict = Field(default={})

    def to_dict(self) -> dict:
        for _, element in register.hashs.items():
            nodes = element.__nodes__().split('.')
            self.set_node(self.structure, nodes, element)
        return self.structure

    def set_node(self, structure: dict, nodes: list, element: Leaf):
        node = nodes.pop(0)
        if len(nodes) > 0:
            if not structure.get(node):
                structure[node] = {}
            self.set_node(structure[node], nodes, element)
        else:
            if not structure.get(node):
                structure[node] = []
            structure[node].append(element.to_dict())

    def to_json(self, path: Union[Path, str]) -> None:
        structure = self.to_dict()

        path = check_path(path)

        if not path.parent:
            create_file(path.parent)

        with open(path, 'w') as file:
            json.dump(structure, file, indent=6, cls=UUIDEncoder)


class DeSerializer(BaseModel, ABC):

    @abstractmethod
    def load(self, path: Path, **kwargs) -> None:
        pass


class JSONDeserializer(DeSerializer):
    factory: ElementFactory = Field(default=element_factory)

    def load(self, path: Path, encoding='utf8') -> None:

        path = check_path(path)
        obj = open_json(path, encoding)
        for node, structure in obj.items():
            self._parse(node, structure)

    def _parse(self, nodes: str, obj: Union[dict, list]) -> None:

        if isinstance(obj, dict):
            for node, structure in obj.items():
                self._parse(f'{nodes}.{node}', structure)
        elif isinstance(obj, list):
            for data in obj:
                self.factory.create_element(nodes, data)


# generator
class GeneratorABC(BaseModel, ABC):
    serializer: Serializer
    deserializer: DeSerializer

    @property
    @abstractmethod
    def register(self) -> Register:
        pass


class Generator(GeneratorABC):
    serializer: Serializer = Field(default=JSONSerializer())
    deserializer: DeSerializer = Field(default=JSONDeserializer())

    def register(self) -> Register:
        return register

    def load_fixtures(self, path: Path, encoding='utf8') -> None:
        self.deserializer.load(path, encoding=encoding)

    def to_dict(self) -> dict:
        return self.serializer.to_dict()

    def to_json(self, path: Union[str, Path]) -> None:
        self.serializer.to_json(path)

    def get_element_by_nameInternal(self, name: str) -> Leaf:
        """Return element of given nameInternal"""
        if self.register.get_by_name(name):
            return self.register.get_by_name(name)
        else:
            raise ValueError(f'Element with nameInternal {name} did not find')

    def get_element_by_uuid(self, uuid: str) -> Leaf:
        """Return element of given uuid"""
        if register.get_by_uuid(uuid):
            return register.get_by_uuid(uuid)
        else:
            raise ValueError(f'Element with uuid {uuid} did not find')

    def get_elements_by_type(self, element: Leaf) -> List[Leaf]:
        """Return list of all elements of given element type"""
        return [v for k, v in self.register.name.items() if isinstance(v, element.__wrapped__)]

    def get_elements_by_name(self, name: str) -> List[Leaf]:
        """Return list of elements that internal name contains part of input string"""
        return [v for k, v in self.register.name.items() if k.__contains__(name)]