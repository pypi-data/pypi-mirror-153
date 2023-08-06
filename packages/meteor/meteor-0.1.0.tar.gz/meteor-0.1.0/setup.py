# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['meteor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'meteor',
    'version': '0.1.0',
    'description': 'Mediator pattern, interface inspired by jbogard/MediatR',
    'long_description': '# Meteor\nAn un-featureful implementation of the mediator pattern.\n\n\n# To do\n- [ ] documentation\n',
    'author': 'stnley',
    'author_email': '64174376+stnley@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stnley/meteor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
