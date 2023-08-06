# -*- coding: utf-8 -*-
# django-jsonrpc-aiohttp | (c) 2022-present Tomek Wójcik | MIT License
import logging

from bthlabs_jsonrpc_core import Executor, JSONRPCAccessDeniedError
from bthlabs_jsonrpc_core.exceptions import JSONRPCParseError

LOGGER = logging.getLogger('bthlabs_jsonrpc.aiohttp.executor')


class AioHttpExecutor(Executor):
    def __init__(self, request, can_call, namespace=None):
        super().__init__(namespace=namespace)
        self.request = request
        self.can_call = can_call

    async def list_methods(self, *args, **kwargs):
        return super().list_methods()

    async def deserialize_data(self, request):
        try:
            return await request.json()
        except Exception as exception:
            LOGGER.error('Error deserializing RPC call!', exc_info=exception)
            raise JSONRPCParseError()

    def enrich_args(self, args):
        return [self.request, *super().enrich_args(args)]

    async def before_call(self, method, args, kwargs):
        can_call = await self.can_call(self.request, method, args, kwargs)
        if can_call is False:
            raise JSONRPCAccessDeniedError(data='can_call')

    async def execute(self):
        with self.execute_context() as execute_context:
            data = await self.deserialize_data(self.request)

            calls = self.get_calls(data)
            for call in calls:
                with self.call_context(execute_context, call) as call_context:
                    if call_context.is_valid is True:
                        await self.before_call(
                            call_context.method,
                            call_context.args,
                            call_context.kwargs,
                        )

                        call_context.result = await call_context.handler(
                            *call_context.args, **call_context.kwargs,
                        )

        return execute_context.serializer
