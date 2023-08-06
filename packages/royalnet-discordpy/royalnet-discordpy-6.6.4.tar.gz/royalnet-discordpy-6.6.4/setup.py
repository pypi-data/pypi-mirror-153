# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalnet_discordpy', 'royalnet_discordpy.bullet']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'discord.py>=1.7.1,<2.0.0', 'royalnet>=6.7.1,<7.0.0']

setup_kwargs = {
    'name': 'royalnet-discordpy',
    'version': '6.6.4',
    'description': 'A Discord.py-based frontend for the royalnet.engineer module.',
    'long_description': '# `royalnet_telethon`\n\nA Telethon-based PDA implementation for the `royalnet.engineer` module.\n\nThe documentation is [hosted on Read The Docs](https://royalnet-console.readthedocs.io/en/latest/).\n\n## See also\n\n- [Royalnet 6](https://github.com/Steffo99/royalnet-6)\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/royalnet-discordpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
