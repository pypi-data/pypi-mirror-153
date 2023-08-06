#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""
import json

from wush.common.utils import run_shell
from wush.common.loggers import get_logger
from wush.config import load_config
from wush.web.request import RequestClient
from wush.web import RequestBuilder

logger = get_logger('wush.run')

__all__ = ['run']

def run(module_name, request_name, **kwargs):
    params = kwargs.get("params", {})
    env = kwargs.get("env", {})
    json_data = kwargs.get("json", {})
    config_path = kwargs.get("config")
    with_browser_cookie = kwargs.get("with_browser_cookie", False)

    config = load_config(config_path)
    request_model = config.get_request(module_name, request_name,
        environs = env)
    request_model.add_params(**params)
    request_model.add_json(**json_data)

    builder = RequestBuilder.loads_request_model(request_model,
        with_browser_cookie)

    req_client = RequestClient(builder)
    return req_client.request()


def run_in_shell(module_name, request_name, **kwargs):
    params = kwargs.get("params", {})
    env = kwargs.get("env", {})
    json_data = kwargs.get("json", {})
    config = kwargs.get("config")
    cmd = f'wush run --module {module_name} --name {request_name}'
    if params:
        for key, value in params.items():
            cmd += f' --params {key}={value}'
    if env:
        for key, value in env.items():
            cmd += f' --env {key}={value}'
    if json_data:
        for key, value in json_data.items():
            cmd += f' --json {key}={value}'
    if config:
        cmd += f' --config {config}'
    logger.info(f'run cmd {cmd}')
    res = run_shell(cmd)
    lines = []
    for line in res:
        line = line.decode()
        for line in line.split('\n'):
            if line.startswith('('):
                continue
            line = line.replace('\n', '')
            lines.append(line)
    text = ''.join(lines)
    logger.info(f'run res {text}')

    return json.loads(text)


if __name__ == "__main__":
    res = run('wush', 'test_get', params={"age": 1})
    print(res.json())


