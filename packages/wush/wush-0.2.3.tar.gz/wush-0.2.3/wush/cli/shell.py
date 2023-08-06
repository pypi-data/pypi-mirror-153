#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
#  import argparse
import traceback
import multiprocessing as mp
import pygments

from csarg import CommandArgumentParser
from csarg import CommandArgumentParserFactory
from pygments.lexers.python import PythonLexer
from prompt_toolkit import print_formatted_text
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.history import FileHistory
from wpy.functools import clock

from wush.common.loggers import create_logger
from wush.common.run_mode import RUN_MODE
from wush.common.constants import Constants
from wush.completion.command import CommandCompleter
from wush.config import load_config

from .exceptions import ContinueException
from .exceptions import CommnadNotFoundException
from .server import run_server


class Shell():
    logger = create_logger('Shell')

    parser_dict = {}
    parser = None
    _prompt_default = ''
    web_port = None
    session = None

    def __init__(self):
        self.parser = self._get_parser()
        self.config = load_config()
        self.session = PromptSession(
            completer=CommandCompleter(self.parser),
            # 设置历史记录文件
            history = FileHistory(Constants.HISTORY_PATH),
            auto_suggest = AutoSuggestFromHistory(),
            complete_in_thread=True
        )

    def _get_parser(self, cmd=None):
        if cmd not in self.parser_dict:
            parser = CommandArgumentParserFactory.build_parser(cmd)
            if isinstance(parser, CommandArgumentParser):
                parser.set_prompt(self.session)
            self.parser_dict[cmd] = parser
        return self.parser_dict[cmd]

    def run(self):
        RUN_MODE.set_shell()
        p = mp.Process(target=run_server, daemon=True)
        p.start()
        self._run_shell()
        p.terminate()

    def _run_shell(self):
        while True:
            try:
                #  left_prompt = 'wush/{space}/{module}> '.format(
                    #  space = self.config.space_name,
                    #  module = self.config.module_name
                #  )
                left_prompt = 'wush> '
                right_prompt = ''
                text = self.session.prompt(
                    left_prompt,
                    default = self._prompt_default,
                    rprompt = right_prompt,
                )
                self._run_once_time(text)
            except ContinueException:
                continue
            except CommnadNotFoundException:
                print('command not found: {}'.format(text))
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                self._print('ERROR: ' + str(e))
                self.logger.error(traceback.format_exc())
            self._end_run()

        print('GoodBye!')

    def _end_run(self):
        self._prompt_default = ''

    @clock(fmt = Constants.CLOCK_FMT, logger_func = logger.info)
    def _run_once_time(self, text):
        """运行单次命令"""
        if not text:
            return
        parser = self._get_parser()
        args = parser.parse_args(text)
        cmd = args.cmd
        self.parser = self._get_parser(cmd)
        self.logger.info('run argparser %s', self.parser)

        self._run_base_cmd(text)

        self.logger.info(self.parser)
        if isinstance(self.parser, CommandArgumentParser):
            self.parser.run(text)
            return

        if not hasattr(self, '_' + cmd):
            raise CommnadNotFoundException()

        func = getattr(self, '_' + cmd)
        func(text)

    def _run_base_cmd(self, text):
        """运行基础命令"""
        if text.startswith('!'):
            text = text[1:]
            try:
                history_num = int(text)
                self.logger.info(history_num)
                cmd = self.get_history_by_num(history_num)
                self._prompt_default = cmd
            except:
                self.logger.error(traceback.format_exc())
                raise CommnadNotFoundException()
            else:
                raise ContinueException()

    def _exit(self, text):
        raise EOFError()

    def get_history_by_num(self, num):
        """获取历史命令"""
        items = self.session.history.get_strings()
        if len(items) < num:
            return None
        return items[num - 1]

    def _test(self, text):
        #  for k, v in os.environ.items():
            #  print(k, v)
        pass

    def _print(self, text):
        tokens = list(pygments.lex(text, lexer=PythonLexer()))
        print_formatted_text(PygmentsTokens(tokens), end='')

