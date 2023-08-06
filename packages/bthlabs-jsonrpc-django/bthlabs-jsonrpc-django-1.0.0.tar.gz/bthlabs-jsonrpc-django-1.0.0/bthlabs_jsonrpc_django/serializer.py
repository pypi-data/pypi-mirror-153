# -*- coding: utf-8 -*-
# django-jsonrpc-django | (c) 2022-present Tomek Wójcik | MIT License
from bthlabs_jsonrpc_core import JSONRPCSerializer
from django.db.models import QuerySet


class DjangoJSONRPCSerializer(JSONRPCSerializer):
    SEQUENCE_TYPES = (QuerySet, *JSONRPCSerializer.SEQUENCE_TYPES)
