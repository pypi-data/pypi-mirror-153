#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
from wush.common.loggers import create_logger
from wush.cli.command import Command

logger = create_logger('main')


def main():
    import time
    begin = time.time()
    cmd = Command()
    cmd.run()
    logger.info('wush time used: {}'.format(time.time() - begin))

if __name__ == "__main__":
    main()

#  index_model.__subclasses__():
