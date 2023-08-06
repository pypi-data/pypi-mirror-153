#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
网络相关工具方法
"""

import socket
import traceback
from wush.common.loggers import get_logger

logger = get_logger()


def telnet(server_ip: str, port: int) -> bool:
    """链接服务"""
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1) #设置超时时间
    try:
        sk.connect((server_ip,port))
        sk.close()
        return True
    except ConnectionRefusedError:
        return False
    except Exception:
        logger.error(traceback.format_exc())
        logger.error(traceback.format_stack())
        sk.close()
        return False
