# -*- coding: utf-8 -*-
# django-jsonrpc-django | (c) 2022-present Tomek Wójcik | MIT License
import typing

from django.http import HttpRequest


def is_authenticated(request: HttpRequest) -> bool:
    """Checks if the request user is authenticated and active."""
    return all((
        request.user.is_anonymous is False,
        request.user.is_active is True,
    ))


def is_staff(request: HttpRequest) -> bool:
    """Checks if the request user is a staff user."""
    return request.user.is_staff


def has_perms(perms: list[str]) -> typing.Callable:
    """Checks if the request user has the specified permissions."""

    def internal_has_perms(request: HttpRequest) -> bool:
        return request.user.has_perms(perms)

    return internal_has_perms
