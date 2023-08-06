# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'crescent/ext'}

packages = \
['cooldowns',
 'crescent',
 'crescent.commands',
 'crescent.ext.cooldowns',
 'crescent.internal',
 'crescent.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.4.0,<22.0.0',
 'hikari>=2.0.0.dev108',
 'pycooldown>=0.1.0-beta.6,<0.2.0']

setup_kwargs = {
    'name': 'hikari-crescent',
    'version': '0.1.0',
    'description': '🌕 A dead simple command handler for Hikari',
    'long_description': '# hikari-crescent\n\n<div align="center">\n\n![code-style-black](https://img.shields.io/badge/code%20style-black-black)\n[![Mypy](https://github.com/magpie-dev/hikari-crescent/actions/workflows/mypy.yml/badge.svg)](https://github.com/magpie-dev/hikari-crescent/actions/workflows/mypy.yml)\n[![Docs](https://github.com/magpie-dev/hikari-crescent/actions/workflows/pdoc.yml/badge.svg)](https://magpie-dev.github.io/hikari-crescent/crescent.html)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/magpie-dev/hikari-crescent/main.svg)](https://results.pre-commit.ci/latest/github/magpie-dev/hikari-crescent/main)\n![Pypi](https://img.shields.io/pypi/v/hikari-crescent)\n\n </div>\n \nA simple command handler for [Hikari](https://github.com/hikari-py/hikari).\n\n## Features\n - Simple and intuitive API.\n - Slash, user, and message commands.\n - Supports autocomplete.\n - Error handling for commands, events, and autocomplete.\n - Command groups.\n - Hooks to run function before a command (or any command from a group!)\n - Plugin system to easily split bot into different modules.\n - Makes typehinting easy.\n\n### Links\n> 📝 | [Docs](https://magpie-dev.github.io/hikari-crescent/crescent.html)<br>\n> 📦 | [Pypi](https://pypi.org/project/hikari-crescent/)\n\n## Installation\nCrescent is supported in python3.8+.\n```\npip install hikari-crescent\n```\n\n## Usage\nSignature parsing can be used for simple commands.\n\n```python\nimport crescent\n\nbot = crescent.Bot("YOUR_TOKEN")\n\n# Include the command in your bot - don\'t forget this\n@bot.include\n# Create a slash command\n@crescent.command\nasync def say(ctx: crescent.Context, word: str):\n    await ctx.respond(word)\n\nbot.run()\n```\n\nInformation for arguments can be provided using the `Annotated` type hint.\nSee [this example](https://github.com/magpie-dev/hikari-crescent/blob/main/examples/basic/basic.py) for more information.\n\n```python\n# python 3.9 +\nfrom typing import Annotated as Atd\n\n# python 3.8\nfrom typing_extensions import Annotated as Atd\n\n@bot.include\n@crescent.command\nasync def say(ctx: crescent.Context, word: Atd[str, "The word to say"]) -> None:\n    await ctx.respond(word)\n```\n\nComplicated commands, such as commands with many modifiers on options or autocomplete on several options, should\nuse [class commands](https://github.com/magpie-dev/hikari-crescent/blob/main/examples/basic/command_classes.py).\nClass commands allow you to declare a command similar to how you declare a dataclass. The option function takes a\ntype followed by the description then optional information.\n\n```python\n@bot.include\n@crescent.command(name="say")\nclass Say:\n    word = crescent.option(str, "The word to say")\n\n    async def callback(self, ctx: crescent.Context) -> None:\n        await ctx.respond(self.word)\n```\n\n### Typing to Option Types Lookup Table \n| Type | Option Type |\n|---|---|\n| `str` | Text |\n| `int` | Integer |\n| `bool` | Boolean |\n| `float` | Number |\n| `hikari.User` | User |\n| `hikari.Role` | Role |\n| `crescent.Mentionable` | Role or User |\n| Any Hikari channel type. | Channel. The options will be the channel type and its subclasses. |\n| `Union[Channel Types]` (command only) | Channel. ^ |\n| `List[Channel Types]` (classes only) | Channel. ^ |\n\n### Error Handling\nErrors that are raised by a command can be handled by `crescent.catch_command`.\n\n```python\nclass MyError(Exception):\n    ...\n\n@bot.include\n@crescent.catch_command(MyError)\nasync def on_err(exc: MyError, ctx: crescent.Context) -> None:\n    await ctx.respond("An error occurred while running the command.")\n\n@bot.include\n@crescent.command\nasync def my_command(ctx: crescent.Context):\n    raise MyError()\n```\n\n### Events\n```python\nimport hikari\n\n@bot.include\n@crescent.event\nasync def on_message_create(event: hikari.MessageCreateEvent):\n    if event.message.author.is_bot:\n        return\n    await event.message.respond("Hello!")\n```\nUsing crescent\'s event decorator lets you use\ncrescent\'s [event error handling system](https://github.com/magpie-dev/hikari-crescent/blob/main/examples/error_handling/basic.py#L27).\n\n# Support\nContact `Lunarmagpie❤#0001` on Discord or create an issue. All questions are welcome!\n\n# Contributing\nCreate a issue for your feature. There aren\'t any guildlines right now so just don\'t be rude.\n',
    'author': 'Lunarmagpie',
    'author_email': 'Bambolambo0@gmail.com',
    'maintainer': 'Circuit',
    'maintainer_email': 'circuitsacul@icloud.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
