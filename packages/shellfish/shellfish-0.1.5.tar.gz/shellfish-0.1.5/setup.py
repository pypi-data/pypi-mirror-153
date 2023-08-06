# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['shellfish', 'shellfish.aios', 'shellfish.dev', 'shellfish.fs', 'shellfish.sh']

package_data = \
{'': ['*']}

install_requires = \
['aiopen>=0.5.0,<0.6.0',
 'asyncify>=0.9.1',
 'funkify>=0.4.0',
 'jsonbourne>=0.20.3',
 'listless>=0.1.0',
 'pydantic>=1.9.0,<2.0.0',
 'xtyping>=0.6.0']

setup_kwargs = {
    'name': 'shellfish',
    'version': '0.1.5',
    'description': 'shellfish ~ shell & file-system utils',
    'long_description': '<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">\n<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>\n</a>\n\n# shellfish\n\n[![Wheel](https://img.shields.io/pypi/wheel/shellfish.svg)](https://img.shields.io/pypi/wheel/shellfish.svg)\n[![Version](https://img.shields.io/pypi/v/shellfish.svg)](https://img.shields.io/pypi/v/shellfish.svg)\n[![py_versions](https://img.shields.io/pypi/pyversions/shellfish.svg)](https://img.shields.io/pypi/pyversions/shellfish.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Install:** `pip install shellfish` OR `poetry add shellfish`\n\n**What:** shellfish = shell & file-system utils; async & sync\n\n**Features:**\n\n - Pydantic models\n - Asyncio\n - Type annotated\n\n\n**TODO:**\n\n - [ ] Add support for acceptable return codes\n - [ ] Look into breaking down shellfish.sh into smaller modules\n',
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs/tree/main/libs/shellfish',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
