# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compose_x_render']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1.0,<7.0',
 'argparse>=1.4.0,<2.0.0',
 'compose-x-common>=1.0,<2.0',
 'importlib-resources>=5.4.0,<6.0.0',
 'jsonschema>=3.2.0,<5.0']

entry_points = \
{'console_scripts': ['compose-x-render = compose_x_render.cli:main',
                     'ecs-compose-x-render = compose_x_render.cli:main']}

setup_kwargs = {
    'name': 'compose-x-render',
    'version': '0.5.5',
    'description': 'Library & Tool to compile/merge compose files with top level extension fields',
    'long_description': None,
    'author': 'John Preston',
    'author_email': 'john@compose-x.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
