#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
常量模块
"""

import os
import random

from .utils import get_current_module_path

__all__ = ['Constants']

INIT_CONIFG_YML = """
env:
  github_domain: 'api.github.com'
modules:
  - name: github_user
    domain: '${github_domain}'
    protocol: https
    url_prefix: /users
    requests:
      - name: user_profile
        path: /psf
"""

INIT_CONIFG_TEXT = f"""
# wush 工具的配置文档
# env:
{INIT_CONIFG_YML}
"""

class Constants(object):
    TMPDIR = '/tmp/wush'
    BASETYPE_MAP = {
        'str': str,
        'string': str,
        'int': int,
        'list': list,
        'dict': dict,
        'float': float,
    }
    CONFIG_DIR = os.path.expanduser('~/.wush')
    CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.yml')
    HISTORY_PATH = os.path.expanduser('~/.wush_history')
    API_HISTORY_DIR = os.path.expanduser('~/.wush_api_history')
    SERVER_HOST = 'localhost'
    SERVER_PORT = '6060'
    INIT_CONIFG_YML = INIT_CONIFG_YML
    INIT_CONIFG_TEXT = INIT_CONIFG_TEXT
    CLOCK_FMT = '[耗时][{T:0.4f}s] {F}({A}, {K})'

    @classmethod
    def get_sys_config_path(cls):
        return os.path.join(get_current_module_path(), 'config/config.yml')

    @classmethod
    def build_tmpfile(cls, prefix):
        """创建临时文件"""
        return os.path.join(cls.TMPDIR, f'{prefix}.{random.randint(1, 90000)}')

    @classmethod
    def str_to_basetype(cls, text):
        """字符串转为基础类型"""
        if text not in cls.BASETYPE_MAP:
            raise ValueError(f'{text} is not basetype')
        return cls.BASETYPE_MAP[text]

