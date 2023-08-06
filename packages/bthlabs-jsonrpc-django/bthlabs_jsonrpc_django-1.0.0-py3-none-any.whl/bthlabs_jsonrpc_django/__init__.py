# -*- coding: utf-8 -*-
# django-jsonrpc-django | (c) 2022-present Tomek Wójcik | MIT License
from .auth_checks import (  # noqa
    has_perms,
    is_authenticated,
    is_staff,
)
from .views import JSONRPCView  # noqa

__version__ = '1.0.0'
