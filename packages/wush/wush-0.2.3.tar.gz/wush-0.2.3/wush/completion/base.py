#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
命令补全
"""

from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import Completion

from wpy.lists import search

__all__ = [
    "BaseCompleter"
]

class BaseCompleter(Completer):
    char_before_cursor = ''
    current_line_before_cursor = ''
    first_word = ''

    def yield_completer(self, completer):
        items = completer.get_completions(self.document, self.complete_event)
        for item in items:
            yield item

    @property
    def first_word(self):
        """
        获取第一个单词
        """
        def _():
            current_line_before_cursor = self.current_line_before_cursor.strip()
            args = current_line_before_cursor.split(' ')
            args_len = len(args)
            return args[0] if args_len > 0 else ''
        res = _()
        return res

    @property
    def word_for_completion(self):
        """补全使用的单词"""
        def _():
            char_before_cursor = self.char_before_cursor
            current_line_before_cursor = self.current_line_before_cursor.strip()
            args = current_line_before_cursor.split(' ')
            args_len = len(args)
            if char_before_cursor == ' ':
                return args[-1]

            return args[-1] if args_len == 1 else args[-2]
        res = _()
        return res

    @property
    def word_before_cursor(self):
        """光标前的单词"""
        def _():
            if self.char_before_cursor == ' ':
                return ''
            text = self.current_line_before_cursor
            text = text.split(' ')[-1]
            if text in ('/', '~/'):
                return text
            return text.split('/')[-1]

        res = _()
        return res

    def get_completions(self, document, complete_event):
        self.document = document
        self.complete_event = complete_event
        for k in dir(document):
            if k.startswith('_'):
                continue
            val = getattr(document, k)
            if k.startswith('get'):
                continue
            if k.startswith('find'):
                continue
            if isinstance(val, int) or isinstance(val, str):
                setattr(self, k, val)

    def get_start_position(self):
        """获取文字补全的位置"""
        word = self.word_before_cursor
        if word in ('/', '~/'):
            return 0
        return -len(word)

    def filter(self, name):
        """过滤文件名"""
        name = name.lower()
        word = self.word_before_cursor.lower()
        if word in ('/', '~/'):
            return True
        if name.startswith(word):
            return True
        return False

    def search(self, words):
        """搜索"""
        keyword = self.word_before_cursor.lower()
        if keyword in ('/', '~/'):
            return words
        if not words:
            return words
        first_word = words[0]
        words_dict = {}
        if isinstance(first_word, Completion):
            words_dict = { o.text: o for o in words }
            words = [o.text for o in words]

        words = search(words, keyword)
        if isinstance(first_word, Completion):
            for i in range(len(words)):
                words[i] = words_dict[words[i]]

        return words

