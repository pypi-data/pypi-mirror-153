# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dropland_sqla']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[asyncio]>=1.4,<2.0']

entry_points = \
{'dropland.storages.sql': ['sqla = dropland_sqla.main']}

setup_kwargs = {
    'name': 'dropland-sqla',
    'version': '0.7.1',
    'description': '',
    'long_description': None,
    'author': 'Max Plutonium',
    'author_email': 'plutonium.max@gmail.com',
    'maintainer': 'Max Plutonium',
    'maintainer_email': 'plutonium.max@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
