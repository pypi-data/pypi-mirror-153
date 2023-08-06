#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""
from csarg import CommandArgumentParserFactory

from wush.common.constants import Constants
from wush.common.loggers import create_logger
from .command import CmdArgumentParser


@CommandArgumentParserFactory.register()
class HistoryArgumentParser(CmdArgumentParser):
    cmd = 'history'
    logger = create_logger()

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        return item

    def run_shell(self, text):
        items = self._prompt.history.get_strings()
        self._print_historys(items)

    def run_command(self, text):
        with open(Constants.HISTORY_PATH, 'r') as f:
            lines = f.readlines()

        historys = []
        for line in lines:
            if not line.startswith('+'):
                continue
            historys.append(line.strip('\n')[1:])

        self._print_historys(historys)

    def _print_historys(self, historys: list):
        history_max_num_len = len(str(len(historys)))
        for i, item in enumerate(historys):
            show_index = i + 1
            show_index_fmt = '{{:<{}d}}'.format(history_max_num_len)
            line = '{} {}'.format(show_index_fmt.format(show_index), item)
            self._print(line)

