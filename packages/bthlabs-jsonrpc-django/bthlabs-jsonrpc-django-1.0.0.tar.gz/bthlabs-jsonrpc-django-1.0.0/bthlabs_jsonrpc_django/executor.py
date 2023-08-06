# -*- coding: utf-8 -*-
# django-jsonrpc-django | (c) 2022-present Tomek Wójcik | MIT License
import typing

from bthlabs_jsonrpc_core import Executor, JSONRPCAccessDeniedError
from django.http import HttpRequest

from bthlabs_jsonrpc_django.serializer import DjangoJSONRPCSerializer


class DjangoExecutor(Executor):
    serializer = DjangoJSONRPCSerializer

    def __init__(self,
                 request: HttpRequest,
                 can_call: typing.Callable,
                 namespace: typing.Optional[str] = None):
        super().__init__(namespace=namespace)
        self.request: HttpRequest = request
        self.can_call: typing.Callable = can_call

    def enrich_args(self, args):
        return [self.request, *super().enrich_args(args)]

    def before_call(self, method, args, kwargs):
        can_call = self.can_call(self.request, method, args, kwargs)
        if can_call is False:
            raise JSONRPCAccessDeniedError(data='can_call')
