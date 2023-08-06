# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bthlabs_jsonrpc_aiohttp']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6,<4.0', 'bthlabs-jsonrpc-core==1.0.0']

setup_kwargs = {
    'name': 'bthlabs-jsonrpc-aiohttp',
    'version': '1.0.0',
    'description': 'BTHLabs JSONRPC - aiohttp integration',
    'long_description': "bthlabs-jsonrpc-aiohttp\n=======================\n\nBTHLabs JSONRPC - aiohttp integration\n\n`Docs`_ | `Source repository`_\n\nOverview\n--------\n\nBTHLabs JSONRPC is a set of Python libraries that provide extensible framework\nfor adding JSONRPC interfaces to existing Python Web applications.\n\nThe *aiohttp* package provides aiohttp integration.\n\nInstallation\n------------\n\n.. code-block:: shell\n\n    $ pip install bthlabs_jsonrpc_aiohttp\n\nExample\n-------\n\n.. code-block:: python\n\n    # app.py\n    from aiohttp import web\n    from bthlabs_jsonrpc_core import register_method\n\n    from bthlabs_jsonrpc_aiohttp import JSONRPCView\n\n    @register_method('hello')\n    async def hello(request, who='World'):\n        return f'Hello, {who}!'\n\n    app = web.Application()\n    app.add_routes([\n        web.post('/rpc', JSONRPCView()),\n    ])\n\nAuthor\n------\n\n*bthlabs-jsonrpc-aiohttp* is developed by `Tomek Wójcik`_.\n\nLicense\n-------\n\n*bthlabs-jsonrpc-aiohttp* is licensed under the MIT License.\n\n.. _Docs: https://projects.bthlabs.pl/bthlabs-jsonrpc/aiohttp/\n.. _Source repository: https://git.bthlabs.pl/tomekwojcik/bthlabs-jsonrpc/\n.. _Tomek Wójcik: https://www.bthlabs.pl/\n",
    'author': 'Tomek Wójcik',
    'author_email': 'contact@bthlabs.pl',
    'maintainer': 'BTHLabs',
    'maintainer_email': 'contact@bthlabs.pl',
    'url': 'https://projects.bthlabs.pl/bthlabs-jsonrpc/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
