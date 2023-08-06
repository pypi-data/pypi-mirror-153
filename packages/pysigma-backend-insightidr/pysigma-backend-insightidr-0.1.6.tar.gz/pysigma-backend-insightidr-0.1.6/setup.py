# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigma', 'sigma.backends.insight_idr', 'sigma.pipelines.insight_idr']

package_data = \
{'': ['*']}

install_requires = \
['pysigma>=0.6.2,<0.7.0']

setup_kwargs = {
    'name': 'pysigma-backend-insightidr',
    'version': '0.1.6',
    'description': 'pySigma Rapid7 InsightIDR backend',
    'long_description': None,
    'author': 'Micah Babinski',
    'author_email': 'm.babinski.88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SigmaHQ/pySigma-backend-insightidr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
