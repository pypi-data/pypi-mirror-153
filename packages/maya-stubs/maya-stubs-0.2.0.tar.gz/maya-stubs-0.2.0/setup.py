# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maya-stubs']

package_data = \
{'': ['*'], 'maya-stubs': ['api/*', 'cmds/*', 'mel/*']}

setup_kwargs = {
    'name': 'maya-stubs',
    'version': '0.2.0',
    'description': 'Stubs for Maya',
    'long_description': '# Maya Stubs\nStubs for Autodesk Maya\n\nThe goal of this is to get as fully typed stubs for all maya APIs.\nThis is not a small feat so the stubs will improve over time.\n\n# Status:\n- 🚧 maya.cmds: Incomplete\n    - [x] Stubs for all commands.\n    - [x] Accurate Arguments signatures for most commands (parsed from `cmds.help("command")`).\n    - [x] Implicit first argument(s) for most command.\n    - [ ] Accurate Arguments signatures all commands.\n    - [ ] Return Types.\n    - [ ] Docstrings.\n- 🚧 OpenMaya 1.0: Incomplete\n    - [x] Stubs for all members\n    - [ ] Accurate Argument Signatures\n    - [ ] Return Types\n    - [ ] Docstrings.\n- 🚧 OpenMaya 2.0: Incomplete\n    - [x] Stubs for all members\n    - [ ] Accurate Argument Signatures\n    - [ ] Return Types\n    - [x] Docstrings.',
    'author': 'Loïc Pinsard',
    'author_email': 'muream@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Muream/maya-stubs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
