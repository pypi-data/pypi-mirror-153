from abc import ABC, abstractmethod
from uuid import UUID
from typing import Type, Any
from functools import wraps
from warnings import warn
from pandas import DataFrame
import pandas
from pydantic import BaseModel, Field
import weakref

from metagen.base import LeafABC


# TODO: Solve weak references


class Register(BaseModel, ABC):

    @abstractmethod
    def add(self, element: Type[LeafABC]) -> None:
        pass

    @abstractmethod
    def check_register(self, element: Type[LeafABC]) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Type[LeafABC]:
        pass

    @abstractmethod
    def get_by_hash(self, hash: int) -> Type[LeafABC]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: UUID) -> Type[LeafABC]:
        pass

    class Config:
        arbitrary_types_allowed = True


# register
class DictRegister(Register):
    hashs: dict = Field(default_factory=dict)
    uuid: dict = Field(default_factory=dict)
    name: dict = Field(default_factory=dict)

    def add(self, element: Type[LeafABC]) -> None:
        if not self.check_register(element):
            self.hashs.update({hash(element): element})
            self.uuid.update({str(element.key): element})
            self.name.update({element.nameInternal: element})
        else:
            raise ValueError(f'PTR element "{element.__class__.__name__}" with nameInternal: {element.nameInternal}, '
                             f'key: {element.key} and hash: {hash(element)} already exist')

    def check_register(self, element: Type[LeafABC]) -> bool:
        return all([self.hashs.get(hash(element)), self.name.get(element.nameInternal)])

    def get_by_name(self, name: str) -> Type[LeafABC]:
        return self.name.get(name)

    def get_by_hash(self, hash: int) -> Type[LeafABC]:
        return self.hashs.get(hash)

    def get_by_uuid(self, uuid: str) -> Type[LeafABC]:
        if UUID(uuid):
            return self.uuid.get(uuid)


def prepare_element4pandas(element: Type[LeafABC]) -> dict:
    """Helper function, creates dict for allement to concat later the element dict into pandas dataframe"""
    element_dict = {k:v for k, v in element.dict().items() if not isinstance(v, (list, dict, tuple))}
    element_dict['element'] = weakref.ref(element)
    element_dict['type'] = element.__class__.__name__
    element_dict['hash'] = hash(element)
    return element_dict


class PandasRegister(Register):
    table: DataFrame = Field(default_factory=DataFrame)
    element_instances: list = Field(default_factory=list)

    def add(self, element: Type[LeafABC]) -> None:
        """Add element to register. If element hash in register rise error"""
        self.element_instances.append(element)
        element_pd = DataFrame(prepare_element4pandas(element), index=['key'])
        self.table = pandas.concat([self.table, element_pd], ignore_index=True, axis=0)

    def check_register(self, element: Type[LeafABC])-> bool:
        try:
            self.get_by_hash(hash(element))
            return True
        except (ValueError, KeyError):
            return False

    def get_by_name(self, name: str) -> Type[LeafABC]:
        return self.get_by_attrName(name, attrName='nameInternal')

    def get_by_hash(self, hash: int) -> Type[LeafABC]:
        return self.get_by_attrName(hash, attrName='hash')

    def get_by_uuid(self, uuid: UUID) -> Type[LeafABC]:
        return self.get_by_attrName(uuid, attrName='key')

    def get_by_attrName(self, value: Any, attrName: str) -> Type[LeafABC]:
        """Find element in register based on columne name and ist value """
        filter = self.table[attrName] == value
        return self.table.loc[filter]['element'].item()()



# register = DictRegister()
register = PandasRegister()


def exist_in_register(element):
    @wraps(element)
    def checking_register(*args, **kwargs):
        instance = element(*args, **kwargs)
        if register.check_register(instance):
            registered_element = register.get_by_hash(hash(instance))
            warn(f'Element duplication: Element {instance.__class__.__name__} with parameters: '
                 f'{"; ".join([f"{k}: {v}" for k, v in kwargs.items()])} found in register. Element '
                 f'{registered_element.__repr__()} returned instead')
            return registered_element
        else:
            register.add(instance)
            return instance
    return checking_register