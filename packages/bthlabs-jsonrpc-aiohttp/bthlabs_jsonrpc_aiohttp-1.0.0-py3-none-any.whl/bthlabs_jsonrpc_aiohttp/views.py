# -*- coding: utf-8 -*-
# django-jsonrpc-aiohttp | (c) 2022-present Tomek Wójcik | MIT License
import typing

from aiohttp import web

from bthlabs_jsonrpc_aiohttp.executor import AioHttpExecutor


class JSONRPCView:
    """
    The JSONRPC View. This is the main JSONRPC entry point. Use it to register
    your JSONRPC endpoints.

    Example:

    .. code-block:: python

        from bthlabs_jsonrpc_aiohttp import JSONRPCView

        app.add_routes([
            web.post('/rpc', JSONRPCView()),
            web.post('/example/rpc', JSONRPCView(namespace='examnple')),
        ])
    """

    # pragma mark - Public interface

    def __init__(self, namespace: typing.Optional[str] = None):
        self.namespace: typing.Optional[str] = namespace

    async def can_call(self,
                       request: web.Request,
                       method: str,
                       args: list,
                       kwargs: dict) -> bool:
        """
        Hook for subclasses to perform additional per-call permissions checks
        etc. The default implementation returns ``True``.
        """
        return True

    async def __call__(self, request: web.Request) -> web.Response:
        """The request handler."""
        executor = AioHttpExecutor(
            request, self.can_call, namespace=self.namespace,
        )

        serializer = await executor.execute()
        if serializer is None:
            return web.Response(body='')

        return web.json_response(serializer.data)
