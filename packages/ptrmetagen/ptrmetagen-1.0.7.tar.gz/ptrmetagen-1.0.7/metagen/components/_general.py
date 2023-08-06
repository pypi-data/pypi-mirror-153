from typing import Union, Dict
from uuid import UUID
from abc import ABC
from pydantic import BaseModel

from metagen.base import Leaf, BaseModelWithDynamicKey, set_key_from_input


class BaseModelArbitrary(BaseModel):
    pass

    class Config:
        arbitrary_types_allowed = True


class Component(BaseModel, ABC):
    pass


class Filter(BaseModelWithDynamicKey):
    __root__: Dict[str, UUID]

    @classmethod
    def set(cls, key_name: str, key: Union[str, UUID, Leaf]):
        uuid = set_key_from_input(key)
        return cls(**{key_name: uuid})

