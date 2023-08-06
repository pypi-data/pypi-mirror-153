# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aioxmlrpc']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'aioxmlrpc',
    'version': '0.6.4',
    'description': 'Source code of Sequoia API TLDPublic',
    'long_description': "=========\naioxmlrpc\n=========\n\n.. image:: https://github.com/mardiros/aioxmlrpc/actions/workflows/main.yml/badge.svg\n   :target: https://github.com/mardiros/aioxmlrpc/actions/workflows/main.yml\n\n\n.. image:: https://codecov.io/gh/mardiros/aioxmlrpc/branch/master/graph/badge.svg?token=BR3KttC9uJ\n   :target: https://codecov.io/gh/mardiros/aioxmlrpc\n\n\nGetting Started\n===============\n\nAsyncio version of the standard lib ``xmlrpc``\n\nCurrently only ``aioxmlrpc.client``, which works like ``xmlrpc.client`` but\nwith coroutine is implemented.\n\nFill free to fork me if you want to implement the server part.\n\n\n``aioxmlrpc`` is based on ``httpx`` for the transport, and just patch\nthe necessary from the python standard library to get it working.\n\n\nInstallation\n------------\n\n::\n\n    pip install aioxmlrpc\n\n\nExample of usage\n----------------\n\nThis example show how to print the current version of the Gandi XML-RPC api.\n\n\n::\n\n    import asyncio\n    from aioxmlrpc.client import ServerProxy\n\n\n    @asyncio.coroutine\n    def print_gandi_api_version():\n        api = ServerProxy('https://rpc.gandi.net/xmlrpc/')\n        result = yield from api.version.info()\n        print(result)\n\n    if __name__ == '__main__':\n        loop = asyncio.get_event_loop()\n        loop.run_until_complete(print_gandi_api_version())\n        loop.stop()\n\n\nRun the example\n\n::\n\n    poetry run examples/gandi_api_version.py\n",
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gauvr.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mardiros/aioxmlrpc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
