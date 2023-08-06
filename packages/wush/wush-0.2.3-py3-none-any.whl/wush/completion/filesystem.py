#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
命令补全
"""

import os
from prompt_toolkit.completion import Completion

from .base import BaseCompleter

__all__ = ['ExecutableCompleter']

class ExecutableCompleter(BaseCompleter):

    def get_completions(self, document, complete_event):
        super().get_completions(document, complete_event)
        last_word = document.text.split(' ')[-1]

        path = os.path.expanduser(last_word)
        dirname = os.path.dirname(path)

        for name in self.search(os.listdir(dirname)):
            start_position = self.get_start_position()
            yield Completion(name, start_position=start_position)

