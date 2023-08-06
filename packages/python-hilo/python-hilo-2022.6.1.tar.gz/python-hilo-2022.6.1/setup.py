# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhilo', 'pyhilo.device', 'pyhilo.util']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0',
 'aiosignal>=1.2.0',
 'async-timeout>=4.0.0',
 'attrs>=21.2.0',
 'backoff>=1.11.1',
 'python-dateutil>=2.8.2',
 'ruyaml>=0.91.0',
 'voluptuous>=0.13.1',
 'websockets>=8.1,<11.0']

setup_kwargs = {
    'name': 'python-hilo',
    'version': '2022.6.1',
    'description': 'A Python3, async interface to the Hilo API',
    'long_description': '[![Total alerts](https://img.shields.io/lgtm/alerts/g/dvd-dev/python-hilo.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/dvd-dev/python-hilo/alerts/)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/dvd-dev/python-hilo.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/dvd-dev/python-hilo/context:python)\n\n# python-hilo\n\n`python-hilo` (aka `pyhilo`) is a Python 3.9, `asyncio`-driven interface to the unofficial\nHilo API from Hydro Quebec. This is meant to be integrated into Home Assistant.\n\nNothing is fully functional right now except for the PoC. Before this package, the Hilo API\nwas returning all information via some REST calls. Since the end of 2021, Hilo has deprecated\nsome of the endpoints including the ones that returns the status of the devices. This was\nreplaced with a websocket system using Google Firebase.\n\n## Running the PoC\n\n```\n$ python -m virtualenv .venv\n$ source .venv/bin/activate\n$ pip install -r requirements.txt\n$ cat << EOF > .env\nexport hilo_username="moi@gmail.com"\nexport hilo_password="secretpassword"\n$ source .env\n$ ./test.py\n```\n\nHome assistant integration is available [here](https://github.com/dvd-dev/hilo)\n\n## TODO\n- Type everything: almost done, got a few "type: ignore" to fix\n\n## Later?\n- Full docstrings and doc generation\n- Unit testing\n- Functional testing\n\nIf anyone wants to contribute, feel free to submit a PR. If you\'d like to sync up first, you can\nfire me an email me@dvd.dev\n',
    'author': 'David Vallee Delisle',
    'author_email': 'me@dvd.dev',
    'maintainer': 'David Vallee Delisle',
    'maintainer_email': 'me@dvd.dev',
    'url': 'https://github.com/dvd-dev/python-hilo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
