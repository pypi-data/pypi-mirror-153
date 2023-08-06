#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
from datetime import datetime
from loguru import logger

LOG_FILE = '/tmp/wush.log'
LOG_FORMAT = '[<g>{time:HH:mm:ss.SSS}</g>][<y>{elapsed}</y>]' \
    '[<level>{level}</level>][<c>{name}:{function}:{line}</c>] ' \
    '<level>{message}</level>'

def format_logger(record):
    #  print(record)
    return record


def make_const_extra():
    extra = {}
    #  extra.setdefault('last_time', datetime.now())
    return extra

def patch_record(record):
    #  print(record)

    # 简化包路径名
    name_l = record['name'].split('.')
    if len(name_l) > 2:
        name_l[:-1] = [w[0] for w in name_l[:-1]]
    record.update(
        name='.'.join(name_l),
    )

    # 时间消耗
    record['elapsed'] = str(record['elapsed'])[2:-3]


logger.remove()
#  with logger.contextualize(start_time = datetime.now()):
logger.configure(extra = make_const_extra(), patcher = patch_record)
logger.add(
    LOG_FILE, format=LOG_FORMAT, colorize=True, rotation="50 MB", retention=5
)
#  logger.add( sys.stdout, format = LOG_FORMAT,)

#  handlers = [
        #  {"sink": str(file), "format": "FileSink: {message}"},
        #  {"sink": sys.stdout, "format": "StdoutSink: {message}"},
    #  ]
#  logger.configure(handlers=handlers)


def create_logger(name=None):
    return logger

def get_logger(name=None):
    return create_logger(name=None)


if __name__ == "__main__":
    import time
    logger.debug(f"debug {datetime.now()}")
    time.sleep(1)
    logger.info("info %s", datetime.now())
