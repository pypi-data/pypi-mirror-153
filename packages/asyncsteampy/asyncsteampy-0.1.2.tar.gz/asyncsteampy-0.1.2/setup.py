# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncsteampy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'beautifulsoup4>=4.10.0,<5.0.0', 'rsa>=4.8,<5.0']

setup_kwargs = {
    'name': 'asyncsteampy',
    'version': '0.1.2',
    'description': 'Simple library to trade and interact with steam market, webapi, guard',
    'long_description': '# <p align="center">Asyncsteampy</p>\n\n[![license](https://img.shields.io/github/license/somespecialone/asyncsteampy)](https://github.com/somespecialone/asyncsteampy/blob/master/LICENSE)\n[![pypi](https://img.shields.io/pypi/v/asyncsteampy)](https://pypi.org/project/asyncsteampy)\n[![Tests](https://github.com/somespecialone/asyncsteampy/actions/workflows/tests.yml/badge.svg)](https://github.com/somespecialone/asyncsteampy/actions/workflows/tests.yml)\n[![codecov](https://codecov.io/gh/somespecialone/asyncsteampy/branch/master/graph/badge.svg?token=H3JL81SL7P)](https://codecov.io/gh/somespecialone/asyncsteampy)\n[![CodeFactor](https://www.codefactor.io/repository/github/somespecialone/asyncsteampy/badge)](https://www.codefactor.io/repository/github/somespecialone/asyncsteampy)\n[![versions](https://img.shields.io/pypi/pyversions/asyncsteampy)](https://pypi.org/project/asyncsteampy)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![steam](https://shields.io/badge/steam-1b2838?logo=steam)](https://store.steampowered.com/)\n\n> ### This library is a soft fork of [bukson/steampy](https://github.com/bukson/steampy) ⚠ and created only to provide asynchronous methods and proxies support.\n> #### Docs, examples you can read from original [README](https://github.com/bukson/steampy#readme). Differences of usage and new features listed below 📖\n> #### Must work with python 3.6 and above like origin, but tested only on `3.10` ⚡\n---\n\n## Navigation\n\n- [**Installation**](#installation)\n- [**Login&Init**](#logininit)\n- [**AsyncIO**](#asyncio)\n- [**Proxy support**](#proxy-support)\n- [**Tests**]()\n\n---\n\n## Installation\n\n```shell\npip install asyncsteampy\n\npipenv install asyncsteampy\n\npoetry add asyncsteampy\n```\n\n## Login&Init\n\nNow you don\'t need to pass `username`, `password`, `steamguard` args to `login` method, you can do this in constructor.\n\n```python\nfrom asyncsteampy.client import SteamClient as AsyncSteamClient\n\nasync_steam_client = AsyncSteamClient(\'MY_USERNAME\', \'MY_PASSWORD\', \'PATH_TO_STEAMGUARD_FILE/STEAMGUARD_DICT\',\n                                      api_key="API_KEY")\n```\n\nInstead of passing `str` path or `pathlib.Path` to `steamguard.txt` file or even json serialized string you can just use\ndict object:\n\n```py\nsteamguard = {\n    "steamid": "YOUR_STEAM_ID_64",\n    "shared_secret": "YOUR_SHARED_SECRET",\n    "identity_secret": "YOUR_IDENTITY_SECRET",\n}\n```\n\n## AsyncIO\n\nAll methods that require connection to steam network now have asyncio support (it\nuses [aiohttp](https://github.com/aio-libs/aiohttp)) and are asynchronous : `client`, `market`, `chat`.\n\n```py\nfrom asyncsteampy.client import SteamClient as AsyncSteamClient\n\nasync_steam_client = AsyncSteamClient(\'MY_USERNAME\', \'MY_PASSWORD\', \'PATH_TO_STEAMGUARD_FILE/STEAMGUARD_DICT\',\n                                      api_key="API_KEY")\nawait async_steam_client.login()\nbuy_order_id = "some_buy_order_id"\nresponse = await async_steam_client.market.cancel_buy_order(buy_order_id)\n# do other async work\nawait async_steam_client.close()\n```\n\nIf you end your operations, ⚠️ `keep in mind`, you always need to close your `async_steam_client`. This will do `logout`\nand close `aiohttp` [session](https://docs.aiohttp.org/en/stable/client_reference.html#client-session) properly. Also,\nyou can `await async_steam_client.logout()` without closing session if you need this for some reason.\n\nAsync context manager usage example:\n\n```py\nfrom asyncsteampy.client import SteamClient as AsyncSteamClient\n\nasync with AsyncSteamClient(\'MY_USERNAME\', \'MY_PASSWORD\', \'PATH_TO_STEAMGUARD_FILE/STEAMGUARD_DICT\',\n                            api_key="API_KEY") as async_steam_client:\n    await async_steam_client.do_what_you_need()\n```\n\nThere you don\'t need to call `close`, async context manager do it automatically when execution passes the block of code.\n\n## Proxy support\n\nIf your proxy type is socks4/5 you should look at this small but precious\nlibrary [aiohttp-socks](https://github.com/romis2012/aiohttp-socks), if proxy type http/https, or you don\'t\nlike `aiohttp-socks` you can use [aiohttp-proxy](\nhttps://github.com/Skactor/aiohttp-proxy) instead.\n\n```python\nimport aiohttp\nfrom aiohttp_socks import ProxyConnector\n\nfrom asyncsteampy.client import SteamClient as AsyncSteamClient\n\nconnector = ProxyConnector.from_url(\'proxy_type://proxy_url_with_or_no_auth\')\nsession_with_proxy = aiohttp.ClientSession(connector=connector)\n\n# Finally, pass session object in AsyncSteamClient\n\nasync_steam_client = AsyncSteamClient(..., session=session_with_proxy)\nasync with AsyncSteamClient(..., session=session_with_proxy) as async_steam_client:\n    ...\n```\n\n## Tests\n\nTo run tests clone repo, install with dev dependencies\n\n```shell\npoetry install\n```\n\nCreate env variables listed in [tests/data](tests/data.py) and run `pytest` from project dir:\n\n```shell\npytest\n```\n',
    'author': 'somespecialone',
    'author_email': 'tkachenkodmitriy@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/somespecialone/asyncsteampy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
