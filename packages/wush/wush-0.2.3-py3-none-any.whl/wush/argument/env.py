#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import argparse
import os
from collections import deque

from wpy.path import (
    read_dict, write_yml
)
from csarg import Action
from csarg import CommandArgumentParserFactory

from wush.config import load_config
from wush.argument.command import CmdArgumentParser

def init_argparse():
    """初始化参数"""
    parser = argparse.ArgumentParser(description='Wush command',)
    parser.add_argument('cmd', help='You can use run, body, env, module')
    parser.add_argument('-a', '--add', help='Config dir name', action='append')
    parser.add_argument('-v', '--verbose', help='Config dir name')
    parser.add_argument('-s', '--save', help='Config dir name')
    parser.add_argument('-f', '--file', action='store_true',
            help='Config dir name')
    return parser

@CommandArgumentParserFactory.register()
class EnvArgumentParser(CmdArgumentParser):
    cmd = 'env'

    def get_completions_after_argument(self, word_for_completion):
        """
        获取补全的单词列表
        :param word_for_completion: 补全需要的单词
        """
        if word_for_completion == '--add':
            words = []
            for k, v in self.config.env.items():
                text = '{}='.format(k)
                display = '{}={}'.format(k, v)
                words.append(dict(text = text, display = display))
            return words

        return super().get_completions_after_argument(word_for_completion)

    def _make_args_dict(self, args):
        res = super()._make_args_dict(args)
        args = list(filter(lambda x: x != '--save', args))
        if len(args) < 3:
            return res
        # 将所有成对的参数都放入参数列表
        d_args = deque(args[1:])
        d_args.rotate(-1)
        for i, (k, v) in enumerate(zip(args[1:], d_args)):
            if i % 2  == 1 or not k.startswith('--'):
                continue
            k = k.replace('--', '')
            res[k] = v
        return res

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--save', action=Action.STORE_TRUE.value,
            help="保存环境变量")
        item.add_argument('--add', action=Action.APPEND.value,
            help="添加环境变量")

        item.sys_parser = init_argparse()
        item.config = load_config()

        return item

    def run(self, args):
        """执行"""
        self.logger.info(args)
        # TODO 替换本身的 argparse
        args_list = args.split(' ')
        args_list.append('--file')
        sys_args = self.sys_parser.parse_args(args_list)

        args = self.parse_args(args)
        for arg in self.get_arguments():
            self.logger.info(f'{self.cmd} {arg.name} {getattr(args, arg.name)}')
        if sys_args.add:
            for key_val in sys_args.add:
                key, val = key_val.split('=')
                self.config.add_env(key, val)
                # 写入当前环境变量
                # TODO 需要禁止修改敏感字段
                os.environ[key] = val

        output = {
            'headers': [
                { "display": "Key" },
                { "display": "Value" },
                ],
            "items": []
            }
        for k, v in self.config.env.items():
            line = (k, v)
            output['items'].append(line)
        self.config.function.print_table(output)

        # TODO 保存数据去掉 wapi
        # 保存数据
        if args.save:
            env_path = self.wapi.config.get_env_path()
            env_data = {}
            try:
                env_data = read_dict(env_path)
            except:
                pass
            for k, v in self.wapi.config.env.dict().items():
                if k in ('body_path',):
                    continue
                if k.isupper():
                    continue
                if not v:
                    continue
                if env_data.get(k) == v:
                    continue
                self.logger.info('Env save %s=%s', k, v)
                env_data[k] = v
            write_yml(env_path, env_data)

    def run_shell(self, args):
        self.run(args)

    def run_command(self, args):
        self.run(args)
