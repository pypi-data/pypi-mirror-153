# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyventure']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.4.4,<13.0.0']

setup_kwargs = {
    'name': 'pyventure',
    'version': '0.1.1',
    'description': 'A simple framework for creating text adventure games.',
    'long_description': '# Pyventure is a simple library for creating a text adventure with Python\nI created this library with and for my son for him practice coding,\nusing pip, and importing libraries.\n\n\n## Installation\n`python -m pip install pyventure`\n\n## Tutorial\nPyventure handles the game logic; all the user needs to do is\ncreate `Place` objects. Each `Place` object represents a location\non the game map. It is the game space which includes things with \nwhich the player can interact.\n\nA `Place` object is created by providing four parameters:\n1. a string `name` _required_\n2. a string `description` _required_\n3. a list of `Feature`s\n4. a list of `Node`s\n\n### Example of a playable game with two places to move between\n```python\nfrom pyventure.place import Place, Feature, Node\nfrom pyventure.items import Clue, Consumable, Tool\nfrom pyventure.game_loops import start\nfrom pyventure.message import msg\n\nLIVING_ROOM = \'Living Room\'\nKITCHEN = \'Kitchen\'\n\nliving_room = Place(\n    name=LIVING_ROOM,\n    description="There is a door on your [u]left[/u] and a pencil on the carpet.",\n    features=[\n        Feature(\n            name=\'pencil\',\n            interact_msg=\'It is a no. 2 Pencil\',\n            takeable=Tool(\n                name=\'pencil\',\n                risk=0,\n                uses=10,\n                description=\'it could stand to be sharpened\',\n                total=1\n            )\n        )\n    ],\n    nodes = [\n        Node(\n            name=\'left\',\n            place_name=KITCHEN,\n            travel_msg=\'You open the door and stop into the kitchen.\',\n            accessible=True\n        )\n    ]\n)\n\n\nkitchen = Place(\n    name=KITCHEN,\n    description="The floor is dirty. You\'re afraid of what is in the refridgerator.",\n    features=[],\n    nodes = [\n        Node(\n            name=\'living room\',\n            place_name=LIVING_ROOM,\n            travel_msg=\'You are back in the living room.\',\n            accessible=True\n        )\n    ]\n)\n\nall_places = {\n    LIVING_ROOM: living_room,\n    KITCHEN: kitchen\n}\n\n\nif __name__ == \'__main__\':\n    msg.narrate(\'Welcome to a Simple Game\')\n    start(new_game_msg=\'Name your character: \', all_places=all_places)\n\n```\n',
    'author': 'David Flood',
    'author_email': 'davidfloodii@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/d-flood/pyventure',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
