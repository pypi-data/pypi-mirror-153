# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['askitsu']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'askitsu',
    'version': '0.4.0',
    'description': 'An async wrapper for Kitsu.io  API written in python',
    'long_description': '<h1  align="center">\naskitsu\n</h1>\n\n[![TwitterShomy](https://img.shields.io/badge/-shomykohai-1DA1F2?style=flat&logo=twitter&logoColor=white&labelColor=1DA1F2)](https://twitter.com/shomykohai)\n[![askitsu](https://img.shields.io/pypi/v/askitsu?label=askitsu&logo=pypi&logoColor=white&labelColor=blue&color=9cf)](https://pypi.org/project/askitsu/)\n[![Documentation Status](https://readthedocs.org/projects/askitsu/badge/?version=latest)](https://askitsu.readthedocs.io/en/latest/?badge=latest)\n\n<p align="center">\n  An async wrapper for Kitsu.io API written in Python\n</p>\n\n![askitsu](https://github.com/ShomyKohai/askitsu/blob/master/docs/images/dark.png?raw=true "askitsu")\n  \n# Key features\n\n- Fully typed\n- Use of `async`/`await`\n- Support most of primary Kitsu entries -- Anime, Manga, Characters and much more\n- Can be used with discord bots\n\n# Installing\n\nRequires python 3.8+\n\nTo install the package, you can simply run\n\n```py\n\n#Linux/MacOS\npython3 -m pip install askitsu\n\n\n#Windows\npy -3 -m pip install askitsu\n\n```\n\nOr to get the latest dev version\n\n```py\n\n#Linux/MacOS\npython3 -m pip install git+https://github.com/ShomyKohai/askitsu.git\n\n  \n\n#Windows\npy -3 -m pip install git+https://github.com/ShomyKohai/askitsu.git\n\n```\n\n## Requirements\n\n- [aiohttp](https://pypi.org/project/aiohttp/)\n- [colorama](https://pypi.org/project/colorama/)\n\n# Examples\n\n```py\nimport askitsu\nimport asyncio\n\nasync def search():\n    client = askitsu.Client()\n    anime = client.search_anime("attack on titan")\n    print(anime.episode_count)\n    print(anime.status)\n    client.close()\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(search())\n\n```\n\nMore examples can be found inside the example directory -> [Here](https://github.com/ShomyKohai/askitsu/tree/master/examples)\n\n# Links\n\n- [Docs](https://askitsu.readthedocs.io/)\n- [PyPi](https://pypi.org/project/askitsu/)\n- [Kitsu.io Docs](https://kitsu.docs.apiary.io/)\n- [discord.py](https://github.com/Rapptz/discord.py) (bot example)\n',
    'author': 'Shomy',
    'author_email': '61943525+ShomyKohai@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ShomyKohai/askitsu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
