#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

from routes import Mapper
from wpy.base import BaseObject

route_map = Mapper()
route_map.connect(None, "/api/pg/test?id={id}", controller="pangu", action='test')

#  res = route_map.match('/api/pg/test')
#  print(res)

class Route(BaseObject):

    def __init__(self, url, endpoint, methods=None):
        super().__init__(url = url, endpoint = endpoint, methods=methods)
        if not self.methods:
            self.methods = ['GET']

class RouteGroup(BaseObject):

    def __init__(self, name, url_prefix=None):
        super().__init__(name = name, url_prefix = url_prefix)
        self._routes = []

    def route(self,url, methods=None):
        def decorate(func):
            r = Route(url, func)
            self._routes.append(r)
            return func
        return decorate

    def get_routes(self):
        return self._routes

class RouteFactory(BaseObject):
    _routes_endpoints = {}
    _route_map = Mapper()

    def _add_route(cls, route):
        key = route.endpoint.__name__
        if key in cls._routes_endpoints:
            raise Exception('endpoint {} is exists'.format(key))
        cls._routes_endpoints[key] = route

    def register_route(cls, route):
        if isinstance(route, Route):
            cls._add_route(route)
        if isinstance(route, RouteGroup):
            for r in route.get_routes():
                cls._add_route(r)

        for k, route in cls._routes_endpoints.items():
            cls._route_map.connect(None, r.url, controller='', action=k)

    def match(url, method='GET'):
        """匹配"""


factory = {}

def register(url):
    def decorate(func):
        key = func.__name__
        print(func.__module__)
        print(func.__name__)
        print(func.__new__)
        print(dir(func))
        route_map.connect(None, url, controller="test", action=key)
        factory[key] = func
        return func
    return decorate


#  class Test():

rg = RouteGroup('test')

@rg.route('/test')
def test():
    print('test')

print(rg.get_routes())
