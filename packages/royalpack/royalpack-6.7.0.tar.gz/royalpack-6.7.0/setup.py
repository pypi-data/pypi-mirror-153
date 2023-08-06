# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalpack',
 'royalpack.bolts',
 'royalpack.commands',
 'royalpack.database',
 'royalpack.database.alembic',
 'royalpack.database.alembic.versions',
 'royalpack.services']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.37.0,<0.38.0',
 'aiohttp>=3.7.4,<4.0.0',
 'alembic>=1.5.8,<2.0.0',
 'arrow>=1.0.3,<2.0.0',
 'async-timeout>=3.0.1,<4.0.0',
 'coloredlogs>=15.0,<16.0',
 'colour>=0.1.5,<0.2.0',
 'psycopg2>=2.8.6,<3.0.0',
 'royalnet>=6.6.0,<6.7.0',
 'royalnet_console>=6.6.2,<7.0.0',
 'royalnet_discordpy>=6.6.2,<7.0.0',
 'royalnet_telethon>=6.6.2,<7.0.0',
 'royalspells>=3.2,<4.0',
 'sentry-sdk>=1.0.0,<2.0.0',
 'steam>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'royalpack',
    'version': '6.7.0',
    'description': 'Royalnet Commands for the RYG community',
    'long_description': '# Royalpack\n\n[Royalnet](https://github.com/Steffo99/royalnet-6) Commands for the RYG community\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RYGhub/royalpack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
