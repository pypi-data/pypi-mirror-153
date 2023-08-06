# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selenium_toolkit']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'selenium-toolkit',
    'version': '0.0.2',
    'description': 'this is not a awesome description',
    'long_description': '# WebDriverToolKit',
    'author': 'Jorge Vasconcelos',
    'author_email': 'john@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jorgepvasconcelos/webdriver-toolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
