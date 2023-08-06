# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doter', 'doter.commands']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'fire>=0.4.0,<0.5.0', 'rich>=10.15.2,<11.0.0']

entry_points = \
{'console_scripts': ['doter = doter.__main__:main']}

setup_kwargs = {
    'name': 'doter',
    'version': '1.0.0',
    'description': 'A dotfile manager',
    'long_description': None,
    'author': 'Alex Zhang',
    'author_email': 'zhangchi0104@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
