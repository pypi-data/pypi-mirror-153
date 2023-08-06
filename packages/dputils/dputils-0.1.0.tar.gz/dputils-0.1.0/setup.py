# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dputils']

package_data = \
{'': ['*']}

install_requires = \
['docx2txt>=0.8,<0.9', 'pdfminer.six>=20220524,<20220525']

setup_kwargs = {
    'name': 'dputils',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'AkulS1008',
    'author_email': 'akulsingh0708@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
