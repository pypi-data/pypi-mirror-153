#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""
import os
import json
from csarg import Action
from csarg import CommandArgumentParserFactory

from wush.common import utils
from wush.common.config_value import ConfigValue
from wush.common.loggers import create_logger

from .command import CmdArgumentParser


@CommandArgumentParserFactory.register()
class AliasArgumentParser(CmdArgumentParser):
    cmd = 'alias'
    logger = create_logger('AliasArgumentParser')

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('-v', '--value', help='命令参数')
        item.add_argument('-n', '--name', help='命令别名')
        item.add_argument('--env', action = Action.APPEND.value,
            help='传递环境变量')

        item.alias_path = os.path.expanduser('~/.wush_aliases')

        return item

    def get_completions_after_argument(self, word_for_completion):
        """
        获取补全的单词列表
        :param word_for_completion: 补全需要的单词
        """
        words = []
        if not self.argument:
            return words
        arg = self.argument
        if word_for_completion == '--name':
            # TODO 针对 --name 参数的自动补全
            requests = self.config.get_requests(arg.module)
            words = []
            for req in requests:
                words.append(dict( text = req.name, display_meta=req.title))
            return words
        return super().get_completions_after_argument(word_for_completion)

    def run_command(self, args):
        """运行命令行模式"""
        args = self.parse_args(args)

        data = self.get_aliases()
        if args.value:
            if not args.name:
                print("缺少必要参数 --name")
                return
            data[args.name] = args.value
            text = '\n'.join([json.dumps({k: v}) for k, v in data.items()])
            with open(self.alias_path, 'w') as f:
                f.write(text)
            return

        if args.name:
            environs = utils.list_key_val_to_dict(args.env or [])
            value = data.get(args.name)
            if not value:
                print(f"alias: {args.name} not found")
                return
            value = ConfigValue(value).set_env(**environs).format()
            os.system(f'wush {value}')
            return

        for name, value in data.items():
            print(f'{name}={value}')

    def get_aliases(self):
        if not os.path.exists(self.alias_path):
            return {}
        with open(self.alias_path, 'r') as f:
            lines = f.readlines()

        data = {}
        for line in lines:
            try:
                item = json.loads(line)
                data.update(item)
            except Exception as e:
                print(e)

        return data

    def run_shell(self, args):
        self.run_command(args)

