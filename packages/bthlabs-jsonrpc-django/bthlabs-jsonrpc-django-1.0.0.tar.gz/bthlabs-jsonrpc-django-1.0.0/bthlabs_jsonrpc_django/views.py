# -*- coding: utf-8 -*-
# django-jsonrpc-django | (c) 2022-present Tomek Wójcik | MIT License
import typing

from bthlabs_jsonrpc_core import Executor
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import classonlymethod
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from bthlabs_jsonrpc_django.executor import DjangoExecutor


class JSONRPCView(View):
    """
    The JSONRPC View. This is the main JSONRPC entry point. Use it to register
    your JSONRPC endpoints.

    Example:

    .. code-block:: python

        from bthlabs_jsonrpc_django import JSONRPCView, is_authenticated

        urlpatterns = [
            path(
                'rpc/private',
                JSONRPCView.as_view(
                    auth_checks=[is_authenticated],
                    namespace='admin',
                ),
            )
            path('rpc', JSONRPCView.as_view()),
        ]
    """

    # pragma mark - Private class attributes

    # The executor class.
    executor: Executor = DjangoExecutor

    # pragma mark - Public class attributes

    #: List of auth check functions.
    auth_checks: list[typing.Callable] = []

    #: Namespace of this endpoint.
    namespace: typing.Optional[str] = None

    # pragma mark - Private interface

    def ensure_auth(self, request: HttpRequest) -> None:
        """
        Runs auth checks (if any) and raises
        :py:exc:`django.core.exceptions.PermissionDenied` if any of them
        returns ``False``.

        :meta private:
        """
        if len(self.auth_checks) == []:
            return

        has_auth = all((
            auth_check(request)
            for auth_check
            in self.auth_checks
        ))
        if has_auth is False:
            raise PermissionDenied('This RPC endpoint requires auth.')

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Dispatches the *request*.

        :meta private:
        """
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed,
            )
        else:
            handler = self.http_method_not_allowed

        self.ensure_auth(request)

        return handler(request, *args, **kwargs)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        The POST handler.

        :meta private:
        """
        executor = self.executor(
            request, self.can_call, self.namespace,
        )

        serializer = executor.execute(request.body)
        if serializer is None:
            return HttpResponse('')

        return JsonResponse(serializer.data, safe=False)

    # pragma mark - Public interface

    @classonlymethod
    def as_view(cls, **initkwargs):
        result = super().as_view(**initkwargs)

        return csrf_exempt(result)

    def can_call(self,
                 request: HttpRequest,
                 method: str,
                 args: list,
                 kwargs: dict) -> bool:
        """
        Hook for subclasses to perform additional per-call permissions checks
        etc. The default implementation returns ``True``.
        """
        return True
