# general and helper function and classe

from typing import Union, Optional, Any, List
from pydantic import BaseModel, Field, root_validator, PrivateAttr
from pydantic.utils import ROOT_KEY
from abc import ABC, abstractmethod
from uuid import UUID, uuid4


# helper class
class SingletonMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class BaseModelWithDynamicKey(BaseModel):
    """
    Pydantic workaoround for custom dynamic key
    ref: https://stackoverflow.com/questions/60089947/creating-pydantic-model-schema-with-dynamic-key
    """
    def __init__(self, **data: Any) -> None:
        if self.__custom_root_type__ and data.keys() != {ROOT_KEY}:
            data = {ROOT_KEY: data}
        super().__init__(**data)


class LeafABC(BaseModel, ABC):
    key: Optional[UUID]

    @abstractmethod
    def __nodes__(self) -> str:
        pass

    @property
    @abstractmethod
    def hash_attrs(self) -> tuple:
        pass


# element
class Leaf(LeafABC):
    key: Optional[Union[UUID, str]] = Field(default_factory=uuid4)
    _input_pars: List[str] = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._input_pars = [k for k in data.keys()]

    def to_dict(self):
        include = {k for k, v in self.__dict__.items() if k in self._input_pars or v is not None}
        exlude = {k for k in self.__dict__.keys()} - include

        data = self.dict(by_alias=True, exclude=exlude, include=include)
        key = data.pop('key')
        return {"key": str(key), "data": data}

    @root_validator(pre=True, allow_reuse=True)
    def set_key(cls, values: dict) -> dict:
        return {k: (v.key if isinstance(v, Leaf) else v) for k, v in values.items()}

    @property
    def hash_attrs(self) -> tuple:
        return tuple()

    def __hash__(self) -> int:
        return hash(tuple([self.__dict__.get(attr) if not isinstance(self.__dict__.get(attr), list)
                                   else tuple(self.__dict__.get(attr)) for attr in self.hash_attrs]))

    __slots__ = ('__weakref__',)

    # class Config:
    #     fields = {'_input_pars': {'exclude': True}}


def set_key_from_input(value: Union[str, UUID, Leaf]):
    """
    Helper method used as validator in pydantic model.
    For input string, Leaf or UUID return valid UUID
    """
    if isinstance(value, Leaf):
        return value.key
    if isinstance(value, str):
        return UUID(value)
    return value
