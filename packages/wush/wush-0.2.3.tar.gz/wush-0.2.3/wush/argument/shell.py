#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""

from csarg import CommandArgumentParserFactory

from wush.cli.shell import Shell
from .command import CmdArgumentParser

__all__ = ['ShellArgumentParser']

@CommandArgumentParserFactory.register()
class ShellArgumentParser(CmdArgumentParser):
    cmd = 'shell'

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('-c', '--config', help='Config dir name')
        return item

    def run(self, text):
        shell = Shell()
        shell.run()
