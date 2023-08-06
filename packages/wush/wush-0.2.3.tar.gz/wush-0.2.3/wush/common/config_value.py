#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import json
import os
import re
from functools import singledispatch

from wpy.path import read_dict
from wush.common.loggers import create_logger
#  from wush.model import Model

__all__ = ['environ_keys', 'ConfigValue']

#  _REG_ENV = r'(\${.*?})'
#  _REG_ENV = r'\{(.+?)\}'
_REG_ENV2 = r'\${(.+?)\}'

@singledispatch
def environ_keys(obj):
    """获取环境变量 keys"""
    if not hasattr(obj, '__annotations__'):
        return
    res = set()
    for key in obj.__annotations__.keys():
        env_keys = environ_keys(getattr(obj, key))
        for _key in env_keys:
            res.add(_key)

    return res

@environ_keys.register(str)
def _(text):
    return set(re.findall(_REG_ENV2, text))

@environ_keys.register(dict)
def _(data):
    res = set()
    for key, value in data.items():
        for name in environ_keys(key):
            if name not in res:
                res.add(name)
        for name in environ_keys(value):
            if name not in res:
                res.add(name)
    return res

@environ_keys.register(list)
def _(data):
    res = set()
    for line in data:
        for name in environ_keys(line):
            if name not in res:
                res.add(name)
    return res

#  @environ_keys.register(Model)
#  def _(model):
    #  res = set()
    #  for value in model.dict().values():
        #  for name in environ_keys(value):
            #  if name not in res:
                #  res.add(name)
    #  return res

class ConfigValue():
    logger = create_logger('ConfigValue')

    def __init__(self, value):
        self.value = value

        #  self.REG_ENV = r'(\${.*?})'
        #  self.REG_ENV2 = r'({.*?})'
        self.REG_PARSE = r'(^\b(json|yml|xml)\b@.*?)'
        self.env = dict(os.environ)
        self.functions = {}

    def set_env(self, **data):
        self.env.update(data)
        return self

    def set_functions(self, **data):
        self.functions.update(data)
        return self

    def format(self):
        '''输出格式化信息'''
        return self._format(self.value)

    def _format(self, value):
        if not value:
            # 为空，返回
            return value

        #  格式化响应格式数据
        for t in (str, list, dict):
            if isinstance(value, t):
                func_name = '_format_' + t.__name__
                return getattr(self, func_name)(value)

        # 格式化模型
        #  if isinstance(value, Model):
            #  for k, v in value.to_dict().items():
                #  v = self._format(v)
                #  setattr(value, k, v)
            #  return value

        #  if isinstance(value, BaseObject):
            #  for k, v in value.to_dict().items():
                #  v = self._format(v)
                #  setattr(value, k, v)

        self._format_object(value)
        return value

    def _format_object(self, obj):
        if not hasattr(obj, '__annotations__'):
            return
        for key in obj.__annotations__.keys():
            if not hasattr(obj, key):
                continue
            val = ConfigValue(getattr(obj, key)).set_env(**self.env
                ).set_functions(**self.functions).format()
            setattr(obj, key, val)

    def _format_dict(self, value):
        """格式化字典"""
        for v_k, v_v in value.items():
            value[v_k] = ConfigValue(v_v).set_env(**self.env
                    ).set_functions(**self.functions).format()
        return value

    def _format_list(self, lines):
        """格式化数组"""
        for i in range(len(lines)):
            lines[i] = ConfigValue(lines[i]).set_env(**self.env
                    ).set_functions(**self.functions).format()
        return lines

    def _format_str(self, text):
        '''格式化字符串'''
        if self._has_environs(text):
            text = self._format_environ(text)
        if text.startswith('@'):
            text = text[1:]
            #  self.logger.debug(text)
            if text.startswith('{') and text.endswith('}'):
                return json.loads(text)
            if text.startswith('[') and text.endswith(']'):
                return json.loads(text)

            if not self._is_file(text):
                raise ValueError(u'{} 文件路径不存在'.format(text))

            return self._format_file_content(text)

        parse_type = self._get_parse_type(text)
        if parse_type:
            text = text[len(parse_type) + 1:]
            if self._is_file(text):
                if parse_type == 'json':
                    return read_dict(text)
            else:
                if parse_type == 'json':
                    return json.loads(text)

        return text

    def _get_parse_type(self, text):
        """获取解析类型"""
        lines = re.findall(self.REG_PARSE, text)
        if not lines:
            return None
        return lines[0][-1]

    def _format_file_content(self, filepath):
        '''格式化文件内容'''
        if filepath.endswith('.json') or filepath.endswith('.yml'):
            return read_dict(filepath)

        with open(filepath, 'r') as f:
            lines = f.readlines()
            if not lines:
                return ''
            if lines[0].startswith('{') and lines[-1].endswith('}'):
                return read_dict(filepath)
            return ''.join(lines)

    def _is_file(self, filepath):
        '''是否为文件'''
        return os.path.exists(filepath)

    def _has_environs(self, text):
        '''是否有环境变量'''
        if not isinstance(text, str):
            return False
        self.environ_names = environ_keys(text)
        return True if self.environ_names else False

    def _replace(self, match):
        """正则替换方法"""
        groups = match.groups()
        if not groups:
            return

        k = groups[0]
        if '(' not  in k and ')' not in k:
            env_value = self.env.get(k, "")
            if isinstance(env_value, dict) or isinstance(env_value, list):
                return json.dumps(env_value)
            return str(env_value)

        k = k.strip(')').strip(' ')
        func_name, args_str = k.split('(')
        func = self.functions.get(func_name)
        #  self.logger.info(f'func_name {func_name} {func}')

        if not func:
            return
        if not args_str:
            args_str = '()'
        else:
            args_str = '({},)'.format(args_str)
        args = eval(args_str)
        repl = func(*args)
        repl = str(repl)
        return repl

    def _format_environ(self, text):
        '''格式化环境变量'''
        if not self.environ_names:
            return text

        text = re.sub(_REG_ENV2, self._replace, text)
        #  text = re.sub(_REG_ENV, self._replace, text)
        return text

if __name__ == "__main__":
    text_value = {"name": "wxnacy"}
    text = 'json@${text_value}'
    data = ConfigValue(text).set_env(text_value = text_value).format()
    assert data == {"name": "wxnacy"}
