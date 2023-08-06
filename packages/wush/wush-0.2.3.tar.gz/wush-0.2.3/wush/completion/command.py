#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
命令补全
"""

from prompt_toolkit.completion import Completion

from csarg import CommandArgumentParserFactory
from .base import BaseCompleter
from .word import WordCompleter
from .filesystem import ExecutableCompleter

from wush.common.loggers import create_logger
from wush.config import load_config

__all__ = ['CommandCompleter']

class CommandCompleter(BaseCompleter):
    """shell 环境补全管理"""
    logger = create_logger("CommandCompleter")

    def __init__(self, argparser):
        self.argparser = argparser
        self.path_completer = ExecutableCompleter()
        self.config = load_config()

    def yield_words(self, words):
        """获取命令参数的补全器"""
        if words and isinstance(words[0], dict):
            words = [Completion(**o) for o in words]
        _completer = WordCompleter(words)
        yield from self.yield_completer(_completer)

    def get_completions(self, document, complete_event):
        super().get_completions(document, complete_event)
        self.document = document
        self.complete_event = complete_event
        self.logger.info(f'document.text {document.text}')
        try:
            # 没输入命令时，将命令列表作为补全列表
            if not document.text:
                all_cmds = list(CommandArgumentParserFactory.get_cmd_names())
                # 补全命令
                yield from self.yield_words(all_cmds)
                return

            self.argparser = CommandArgumentParserFactory.build_parser(document.text)
            self.logger.info('completer argparser %s', self.argparser.cmd)
            arg = self.argparser.parse_args(document.text)
            self.logger.info('args %s', arg)
            cmd = self.first_word

            all_cmds = list(CommandArgumentParserFactory.get_cmd_names())
            # 补全命令
            if cmd not in all_cmds:
                yield from self.yield_words(all_cmds)
                return

            word_for_completion = self.word_for_completion

            # 使用自定义方法返回补全单词
            words = self.config.function.get_completion_words(
                word_for_completion)
            if words:
                yield from self.yield_completer(WordCompleter(words))
                return

            # 补全参数后的信息
            words = self.argparser.get_completions_after_argument(
                    word_for_completion)
            if words:
                yield from self.yield_words(words)
                return

            # 使用模块自带的补全
            if word_for_completion in ('--config', '--root'):
                yield from self.yield_completer(self.path_completer)
            else:
                words = self.argparser.get_completions_after_cmd(arg,
                    word_for_completion)
                yield from self.yield_words(words)

        except:
            import traceback
            self.logger.error(traceback.format_exc())
            self.logger.error(traceback.format_stack())
