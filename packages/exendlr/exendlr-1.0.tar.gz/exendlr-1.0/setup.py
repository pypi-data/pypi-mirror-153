# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['exendlr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'exendlr',
    'version': '1.0',
    'description': 'Module for reading docker logs',
    'long_description': '# ExenDLR\n\nExenifix\'s Docker Logs Reader\n\n## Description\n\nModule for reading docker logs for GitHub actions. Includes CLI and program tools.\n\n## Usage\n\n### CLI\n```shell\n$ python3 -m exendlr <container-name> <stop-phrase>\n\n# example\n$ python3 -m exendlr my-nice-bot "bot is ready!"\n```\n\n### Code\n```python\nfrom exendlr import Reader\n\nreader = Reader("my-nice-bot", "bot is ready!")\ncode = reader.start()\n\nif code == 0:\n    print("Bot was started successfully!")\nelif code == 1:\n    print("There was an error running the bot!")\n```\n',
    'author': 'Exenifix',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Exenifix/ExenDLR',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
