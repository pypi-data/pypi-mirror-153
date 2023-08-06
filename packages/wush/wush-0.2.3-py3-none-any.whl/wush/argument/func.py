#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""

from csarg import Action
from csarg import CommandArgumentParserFactory
from inspect import getargspec

from wush.common.utils import list_key_val_to_dict
from wush.common.loggers import create_logger
from wush.config.function import load_function
from .command import CmdArgumentParser


@CommandArgumentParserFactory.register()
class FuncArgumentParser(CmdArgumentParser):
    cmd = 'func'
    logger = create_logger('FuncArgumentParser')

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--doc', help='展示方法的文档信息')
        item.add_argument('--exec', help='执行方法')
        item.add_argument('--params', action = Action.APPEND.value,
            help='请求参数')
        return item

    def run_command(self, text):
        self.run_shell(text)

    def run_shell(self, text):
        functions = self.config.function.get_functions()
        args = self.parse_args(text)
        # 打印方法的文档
        if args.doc:
            for k, v in functions.items():
                if args.doc == k:
                    self._print(getattr(v, '__doc__'))
            return

        if args.exec:
            func_name = args.exec
            func = functions.get(func_name)
            params = list_key_val_to_dict(args.params or [])
            res = func(**params)
            print(res)
            return

        # 方法名的最大长度
        max_func_length = max([len(o) for o in functions.keys()])

        output = {
            'headers': [
                { "display": "方法名", 'width':max_func_length},
                { "display": "描述" },
                { "display": "模块" },
                ],
            'items': []
            }
        for k, v in functions.items():
            output['items'].append((
                k, self._get_short_doc(v), getattr(v, '__module__')))
        self.config.function.print_table(output)

    def _get_short_doc(self, func):
        """获取短文档"""
        doc = func.__doc__ or ''
        doc = doc.split('\n')[0]
        return doc[:20]

    def get_completions_after_argument(self, word_for_completion):
        """
        获取补全的单词列表
        :param word_for_completion: 补全需要的单词
        """
        words = []
        if not self.argument:
            return words
        arg = self.argument
        if word_for_completion == '--doc':
            # 自动补全返回方法名列表
            functions = load_function().get_functions()
            words = []
            for name, func in functions.items():
                words.append(dict( text = name,
                    display_meta=self._get_short_doc(func)))
            return words
        elif word_for_completion == '--exec':
            # 执行方法的自动补全
            functions = load_function().get_functions()
            words = []
            for name, func in functions.items():
                argspec = getargspec(func)
                arg_text = ', '.join(argspec.args)
                if argspec.varargs:
                    arg_text += f', *{argspec.varargs}'
                if argspec.keywords:
                    arg_text += f', **{argspec.keywords}'
                text = f'{name}({arg_text})'
                words.append(dict( text = name,
                    display = text,
                    display_meta=self._get_short_doc(func)))
            return words

        elif word_for_completion == '--params':
            # 参数
            functions = load_function().get_functions()
            params = {}
            for name, func in functions.items():
                if name != arg.exec:
                    continue
                argspec = getargspec(func)
                for arg_name in argspec.args:
                    params[arg_name] = ''
            words = self._dict_to_completions(params)
            return words

        return super().get_completions_after_argument(word_for_completion)

    def _dict_to_completions(self, data):
        """字典转为自动补全信息"""
        words = []
        for k, v in data.items():
            words.append(dict(
                text = '{}='.format(k),
                display = '{}={}'.format(k, v),
                display_meta=''))
        return words
