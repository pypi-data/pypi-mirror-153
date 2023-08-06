# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yukinator']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.4.0,<22.0.0', 'requests-cache>=0.9.4,<0.10.0']

setup_kwargs = {
    'name': 'yukinator',
    'version': '0.1.1',
    'description': 'Unofficial Ergast API wrapper',
    'long_description': "# yukinator\n![actions](https://github.com/BrozenSenpai/yukinator/actions/workflows/python-package.yml/badge.svg)[![Documentation Status](https://readthedocs.org/projects/yukinator/badge/?version=latest)](https://yukinator.readthedocs.io/en/latest/?badge=latest)\n\nUnofficial API wrapper for [Ergast API](http://ergast.com/mrd/). \n\nCreated mainly for learning purposes. There are already at least two other wrappers worth checking: [fastF1](https://github.com/theOehrly/Fast-F1) -  a swiss army knife for F1-related analyses, [pyErgast](https://github.com/weiranyu/pyErgast) - a neat pandas wrapper.\n\nThe name of the wrapper is Yukinator, in honor of the Japanese Formula 1 driver - Yuki Tsunoda.\n\n## Features\n- **Extensive**: covers all Ergast API endpoints\n- **Responsible**: minimize the load on the API server\n    - implemented caching\n- **Simple**: easy to use and customize:\n    - object-oriented design\n    - use of data transfer objects\n    - converts adequate fields from strings to the more suitable types\n- **Lightweight**: minimal usage of the third-party packages\n\n## Installation\n```\npip install yukinator\n ```\n\n## Getting started\nObtaining data for an Ergast API endpoint is very simple. For example, you can get a list of race objects from the 2020 season like this:\n```python\nimport yukinator\n\ny = yukinator.Yuki()\nraces_2020 = y.get_races(year=2020)\n```\nCheck the docs to get acquainted with the methods for the rest of the endpoints.\n\nThe wrapper is initiated with the caching enabled by default. You can manually set the caching-related attributes like a directory for cache file, time after cached items expire, or clear the whole cache before the first request as follows:\n```python\ny = yukinator.Yuki(cache_dir='f1project/races', expires_after=9000, force_clear=True)\n```\nThe caching can be also disabled (strongly not recommended):\n```python\ny = yukinator.Yuki(cache_enabled=False)\n```\nChosen fields of the object can be accessed easily:\n```python\nrace_1 = races_2020[0]\n\n# print name of the race\nprint(race_1.raceName)\n\n# print name from every nested Circuit object\nfor race in races_2020:\n    print(race.Circuit.circuitName)\n```\nEvery object from the obtained list can be converted to the simpler structures:\n```python\n# convert object to the dictionary\nrace_1_dict = race_1.to_dict()\n\n# convert object to the tuple\nrace_1_tuple = race_1.to_tuple()\n\n# convert object to the flat dict - useful for creating pandas dataframes\nrace_1_flat_dict = race_1.to_flat_dict() \n\n# convert object to a json string\nrace_1_json = race_1.to_json()\n```\n\n**WARNING**\n\nThe Ergast API has a limit of four calls per second and 200 per hour. Please take care while calling the methods within a loop.\n\n## Documentation\nThe documentation is hosted on [ReadTheDocs.io](https://yukinator.readthedocs.io/en/latest/)\n\n## Help, questions, and contributing\nAll contributors are very welcome. If you have any questions or a bug to report feel free to open an issue.\n\n## External packages\nYukinator depends on these third-party packages:\n* [attrs](https://www.attrs.org/en/stable/)\n* [requests-cache](https://requests-cache.readthedocs.io/en/stable/)",
    'author': 'brozen',
    'author_email': 'szymon.mazurkievicz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BrozenSenpai/yukinator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
