#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""
#  import json

from wpy.base import BaseEnum

class ModeEnum(BaseEnum):
    COMMAND = 'command'
    SHELL = 'shell'

class RunMode:
    #  name = 'run_mode'
    _mode = None

    def __init__(self, mode = None):
        self._mode = mode

    @property
    def mode(self):
        """模式"""
        return self._mode

    @property
    def is_command(self):
        """是否为命令模式"""
        return self._mode == ModeEnum.COMMAND.value

    @property
    def is_shell(self):
        """是否为 shell 模式"""
        return self._mode == ModeEnum.SHELL.value

    def set_command(self):
        self._mode = ModeEnum.COMMAND.value

    def set_shell(self):
        self._mode = ModeEnum.SHELL.value

    #  def dict(self):
        #  return { "mode": self.mode }

    #  def json(self):
        #  return json.dumps(self.dict())


RUN_MODE = RunMode()
