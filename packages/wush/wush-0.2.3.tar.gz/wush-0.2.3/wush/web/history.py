#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
请求历史
"""

import os
from wpy.base import BaseObject
from wpy.path import (
    read_dict, write_dict
)

from wush.config import load_config
from wush.web.response import ResponseClient

__all__ = ['History']

class HistoryModel(BaseObject):
    db = 'wush'
    table = 'history'

    version = ''
    request = dict()
    response = dict()

    def save(self, dirname):
        """保存历史"""
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        filepath = os.path.join(dirname, self.version)
        write_dict(filepath, self.to_dict())

    @classmethod
    def find_one(cls, version, dirname):
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        filepath = os.path.join(dirname, version)
        return read_dict(filepath)


class History(object):

    def __init__(self, *args, **kwargs):
        self.config = load_config()

    def save(self, response_client: ResponseClient):
        h = HistoryModel()
        h.version = response_client.request_builder.version
        h._id = h.version
        h.request = response_client.request_builder.to_requests()
        res = {
            'is_json': response_client.is_json,
            'text': response_client.text
        }
        if response_client.is_json:
            res['json'] = response_client.json()
        h.response = res
        h.save(self.config.api_history_dir)

    def read(self, version):
        """读取版本信息"""
        return HistoryModel.find_one(version, self.config.api_history_dir)

