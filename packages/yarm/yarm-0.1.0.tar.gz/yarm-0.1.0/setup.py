# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yarm']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['yarm = yarm.console:main']}

setup_kwargs = {
    'name': 'yarm',
    'version': '0.1.0',
    'description': 'Yet another report maker.',
    'long_description': "# yarm \n\nYarm, yet another report maker.\n\nYarm makes it easy for you to create recurring reports by:\n\n- Importing spreadsheets and CSVs\n- Running SQL queries or Python code on this data\n- Exporting the results to spreadsheets, CSVs, charts, and more\n- All configured in a simple YAML file\n\n## Coming soon...\n\nYarm is nearly at alpha, but it's not yet ready for release. Come back soon.\n",
    'author': 'Bill Alive',
    'author_email': 'public+git@billalive.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/billalive/yarm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
