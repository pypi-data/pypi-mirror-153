# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telebot_components',
 'telebot_components.constants',
 'telebot_components.feedback',
 'telebot_components.form',
 'telebot_components.redis_utils',
 'telebot_components.stores']

package_data = \
{'': ['*']}

install_requires = \
['markdownify>=0.11.2,<0.12.0',
 'py-trello>=0.18.0,<0.19.0',
 'pytest-mock>=3.7.0,<4.0.0',
 'redis>=4.3.1,<5.0.0',
 'telebot-against-war==0.3.5']

setup_kwargs = {
    'name': 'telebot-components',
    'version': '0.1.0',
    'description': 'Framework/toolkit for building Telegram bots with telebot and redis',
    'long_description': '# telebot-components\n\nFramework / toolkit for building bots with [telebot](https://github.com/bots-against-war/telebot).\n\n<!-- ## Development -->\n\n\n## Development\n\nInstall with Poetry (requires 1.2.x and higher with plugin support):\n\n```bash\npoetry install\n```\n\n### Testing\n\n```bash\npytest tests -vv\n```\n\nBy default all tests are run with in-memory Redis emulation. But if you have Redis installed you can run them\nlocally on real Redis by specifying something like\n\n```bash\nexport REDIS_URL="redis://localhost:1234"\n```\n\nTests must be able to find an empty Redis DB to use; they also clean up after themselves.\n',
    'author': 'Igor Vaiman',
    'author_email': 'gosha.vaiman@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bots-against-war/telebot-components',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
