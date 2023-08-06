# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botbase', 'botbase.coggies', 'botbase.wraps']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.25.0',
 'jishaku==2.4.0',
 'nextcord-ext-menus>=1.5.2,<2.0.0',
 'nextcord>=2.0.0-beta.2',
 'psutil>=5.9.0,<6.0.0']

entry_points = \
{'console_scripts': ['botbase = botbase.cli:main']}

setup_kwargs = {
    'name': 'ooliver-botbase',
    'version': '1.17.3',
    'description': 'A personal nextcord bot base package for bots.',
    'long_description': '# botbase\n\nThis is a botbase project for [nextcord](https://github.com/nextcord/nextcord) Discord Python bots to reduce boilerplate.\n\n## Config values\n\n`db_enabled: bool` default `True`\n\n`db_url: str` either this or name\n\n`db_name: str` either this or url\n\n`db_user: str` default `"ooliver"`\n\n`db_host str` default `"localhost"`\n\n`version: str` default `"0.0.0"`\n\n`aiohttp_enabled: bool` default `True`\n\n`colors: list[int]` default `[0x9966CC]`\n\n`blacklist_enabled: bool` default `True`\n\n`prefix: str | list[str]`\n\n`helpmsg: str` default [`defaulthelpmsg`](https://github.com/ooliver1/botbase/blob/main/botbase/botbase.py#L38-L47)\n\n`helpindex: str` default [`defaulthelpindex`](https://github.com/ooliver1/botbase/blob/main/botbase/botbase.py#L48-L50)\n\n`helptitle: str` default `"Help Me!"`\n\n`helpfields: dict[str, str]` default `{}`\n\n`helpinsert: str` default `""`\n\n`emojiset: Emojis[str, str]` default `Emojis()`\n\n`logchannel: int` default `None`\n\n`guild_ids: list[int]` default `None`\n',
    'author': 'ooliver1',
    'author_email': 'oliverwilkes2006@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ooliver1/botbase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
