#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
工具模块
"""

import json
import os
import importlib
from importlib.machinery import SourceFileLoader
import subprocess

from wush.common.exceptions import JsonException

__all__ = ['get_current_module_path']

def filter_json(data, rules):
    """
    过滤 json 数据
    :param dict data: 过滤的数据
    :param list rules: 过滤规则，例：{"name"}

    最终拼成的命令格式如下
    echo '{"id": 1, "name": "wxnacy"}' | jq '{"name"}'
    """
    cmd_fmt = "echo '{}' | jq '{}'"
    text = json.dumps(data)
    for rule in rules:
        cmd = cmd_fmt.format(text , rule)
        content, err = run_shell(cmd)
        if err:
            raise JsonException(err)
        return json.loads(content)
    return data

def fmt_path(path):
    """格式化地址"""
    path = os.path.expanduser(path)
    return path

def list_key_val_to_dict(data):
    """
    键值对列表转为字典
    :param data: ['name=wxnacy', 'key=True', 'test']
    :returns { 'name': 'wxnacy', 'key': 'True'  }
    """
    res = {}
    for item in data:
        if '=' in item:
            k, v = item.split('=', 1)
            res[k] = v
    return res

def run_shell(command):
    """运行 shell 语句"""
    res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
        stderr = subprocess.PIPE)
    return res.communicate()

def load_module(module_name):
    """加载模块"""
    if module_name.endswith('.py'):
        name = str(hash(module_name))
        views_module = SourceFileLoader(name,
            module_name).load_module()
    else:
        views_module = importlib.import_module(module_name)
    return views_module

def get_current_module_path():
    """获取当前模块的路径"""
    import wush as _wush
    module_path = _wush.__path__[0]
    return module_path

def open_url(url):
    """打开 url"""
    # TODO 适配更多系统
    os.system(f'open -a "/Applications/Google Chrome.app" "{url}"')
