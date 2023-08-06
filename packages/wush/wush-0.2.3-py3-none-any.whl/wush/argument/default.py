#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""

from .command import CmdArgumentParser

class DefaultArgumentParser(CmdArgumentParser):
    cmd = 'default'

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--config')
        item.add_argument('--module')
        item.add_argument('--space')
        return item

