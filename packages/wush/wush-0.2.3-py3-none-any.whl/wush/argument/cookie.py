#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""
import json
from csarg import Action
from csarg import CommandArgumentParserFactory

from wush.common.loggers import create_logger
from wush.web.cookie import Cookie

from .command import CmdArgumentParser


@CommandArgumentParserFactory.register()
class CookieArgumentParser(CmdArgumentParser):
    cmd = 'cookie'
    logger = create_logger('CookieArgumentParser')

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--domain', action = Action.APPEND.value,
            help='域名')
        item.add_argument('--to-str', action = Action.STORE_TRUE.value,
            help='是否转为字符串')

        return item

    def get_completions_after_argument(self, word_for_completion):
        """
        获取补全的单词列表
        :param word_for_completion: 补全需要的单词
        """
        words = []
        if not self.argument:
            return words
        #  arg = self.argument
        #  if word_for_completion == '--name':
            #  # 针对 --name 参数的自动补全
            #  requests = self.config.get_requests(arg.module)
            #  words = []
            #  for req in requests:
                #  words.append(dict( text = req.name, display_meta=req.title))
            #  return words

        return super().get_completions_after_argument(word_for_completion)

    def run_command(self, text):
        """运行命令行模式"""
        args = self.parse_args(text)
        if args.domain:
            res = Cookie.get_browser_cookie(*args.domain)
            if args.to_str:
                lines = [f'{k}={v};' for k, v in res.items()]
                print(' '.join(lines))

            else:
                print(json.dumps(res, indent=4))
            return
        print('使用 --domain 指定域名')

    def run_shell(self, text):
        self.run_command(text)

