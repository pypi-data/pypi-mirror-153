# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['casper7_plugin_meatball_day']

package_data = \
{'': ['*']}

install_requires = \
['docopt-ng>=0.8.1,<0.9.0',
 'pendulum>=2.1.2,<3.0.0',
 'piccolo[all]>=0.74.4,<0.75.0',
 'platformdirs>=2.5.2,<3.0.0',
 'pydantic>=1.9.1,<2.0.0']

entry_points = \
{'console_scripts': ['casper7-plugin-meatball-day = '
                     'casper7_plugin_meatball_day.run:plugin']}

setup_kwargs = {
    'name': 'casper7-plugin-meatball-day',
    'version': '0.1.0',
    'description': '',
    'long_description': "# meatball day\n\nit's a tradition\n",
    'author': 'backwardspy',
    'author_email': 'backwardspy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
