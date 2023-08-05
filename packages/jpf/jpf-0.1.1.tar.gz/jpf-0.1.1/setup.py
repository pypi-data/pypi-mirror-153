# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jpf']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['jpf = jpf:main']}

setup_kwargs = {
    'name': 'jpf',
    'version': '0.1.1',
    'description': 'Pretty format all your json files at once in place with three characters',
    'long_description': '# jpf\nPretty format all your json files at once in place with three characters\n\n### Usage\n\n```jpf```\n\nJust typing in the three magic characters will pretty format all your `*.json` files in the current folder and all subfolders.\nSince the command is recursive `jpf` should be used with caution.',
    'author': 'fxwiegand',
    'author_email': 'fxwiegand@wgdnet.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fxwiegand/jpf',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
