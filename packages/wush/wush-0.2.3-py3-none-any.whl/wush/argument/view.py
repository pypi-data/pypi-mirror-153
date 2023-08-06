#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""
from csarg import CommandArgumentParserFactory

from wush.common.loggers import create_logger
#  from wush.models import Version
from .command import CmdArgumentParser


@CommandArgumentParserFactory.register()
class ViewArgumentParser(CmdArgumentParser):
    cmd = 'view'
    logger = create_logger('ViewArgumentParser')
    _versions = []

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--grep', help='过滤')
        item.add_argument('--open', help='打开')
        item.add_argument('--page', help='页数', datatype=int, default=1)
        item.add_argument('--size', help='每页条数', datatype=int, default=10)
        item.add_argument('--version', help='请求版本')
        return item

    def run(self, text):
        args = self.parse_args(text)
        if args.open:
            self._print('See in browser')
            open_version(args.open)
            return
        self._list(args)

    def _list(self, args):
        items = Version.find()
        items.sort(key = lambda x: x._id, reverse=True)
        data = {
            'headers': [
                { "display": "Version" },
                { "display": "Space" },
                { "display": "Module" },
                { "display": "Name" },
                ],
            'items': []
            }

        def _filter(x):
            text = args.grep
            if text in x.space_name or text in x.module_name or \
                    text in x.request_name:
                return True
            return False

        # 过滤列表
        if args.grep:
            items = list(filter(_filter, items))

        total_count = len(items)

        # 分页展示
        start = (args.page - 1) * args.size
        end = start + args.size
        items = items[start:end]
        self._versions = items
        for item in items:
            data['items'].append((item._id, item.space_name, item.module_name,
                item.request_name))
        if end < total_count:
            data['after_table'] = 'With `--page {}` to see more'.format(args.page + 1)
        self.config.function.print_table(data)

    def get_completions_after_argument(self, word_for_completion):
        """
        获取补全的单词列表
        :param word_for_completion: 补全需要的单词
        """
        words = []
        if not self.argument:
            return words
        arg = self.argument
        if word_for_completion == '--open':
            items = self._versions
            if not items:
                items = Version.find()
                items.sort(key = lambda x: x._id, reverse=True)
            for item in items:
                dm = '{}_{}_{}'.format(item.space_name, item.module_name,
                    item.request_name)
                words.append(dict( text = item._id, display_meta=dm))
            return words

        return super().get_completions_after_argument(word_for_completion)
