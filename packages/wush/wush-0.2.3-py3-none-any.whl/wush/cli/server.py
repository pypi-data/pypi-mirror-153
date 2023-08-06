#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import os
import sys

from flask import Flask
from flask import request

from wush.common.loggers import create_logger
from wush.web.utils import telnet
from wush.web.history import History
from wush.config import load_config

app = Flask(__name__)
client = None

logger = create_logger(__name__)

@app.route('/api/version/<string:version>')
def detail(version):
    res =  History().read(version)
    log_text = f'{request.path} {res}'
    logger.info(log_text)
    return res

@app.route('/api/version/<string:version>/<string:type>')
def detail_type(version, type):
    data = History().read(version)
    res = data.get(type, {})
    if res.get("is_json"):
        return res.get("json")
    else:
        return res.get("text")

@app.route('/api/callback')
def get_callback():
    config = load_config()
    params = dict(request.args)
    func_name = params.pop("func", None)
    if not func_name:
        return { "func": None }

    func = config.function.get_functions().get(func_name)
    if not func:
        return { "func": None }

    return func(**params)

@app.route('/api/test', methods=['post', 'get'])
def test():
    res = {
        "args": request.args,
        "json": request.json,
        "data": str(request.data),
        "headers": dict(request.headers),
        "cookies": dict(request.cookies)
    }
    return res

def clear_stdout():
    # 刷新缓冲区
    sys.stdout.flush()
    sys.stderr.flush()

    # 重定向标准输入、输出、错误的描述符
    # dup2函数原子化地关闭和复制文件描述符，重定向到/dev/nul，即丢弃所有输入输出
    with open('/dev/null') as read_null, \
            open('/dev/null', 'w') as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr.fileno())

def run_server(clear_logger: bool = True, config_path: str = None):
    # 清空输出
    if clear_logger:
        clear_stdout()
    # 获取配置
    config = load_config(config_path)
    port = int(config.server_port)
    host = config.server_host
    # 如果端口还没有启动，则启动服务
    if telnet(host, port):
        logger.info('{}:{} 服务已经启动'.format(host, port))
        return
    logger.info('{}:{} 服务开始启动'.format(host, port))
    app.run(host = host, port=port)

if __name__ == "__main__":
    run_server()
