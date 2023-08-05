# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maya-stubs']

package_data = \
{'': ['*'], 'maya-stubs': ['cmds/*']}

setup_kwargs = {
    'name': 'maya-stubs',
    'version': '0.1.0',
    'description': 'Stubs for Maya',
    'long_description': '# Maya Stubs\nStubs for Autodesk Maya\n\nThe goal of this is to get as fully typed stubs for all maya APIs.\nThis is not a small feat so the stubs will improve over time.\n\n# Status:\n- 🚧 maya.cmds: Incomplete\n    - [x] Stubs for all commands.\n    - [x] Accurate Arguments signatures for most commands (parsed from `cmds.help("command")`).\n    - [ ] Accurate Arguments signatures all commands.\n    - [ ] Implicit first argument of some commands.\n    - [ ] Return Types.\n    - [ ] Docstrings.\n- 🚫 OpenMaya 1.0: Missing\n- 🚫 OpenMaya 2.0: Missing',
    'author': 'Loïc Pinsard',
    'author_email': 'muream@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Muream/maya-stubs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
