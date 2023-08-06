# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devind_core',
 'devind_core.management.commands',
 'devind_core.managers',
 'devind_core.middleware',
 'devind_core.migrations',
 'devind_core.models',
 'devind_core.permissions',
 'devind_core.schema',
 'devind_core.schema.connections',
 'devind_core.schema.mutations',
 'devind_core.schema.queries',
 'devind_core.schema.subscriptions',
 'devind_core.tasks']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3,<4',
 'celery>=5.2.7,<6.0.0',
 'channels>=3.0.4,<4.0.0',
 'devind_helpers>=0.3,<0.4',
 'django-channels-graphql-ws>=0.9.1,<0.10.0',
 'django-oauth-toolkit>=1.7.1,<2.0.0',
 'graphene-django>=2.15.0,<3.0.0',
 'graphene-file-upload>=1.3.0,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'user-agents>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'devind-core',
    'version': '0.6.2',
    'description': 'Devind core.',
    'long_description': None,
    'author': 'Victor',
    'author_email': 'lyferov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devind-team/devind-django-helpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
