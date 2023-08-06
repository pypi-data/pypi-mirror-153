bthlabs-jsonrpc-aiohttp
=======================

BTHLabs JSONRPC - aiohttp integration

`Docs`_ | `Source repository`_

Overview
--------

BTHLabs JSONRPC is a set of Python libraries that provide extensible framework
for adding JSONRPC interfaces to existing Python Web applications.

The *aiohttp* package provides aiohttp integration.

Installation
------------

.. code-block:: shell

    $ pip install bthlabs_jsonrpc_aiohttp

Example
-------

.. code-block:: python

    # app.py
    from aiohttp import web
    from bthlabs_jsonrpc_core import register_method

    from bthlabs_jsonrpc_aiohttp import JSONRPCView

    @register_method('hello')
    async def hello(request, who='World'):
        return f'Hello, {who}!'

    app = web.Application()
    app.add_routes([
        web.post('/rpc', JSONRPCView()),
    ])

Author
------

*bthlabs-jsonrpc-aiohttp* is developed by `Tomek Wójcik`_.

License
-------

*bthlabs-jsonrpc-aiohttp* is licensed under the MIT License.

.. _Docs: https://projects.bthlabs.pl/bthlabs-jsonrpc/aiohttp/
.. _Source repository: https://git.bthlabs.pl/tomekwojcik/bthlabs-jsonrpc/
.. _Tomek Wójcik: https://www.bthlabs.pl/
