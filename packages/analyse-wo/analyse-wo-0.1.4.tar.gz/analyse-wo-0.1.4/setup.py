# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['analyse_wo']

package_data = \
{'': ['*']}

install_requires = \
['getting-and-setting>=0.3.17,<0.4.0', 'pandas>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['wocli = analyse_wo.main:main']}

setup_kwargs = {
    'name': 'analyse-wo',
    'version': '0.1.4',
    'description': "Analyse WO's in M3",
    'long_description': None,
    'author': 'Kim Timothy Engh',
    'author_email': 'kimothy@users.noreply.github.com',
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
