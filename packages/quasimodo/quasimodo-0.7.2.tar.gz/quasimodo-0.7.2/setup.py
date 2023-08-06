# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quasimodo']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.6.1,<2.0.0', 'pika>=1.2.1,<2.0.0']

entry_points = \
{'console_scripts': ['quasimonkey = quasimodo.hunchback:hunchback_client']}

setup_kwargs = {
    'name': 'quasimodo',
    'version': '0.7.2',
    'description': 'AMQP and MQTT over WebSocket Queue Clients',
    'long_description': None,
    'author': 'doubleO8',
    'author_email': 'wb008@hdm-stuttgart.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
