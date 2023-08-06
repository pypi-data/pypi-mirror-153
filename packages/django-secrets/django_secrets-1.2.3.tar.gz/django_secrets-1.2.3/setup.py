# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_secrets',
 'django_secrets.management',
 'django_secrets.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2.27', 'future>=0.18.2,<0.19.0', 'six>=1.11,<2.0']

setup_kwargs = {
    'name': 'django-secrets',
    'version': '1.2.3',
    'description': '',
    'long_description': 'None',
    'author': 'Andy Grabow',
    'author_email': 'andy@freilandkiwis.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
