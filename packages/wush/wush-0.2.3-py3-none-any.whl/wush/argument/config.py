#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""
import os
import shutil

from csarg import CommandArgumentParserFactory
from csarg import Action

from wush.common.constants import Constants
from .command import CmdArgumentParser

@CommandArgumentParserFactory.register()
class ConfigArgumentParser(CmdArgumentParser):
    cmd = 'config'

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--init', action=Action.STORE_TRUE.value,
            help="初始化配置文件")
        return item

    def run(self, text):
        args = self.parse_args(text)

        # 初始化配置文件
        if args.init:
            config_path = Constants.CONFIG_PATH
            if os.path.exists(config_path):
                print("配置文件已存在")
                return

            # 判断配置目录是否存在
            if not os.path.exists(Constants.CONFIG_DIR):
                os.mkdir(Constants.CONFIG_DIR)

            shutil.copyfile(Constants.get_sys_config_path(), config_path)
            print('生成配置文件:', config_path)
