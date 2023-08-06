# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kitsu']

package_data = \
{'': ['*']}

modules = \
['LICENSE']
install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'kitsu.py',
    'version': '1.1.0',
    'description': "A Simple & Lightweight Asynchronous Python Wrapper for Kitsu's Manga & Anime API.",
    'long_description': '<h1 align="center">Kitsu.py</h1>\n\n<div align="center">\n  <strong>Python API wrapper for kitsu.io</strong>\n</div>\n<div align="center">\n  A Simple & Lightweight Asynchronous Python Wrapper for Kitsu’s Manga & Anime API.\n</div>\n\n<br />\n\n\n<div align="center">\n  <!-- License -->\n  <a href="https://github.com/MrArkon/kitsu.py/blob/master/LICENSE">\n    <img src="https://img.shields.io/pypi/l/kitsu.py?label=License&style=flat-square"\n      alt="License" />\n  </a>\n  <!-- Code Quality -->\n  <a href="https://www.codacy.com/gh/MrArkon/Kitsu.py/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MrArkon/Kitsu.py&amp;utm_campaign=Badge_Grad">\n    <img src="https://img.shields.io/codacy/grade/a04e4a4edbb84f6ea6d0c5a091a912a5?label=Code%20Quality&style=flat-square" />\n  </a>\n  <!-- Downloads -->\n   <img src="https://img.shields.io/pypi/dm/Kitsu.py?label=Downloads&style=flat-square" />\n  <!-- PyPi Version -->\n  <a href="https://pypi.python.org/pypi/kitsu.py">\n      <img src="https://img.shields.io/pypi/v/Kitsu.py?label=PyPi&style=flat-square" />\n  </a>\n  <!-- PyPi Version -->\n  <img src="https://img.shields.io/pypi/pyversions/Kitsu.py?label=Python&style=flat-square" />\n</div>\n\n<div align="center">\n  <h3>\n    <a href="https://kitsu-py.readthedocs.io/">\n      Documentation\n    </a>\n    <span> | </span>\n    <a href="https://pypi.org/project/Kitsu.py/">\n      Project Page\n    </a>\n    <span> | </span>\n    <a href="https://github.com/MrArkon/Kitsu.py/blob/master/CHANGELOG.md">\n        Changelog\n    </a>\n  </h3>\n</div>\n\n\n## Features\n* **Simple and Modern** — Simple and Modern Pythonic API using `async/await`.\n* **Typed** — Fully typed to provide a smooth experience while programming.\n* **Features** — Get information about Categories, Episodes, Streaming Links and a lot more!\n* **Custom Search** — Find any Anime/Manga using Filters or Trending Animes & Mangas.\n\n## Requirements\n\nPython 3.8+\n* [aiohttp](https://pypi.org/project/aiohttp/)\n* [python-dateutil](https://pypi.org/project/python-dateutil)\n\n## Installing\nTo install the library, run the following commands:\n```shell\n# Linux/MacOS\npython3 -m pip install -U kitsu.py\n\n# Windows\npy -3 -m pip install -U kitsu.py\n```\n\n## Example\n\nSearch for an anime:\n```python\nimport kitsu\nimport asyncio\n\nclient = kitsu.Client()\n\nasync def main():\n    # Search a specific anime with the name\n    anime = await client.search_anime("jujutsu kaisen", limit=1)\n    \n    print("Canonical Title: " + anime.canonical_title)\n    print("Average Rating: " + str(anime.average_rating))\n    \n    # This returns a list of 5 animes in the spring season 2022\n    animes_in_spring = await client.search_anime(limit=5, season_year=2022, season=\'spring\')\n    \n    print(*[a.title for a in animes_in_spring], sep=", ")\n    \n    # Close the internal aiohttp ClientSession\n    await client.close()\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\nThis prints:\n```\nCanonical Title: Jujutsu Kaisen\nAverage Rating: 85.98\nThat Time I Got Reincarnated as a Slime: Ramiris to the Rescue, Blue Thermal, Q&A=E, Smol Adventures, Estab-Life: Great Escape\n```\nYou can find more examples in the [examples](https://github.com/MrArkon/kitsu.py/tree/master/examples/) directory.\n\n## License\n\nThis project is distributed under the [MIT](https://github.com/MrArkon/kitsu.py/blob/master/LICENSE.txt) license.\n',
    'author': 'MrArkon',
    'author_email': 'mrarkon@outlook.com',
    'maintainer': 'MrArkon',
    'maintainer_email': 'mrarkon@outlook.com',
    'url': 'https://github.com/MrArkon/kitsu.py/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
