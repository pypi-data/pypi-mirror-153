# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_quote_generator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'random-quote-generator-6886754',
    'version': '0.1.0',
    'description': 'my random quote generaror',
    'long_description': None,
    'author': 'Mfana Ronald Conco',
    'author_email': 'ronald.conco@mlankatech.co.za',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
