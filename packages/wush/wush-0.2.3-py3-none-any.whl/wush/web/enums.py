#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
网络相关枚举模块
"""

from wpy.base import BaseEnum

class MethodEnum(BaseEnum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    PATCH = 'PATCH'

class ProtocolEnum(BaseEnum):
    HTTP = 'http'
    HTTPS = 'https'

class HeaderEnum(BaseEnum):
    CONTENT_TYPE = 'Content-Type'
    CONTENT_LENGTH = 'Content-Length'
    LOCATION = 'Location'

class ContentTypeEnum(BaseEnum):
    APPLICATION_JSON = 'application/json'
    TEXT_HTML = 'text/html'

class RequestsParamsEnum(BaseEnum):
    METHOD = 'method'
    URL = 'url'
    PARAMS = 'params'
    JSON = 'json'
    HEADERS = 'headers'
    COOKIES = 'cookies'
