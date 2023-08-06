from dataclasses import dataclass

from .items import Tool, Clue, Consumable


@dataclass
class Node:
    name: str
    place_name: str
    travel_msg: str
    accessible: bool


@dataclass
class Feature:
    name: str
    interact_msg: str
    tool_name: str|None = None
    success_msg: str|None = None
    takeable: Tool|Clue|Consumable|None = None
    danger: int|None = None
    danger_msg: str|None = None
    unlock: Node|None = None
    # strength_required: int|None = None


@dataclass
class Place:
    '''nodes: places.Node'''
    name: str
    description: str
    features: list[Feature]
    nodes: list[Node]
