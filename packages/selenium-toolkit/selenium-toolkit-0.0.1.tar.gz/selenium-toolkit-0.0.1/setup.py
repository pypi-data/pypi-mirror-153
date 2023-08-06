# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['selenium_toolkit']
install_requires = \
['selenium>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'selenium-toolkit',
    'version': '0.0.1',
    'description': 'this is not a awesome description',
    'long_description': '# WebDriverToolKit',
    'author': 'Jorge Vasconcelos',
    'author_email': 'john@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jorgepvasconcelos/webdriver-toolkit',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
