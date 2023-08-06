# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigma', 'sigma.pipelines.crowdstrike']

package_data = \
{'': ['*']}

install_requires = \
['pysigma>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'pysigma-pipeline-crowdstrike',
    'version': '0.1.6',
    'description': 'pySigma CrowdStrike processing pipelines',
    'long_description': None,
    'author': 'Thomas Patzke',
    'author_email': 'thomas@patzke.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SigmaHQ/pySigma-pipeline-crowdstrike',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
