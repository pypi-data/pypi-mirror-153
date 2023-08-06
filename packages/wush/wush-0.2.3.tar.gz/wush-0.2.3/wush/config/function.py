#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
配置可用的方法模块
"""

import traceback
import os
import hashlib
import json
from typing import (
    Dict, Callable, Any
)

from rich.console import Console
from rich.table import Table
from wpy.base import BaseFactory
from wpy import randoms

from wush.common import utils
from wush.common.loggers import get_logger
from wush.web.cookie import Cookie
from wush.web import ResponseClient

logger = get_logger('function')

__all__ = ['FunctionFactory']

class FunctionFactory(BaseFactory):

    @classmethod
    def get_super_factory(cls):
        factory = cls.get_factory()
        _super_factory = {}
        for key, value in factory.items():
            module = value.__module__
            if module.startswith('wush'):
                _super_factory[key] = value
        return _super_factory

@FunctionFactory.register()
def random_int(length: int, min_int: int=None, max_int: int=None):
    """随机 int 值"""
    return randoms.random_int(length, min_int, max_int)

@FunctionFactory.register()
def random_str(length: int, source=None):
    """随机 int 值"""
    return randoms.random_str(length, source)

@FunctionFactory.register()
def md5(text):
    """计算 md5 摘要"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

@FunctionFactory.register()
def get_completion_words(word_for_completion):
    """获取补全的单词列表"""
    return []

@FunctionFactory.register()
def handler_response(response: ResponseClient):
    """统一处理返回结果"""
    try:
        data = response.json()
        data = json.dumps(data, indent=4, ensure_ascii=False)
    except:
        logger.error(traceback.format_exc())
        data = response.content
    print(data)
    url = response.url
    if response.is_html and not response.request_builder.argument.no_browser:
        print('Html page see in browser')
        utils.open_url(url)


@FunctionFactory.register()
def print_table(config):
    """打印表格
    :param dict config: 表格数据
        结构如下：
        {
            "headers": [
                { "display": "列名", 'width': '列宽度，非必传' }
            ],
            "items": [
                ('列数据, 长度需要和 headers 长度保持一致')
            ]
        }
    """
    console = Console()
    headers = config.get("headers") or []
    table = Table(show_header=True, show_lines=True,
        header_style="bold magenta")
    for header in headers:
        name = header.pop("display", '未命名')
        table.add_column(name, **header)
    items = config.get("items", [])
    for item in items:
        table.add_row(*item)
    console.print(table)
    after_table = config.get("after_table")
    if after_table:
        console.print(after_table)

@FunctionFactory.register()
def get_browser_cookies(domains, cookie_name=None):
    """
    获取浏览器的 cookies
    """
    res = Cookie.get_browser_cookie(*domains) or {}
    if cookie_name:
        return res.get(cookie_name)
    return res

class Function(object):
    get_completion_words = None
    random_int = None
    random_str = None
    handler_response: Callable[[ResponseClient], Any] = None
    test = None

    _functions: Dict[str, Callable] = {}

    def __init__(self, functions):
        self._functions = functions
        for name, func in functions.items():
            if isinstance(func, str):
                raise Exception('func {} can not be str'.format(name))
            setattr(self, name, func)

    def add_function(self, func: Callable):
        """添加方法"""
        setattr(self, func.__name__, func)
        self._functions[func.__name__] = func

    def get_functions(self) -> Dict[str, Callable]:
        """获取方法字段"""
        return self._functions

_super_function = None

def load_super_function():
    """加载 super function"""
    global _super_function
    if not _super_function:
        _super_function = Function(FunctionFactory.get_super_factory())
    return _super_function


_function = None
def load_function():
    """加载全部 function"""
    global _function
    if not _function:
        _function = Function(FunctionFactory.get_factory())
    return _function

if __name__ == "__main__":
    pass
