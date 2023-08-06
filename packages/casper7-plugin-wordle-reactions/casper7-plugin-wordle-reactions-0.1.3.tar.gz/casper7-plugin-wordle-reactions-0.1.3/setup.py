# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['casper7_plugin_wordle_reactions']

package_data = \
{'': ['*']}

install_requires = \
['docopt-ng>=0.8.1,<0.9.0', 'pydantic>=1.9.1,<2.0.0']

entry_points = \
{'console_scripts': ['casper7-plugin-wordle-reactions = '
                     'casper7_plugin_wordle_reactions.run:plugin']}

setup_kwargs = {
    'name': 'casper7-plugin-wordle-reactions',
    'version': '0.1.3',
    'description': 'a casper7 plugin that reacts to wordle results',
    'long_description': '# casper7-plugin-wordle-reactions\n\na casper7 plugin that reacts to wordle results\n',
    'author': 'backwardspy',
    'author_email': 'backwardspy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/backwardspy/casper7-plugin-wordle-reactions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
