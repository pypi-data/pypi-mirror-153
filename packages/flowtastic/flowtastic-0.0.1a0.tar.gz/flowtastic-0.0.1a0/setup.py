# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flowtastic', 'flowtastic.cli', 'flowtastic.message', 'flowtastic.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiokafka>=0.7.2,<0.8.0', 'pydantic>=1.9.1,<2.0.0', 'rich>=12.4.4,<13.0.0']

extras_require = \
{'orjson': ['orjson>=3.6.1,<4.0.0']}

entry_points = \
{'console_scripts': ['flowtastic = flowtastic.cli.cli:app']}

setup_kwargs = {
    'name': 'flowtastic',
    'version': '0.0.1a0',
    'description': 'Python Stream Processing (Faust like!) backed by pydantic.',
    'long_description': '<div align="center">\n    <h1>flowtastic</h1>\n    <p>\n        <em>\n            Python Stream Processing (<a href="https://github.com/faust-streaming/faust">Faust</a> like!)\n            backed by <a href="https://github.com/samuelcolvin/pydantic">pydantic</a>.\n            Heavily inspired by <a href="https://github.com/tiangolo/fastapi">FastAPI</a>.\n        </em>\n    </p>\n    <a href="https://pypi.org/project/flowtastic">\n        <img src="https://img.shields.io/pypi/v/flowtastic" alt="Python package version">\n    </a>\n    <a href="https://pypi.org/project/flowtastic">\n        <img src="https://img.shields.io/pypi/pyversions/flowtastic" alt="Supported Python versions">\n    </a>\n</div>\n',
    'author': 'Gabriel Martín Blázquez',
    'author_email': 'gmartinbdev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gabrielmbmb/flowtastic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
