#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""

from csarg import CommandArgumentParserFactory

from wush.cli.server import run_server
from .command import CmdArgumentParser

__all__ = ['ServerArgumentParser']

@CommandArgumentParserFactory.register()
class ServerArgumentParser(CmdArgumentParser):
    cmd = 'server'

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('-c', '--config', help='Config dir name')
        return item

    def run_shell(self, text):
        pass

    def run_command(self, text):
        run_server(clear_logger = False)

