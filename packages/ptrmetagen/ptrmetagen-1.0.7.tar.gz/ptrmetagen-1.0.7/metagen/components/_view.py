from pydantic import BaseModel
from metagen.components._general import Component


class ViewComponent(Component):
    longDescription: str


