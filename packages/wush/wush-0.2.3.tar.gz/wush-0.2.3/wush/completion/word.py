#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
命令补全
"""

from prompt_toolkit.completion import Completion

from .base import BaseCompleter

__all__ = ['WordCompleter']

class WordCompleter(BaseCompleter):

    def __init__(self, words):
        self.words = words

    def get_completions(self, document, complete_event):
        super().get_completions(document, complete_event)
        for compl in self.search(self.words):
            start_position = self.get_start_position()
            # 如果列表是补全类，添加位置直接返回
            if isinstance(compl, Completion):
                compl.start_position = start_position
            else:
                compl = Completion(compl, start_position=start_position)
            yield compl

