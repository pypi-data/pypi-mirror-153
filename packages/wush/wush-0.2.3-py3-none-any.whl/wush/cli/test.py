#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

from wush.web.request import RequestClient
from wush.web import RequestBuilder
import re


_REG_ENV = r'\{(.+?)\}'


def replace(match):
    print(dir(match))
    print(match.groups())


    print('-' * 10)
    return 'ssss'

def main():
    #  builder = RequestBuilder(method='get', url = 'https://ipconfig.io/json')
    #  client = RequestClient(builder)
    #  res = client.request()
    #  print(res.json())

    text = 'my name is ${name} and age is {age()}'
    text = 'ss'
    print('s')

    print(re.findall(_REG_ENV, text))
    res = re.sub(_REG_ENV, replace, text)
    print(res)
    #  logger.info(res)


if __name__ == "__main__":
    main()
