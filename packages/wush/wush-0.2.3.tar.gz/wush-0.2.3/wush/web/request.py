#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

import requests
import json

from requests import Response
from wpy.functools import clock

from wush.common.constants import Constants
from wush.common.loggers import get_logger
from wush.web.response import ResponseClient
from .models import RequestBuilder

__all__ = ['RequestClient']


class RequestClient:
    """请求客户端"""
    logger = get_logger('RequestClient')

    builder: RequestBuilder

    def __init__(self, builder: RequestBuilder):
        self.builder = builder

    def request(self) -> ResponseClient:
        """发送请求"""
        params = self.builder.to_requests()
        self.logger.info(f'request builder {json.dumps(params, indent=4)}')
        res = self._request(**params)
        res_client = ResponseClient(self.builder, res)
        if res_client.status_code in (301, 302):
            url = res_client.headers.location
            params['url'] = url
            res = self._request(**params)
            res_client = ResponseClient(self.builder, res)

        return res_client

    #  @clock(fmt = Constants.CLOCK_FMT, logger_func = logger.info)
    def _request(self, **params) -> Response:
        res = requests.request(**params)
        elapsed = res.elapsed.total_seconds()
        method = params.get('method')
        url = params.get('url')
        self.logger.info(f'{method} {url} elapsed {elapsed}')
        return res

