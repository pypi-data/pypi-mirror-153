#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import sys
import os
#  import re

from csarg import CommandArgumentParserFactory
#  from wpy.path import walkfile
from wush.common.utils import get_current_module_path
from wush.common.utils import load_module

from wush.argument.command import CmdArgumentParser
from wush.common.constants import Constants
from wush.common.loggers import create_logger
from wush.common.run_mode import RUN_MODE
from wush.config import load_config

__all__ = ['Command']

class Command(object):
    logger = create_logger('Command')

    def __init__(self):
        # 初始化创建临时文件目录
        if not os.path.exists(Constants.TMPDIR):
            os.makedirs(Constants.TMPDIR)

        # 动态加载参数解析器模板
        argument_dir = os.path.join(get_current_module_path(), 'argument')
        for name in os.listdir(argument_dir):
            if not name.endswith('.py'):
                continue
            module = f'wush.argument.{name[:-3]}'
            load_module(module)

    def convert_argparse(self, cmd):
        """转换参数解析器"""
        for clz in CmdArgumentParser.__subclasses__():
            if clz.cmd == cmd:
                return clz.default()

        return CommandArgumentParserFactory.build_parser(cmd)

    #  @profile
    def run(self):
        sys_args = sys.argv[1:]
        if not sys_args:
            sys_args = ['shell']
        cmd = sys_args[0]

        if cmd not in CommandArgumentParserFactory.get_cmd_names():
            # 不在程序范围内的命令，默认当做 url 处理
            if not cmd.startswith('http'):
                sys_args[0] = 'http://' + cmd
            sys_args.insert(0, 'run')
            sys_args.insert(1, '--url')
            cmd = 'run'
            #  args_text = ' '.join(sys_args)
            #  # 判断 cmd 是否为 url 格式
            #  if re.match(r'^https?:/{2}\w.+$', cmd):
                #  args_text = 'run ' + args_text.replace(cmd, f'--url {cmd}')
                #  cmd = 'run'

        RUN_MODE.set_command()
        # 转换参数解析器
        parser = self.convert_argparse(cmd)

        args = parser.parse_args(sys_args)
        # 加载配置
        config_path = None
        if hasattr(args, 'config'):
            config_path = args.config
        self.config = load_config(config_path)
        if hasattr(args, 'module'):
            self.config.module_name = args.module
        if hasattr(args, 'space'):
            self.config.space_name = args.space

        parser.run(sys_args)

