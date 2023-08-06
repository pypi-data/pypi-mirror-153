# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ramqp']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=7.1.2,<8.0.0',
 'fastapi>=0.75.1,<0.76.0',
 'more-itertools>=8.12.0,<9.0.0',
 'prometheus-client>=0.13.1,<0.14.0',
 'pydantic>=1.9.0,<2.0.0',
 'pytest-asyncio>=0.18.3,<0.19.0',
 'structlog>=21.5.0,<22.0.0']

setup_kwargs = {
    'name': 'ramqp',
    'version': '2.0.1',
    'description': 'Rammearkitektur AMQP library (aio_pika wrapper)',
    'long_description': None,
    'author': 'Magenta ApS',
    'author_email': 'info@magenta.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
