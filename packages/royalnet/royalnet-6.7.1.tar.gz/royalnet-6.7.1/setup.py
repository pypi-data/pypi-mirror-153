# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalnet',
 'royalnet.engineer',
 'royalnet.engineer.bullet',
 'royalnet.engineer.bullet.contents',
 'royalnet.engineer.bullet.projectiles',
 'royalnet.engineer.pda',
 'royalnet.engineer.pda.implementations']

package_data = \
{'': ['*']}

install_requires = \
['async-property>=0.2.1,<0.3.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'royalnet',
    'version': '6.7.1',
    'description': 'A multiplatform chat bot library',
    'long_description': '# `royalnet` 6\n\nThe repository for the development of `royalnet` version `6.0.0` and later.\n\nThe documentation is [hosted on Read The Docs](https://royalnet-6.readthedocs.io/en/latest/).\n\n## See also\n\n### PDA implementations\n\n- [royalnet-discordpy](https://github.com/Steffo99/royalnet-discordpy) (based on a Discord Bot)\n- [royalnet-console](https://github.com/Steffo99/royalnet-console) (based on a terminal session)\n\n### Old Royalnet versions\n\n- [Royalnet 5](https://github.com/Steffo99/royalnet-5)\n- [Royalnet 4](https://github.com/Steffo99/royalnet-5/tree/four)\n- [Royalbot 3](https://github.com/Steffo99/royalbot-3)\n- [Royalbot 2](https://github.com/Steffo99/royalbot-2)\n- [Royalbot 1](https://github.com/Steffo99/royalbot-1)\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': 'Stefano Pigozzi',
    'maintainer_email': 'me@steffo.eu',
    'url': 'https://github.com/Steffo99/royalnet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
