#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
cookie 相关模块
"""
import traceback
import browsercookie
from http.cookiejar import CookieJar

from wpy.functools import clock
from wush.common.loggers import get_logger
from wush.common.constants import Constants

class Cookie(object):

    logger = get_logger('Cookie')

    _browser_cookies: CookieJar

    def __init__(self, browser_name: str = 'chrome'):
        self._browser_cookies = getattr(browsercookie, browser_name)()

    @property
    def browser_cookies(self) -> type:
        """doc"""
        return self._browser_cookies

    @clock(fmt = Constants.CLOCK_FMT, logger_func = logger.info)
    def get_cookies(self, *domains) -> dict:
        """获取 cookie
        :param list domains: 域名列表
        """
        res = {}

        try:
            for domain in domains:
                v = self.browser_cookies._cookies.get(domain)
                if not v:
                    continue
                cookies = v.get("/")
                for ck, cv in cookies.items():
                    res[ck] = cv.value

        except Exception:
            self.logger.error(traceback.format_exc())
            self.logger.error(traceback.format_stack())
        return res

    @classmethod
    @clock(fmt = Constants.CLOCK_FMT, logger_func = logger.info)
    def get_browser_cookie(cls, *domains, browser: str='chrome') -> dict:
        """获取留来的 cookie
        :param list domains: 域名列表
        """
        chrome = None
        try:
            chrome = getattr(browsercookie, browser)()
        except :
            print('can not import browsercookie')
            traceback.print_exc()
            traceback.print_stack()
        res = {}
        if not chrome:
            return res
        try:
            for domain in domains:
                v = chrome._cookies.get(domain)
                if not v:
                    continue
                cookies = v.get("/")
                for ck, cv in cookies.items():
                    res[ck] = cv.value

        except Exception:
            cls.logger.error(traceback.format_exc())
            cls.logger.error(traceback.format_stack())
        return res

if __name__ == "__main__":
    res = Cookie.get_browser_cookie('.python.org')
    print(res)

