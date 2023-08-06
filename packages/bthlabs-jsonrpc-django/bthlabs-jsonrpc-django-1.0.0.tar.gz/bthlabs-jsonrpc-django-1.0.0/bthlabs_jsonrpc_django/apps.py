# -*- coding: utf-8 -*-
# django-jsonrpc-django | (c) 2022-present Tomek Wójcik | MIT License
import importlib

from django.apps import AppConfig


class BTHLabsJSONRPCConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bthlabs_jsonrpc_django'
    verbose_name = 'BTHLabs JSONRPC'

    def ready(self):
        from django.conf import settings

        for module_path in settings.JSONRPC_METHOD_MODULES:
            _ = importlib.import_module(module_path)
