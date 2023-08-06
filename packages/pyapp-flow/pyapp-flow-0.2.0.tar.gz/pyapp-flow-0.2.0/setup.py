# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyapp_flow', 'tests', 'tests.unit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyapp-flow',
    'version': '0.2.0',
    'description': 'Application workflow framework',
    'long_description': '# pyapp-flow\nA simple application level workflow.\n\nAllows processes to be broken into smaller specific steps, greatly simplifying testing and re-use.\n\n',
    'author': 'Tim Savage',
    'author_email': 'tim@savage.company',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyapp-org/pyapp-flow',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
