#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
#  import abc
from datetime import datetime
import pygments

#  from pygments.token import Token
from pygments.lexers.python import PythonLexer
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit import print_formatted_text

from csarg import CommandArgumentParser

from wpy.functools import clock
from wush.common.constants import Constants
from wush.common.loggers import create_logger
from wush.common.run_mode import RUN_MODE
from wush.config import load_config

class CmdArgumentParser(CommandArgumentParser):
    logger = create_logger('CmdArgumentParser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def get_completions_after_argument(self, word_for_completion):
        """
        获取补全的单词列表
        :param word_for_completion: 补全需要的单词
        """
        return []

    def get_completions_after_cmd(self, argument, words=None):
        """获取补全使用的单词列表"""
        res = []
        if words and isinstance(words, list):
            res.extend(words)
        args = self.get_arguments()
        for arg in args:
            if arg.is_cmd:
                continue
            # 已经赋值的不需要展示
            # 列表除外
            if arg.is_set and not arg.is_list:
                continue
            res.append(dict(text = '--' + arg.name, display_meta = arg.help))
        return res

    def parse_args(self, text):
        """解析参数"""
        args = super().parse_args(text)

        # 输出日志
        arg_dict = {}
        arg_list = self.get_arguments()
        for arg in arg_list:
            #  log_text = f'{self.cmd} argument {arg.name}' \
                #  f' {getattr(args, arg.name.replace("-", "_"))}'
            arg_dict[arg.name] = getattr(args, arg.name.replace('-', '_'))
            #  self.logger.info(log_text)
        self.logger.info(f'{self.cmd} arguments {arg_dict}')
        return args

    def _print(self, text):
        tokens = list(pygments.lex(text, lexer=PythonLexer()))
        print_formatted_text(PygmentsTokens(tokens), end='')

    @clock(fmt = Constants.CLOCK_FMT, logger_func = logger.info)
    def run(self, args):
        begin_text = "cmd begin "
        self.logger.info(f"{begin_text:=<50}")
        self.config = load_config()

        # 添加历史记录
        if RUN_MODE.is_command:
            self.add_history(args)

        func_name = f'run_{RUN_MODE.mode}'
        func = None
        if hasattr(self, func_name):
            func = getattr(self, func_name)
        else:
            # 如果没有提供模式专用函数，则使用默认 run 方法
            if not hasattr(self, 'run'):
                raise RuntimeError('找不到参数运行方法')
            func = getattr(self, 'run')

        func(args)
        end_text = "cmd end "
        self.logger.info(f"{end_text:=<50}")

    @classmethod
    def add_history(cls, cmd):
        if isinstance(cmd, list):
            cmd = ' '.join(cmd)

        cmd.strip()

        if cmd.startswith('history'):
            return

        with open(Constants.HISTORY_PATH, 'r') as f:
            lines = f.readlines()

        historys = []
        for line in lines:
            if not line.startswith('+'):
                continue
            historys.append(line.strip('\n')[1:])

        if historys and historys[-1] == cmd:
            return

        lines = []
        lines.append(f"\n# {str(datetime.now())}")
        lines.append(f"\n+{cmd}\n")
        with open(Constants.HISTORY_PATH, 'a') as f:
            f.write(''.join(lines))

