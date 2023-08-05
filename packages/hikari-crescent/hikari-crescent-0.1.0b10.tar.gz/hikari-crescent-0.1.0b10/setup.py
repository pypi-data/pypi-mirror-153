# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crescent', 'crescent.commands', 'crescent.internal', 'crescent.utils']

package_data = \
{'': ['*'], 'crescent': ['components/*']}

install_requires = \
['attrs>=21.4.0,<22.0.0', 'hikari>=2.0.0.dev108']

setup_kwargs = {
    'name': 'hikari-crescent',
    'version': '0.1.0b10',
    'description': '🌕 A dead simple command handler for Hikari',
    'long_description': '# hikari-crescent\n\n<div align="center">\n\n![code-style-black](https://img.shields.io/badge/code%20style-black-black)\n[![Mypy](https://github.com/magpie-dev/hikari-crescent/actions/workflows/mypy.yml/badge.svg)](https://github.com/magpie-dev/hikari-crescent/actions/workflows/mypy.yml)\n[![Docs](https://github.com/magpie-dev/hikari-crescent/actions/workflows/pdoc.yml/badge.svg)](https://magpie-dev.github.io/hikari-crescent/crescent.html)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/magpie-dev/hikari-crescent/main.svg)](https://results.pre-commit.ci/latest/github/magpie-dev/hikari-crescent/main)\n![Pypi](https://img.shields.io/pypi/v/hikari-crescent)\n\n </div>\n \nA simple command handler for [Hikari](https://github.com/hikari-py/hikari).\n\n## Features\n - Simple and intuitive API.\n - Slash, user, and message commands.\n - Error handling.\n\n### Links\n> 📝 | [Docs](https://magpie-dev.github.io/hikari-crescent/crescent.html)<br>\n> 📦 | [Pypi](https://pypi.org/project/hikari-crescent/)\n\n## Installation\nCrescent is supported in python3.8+.\n```\npip install hikari-crescent\n```\n\n## Usage\nCrescent uses signature parsing to generate your commands. Creating commands is as easy as adding typehints!\n\n```python\nimport crescent\n\nbot = crescent.Bot("YOUR_TOKEN")\n\n# Include the command in your bot - don\'t forget this\n@bot.include\n# Create a slash command\n@crescent.command\nasync def say(ctx: crescent.Context, word: str):\n    await ctx.respond(word)\n\nbot.run()\n```\n\nInformation for arguments can be provided using the `Annotated` type hint.\nSee [this example](https://github.com/magpie-dev/hikari-crescent/blob/main/examples/basic/basic.py) for more information.\n\n```python\n# python 3.9 +\nfrom typing import Annotated as Atd\n\n# python 3.8\nfrom typing_extensions import Annotated as Atd\n\n@bot.include\n@crescent.command\nasync def say(ctx: crescent.Context, word: Atd[str, "The word to say"]):\n    await ctx.respond(word)\n```\n\n# Support\nContact `Lunarmagpie❤#0001` on Discord or create an issue. All questions are welcome!\n\n# Contributing\nCreate a issue for your feature. There aren\'t any guildlines right now so just don\'t be rude.\n',
    'author': 'Lunarmagpie',
    'author_email': 'Bambolambo0@gmail.com',
    'maintainer': 'Circuit',
    'maintainer_email': 'circuitsacul@icloud.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
