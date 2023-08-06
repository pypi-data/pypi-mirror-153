#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

from functools import singledispatch
from functools import lru_cache

def filter(source, *args, **kwargs):
    source_include = args if args else kwargs.get('source_include')
    source_exclude = kwargs.get('source_exclude')
    return DictFilter(source).filter(source_include = source_include,
        source_exclude = source_exclude)

@singledispatch
def _filter(data, include=[], exclude=[]):
    print('_filter')

@_filter.register(dict)
def _filter_dict(data, include=[], exclude=[]):
    print('_filter_dict')

@_filter.register(list)
def _filter_list(data, **kw):
    for d in data:
        _filter_dict(data, **kw)

class DictFilter(dict):
    def filter(self, *args, **kwargs):
        """
        过滤dict
        :param args: 默认 source_include
        :param kwargs:
            source_include：想要留下的keys
                eq:[attr,attr1]
                子元素可以使用 ["obj.attr"] 和 ["obj[attr1,attr2]"] 两种方式
                速度上推荐使用 ["obj[attr1,attr2]"]
            source_exclude：想要去掉的keys
        :return:
        """
        source_include = args if args else kwargs.get('source_include')
        source_exclude = kwargs.get('source_exclude')

        def _filter(t, o, k):
            """
            过滤key
            :param t: 过滤结果
            :param o: 目标对象
            :param k: 需要过滤的key
            :return:
            """
            if k in o:
                t[k] = o[k]
            return t

        def _kv1(k):
            key = k.split('.', 1)[0]
            sub_key = k.split('.', 1)[1]
            return key, sub_key

        def _kv2(k):
            key = k.split('[')[0]
            sub_keys = k.split('[')[1].rstrip(']').split(',')
            return key, sub_keys

        def _include(t, o, k):
            """
            判断key需要何种过滤
            :param t: 过滤结果
            :param o: 目标对象
            :param k: 需要过滤的key
            :return:
            """
            if '.' in k:
                key, sub_key = _kv1(k)
                v = o.get(key)
                if o.get(key) and isinstance(o.get(key), dict):
                    if key not in t:
                        t[key] = {}
                    t[key] = _include(t[key], o[key], sub_key)
                elif v and isinstance(v, list):
                    if key not in t:
                        t[key] = []
                    for i in range(len(v)):
                        temp = DictFilter(v[i]).filter(sub_key)
                        if len(t[key]) == i:
                            t[key].append(temp)
                        else:
                            t[key][i].update(temp)

            elif '[' in k and ']' in k:
                key, sub_keys = _kv2(k)
                v = o.get(key)
                if v and isinstance(v, dict):
                    t[key] = DictFilter(v).filter(*sub_keys)
                elif v and isinstance(v, list):
                    t[key] = [DictFilter(sv).filter(*sub_keys) for sv in v]
            else:
                t = _filter(t, o, k)

            return t

        def _exclude(o, k):
            if '.' in k:
                key, sub_key = _kv1(k)
                v = o.get(key)
                if v and isinstance(v, dict):
                    if sub_key in o[key]:
                        o[key].pop(sub_key)
                elif v and isinstance(v, list):
                    o[key] = [DictFilter(o).filter(source_exclude=[sub_key])
                            for o in v]

            elif '[' in k and ']' in k:
                key, sub_keys = _kv2(k)
                v = o.get(key)
                if v and isinstance(v, dict):
                    o[key] = DictFilter(v).filter(source_exclude=sub_keys)
                elif v and isinstance(v, list):
                    o[key] = [DictFilter(o).filter(source_exclude=sub_keys)
                            for o in v]
            else:
                if k in o:
                    o.pop(k)

        temp = {}
        if source_include:
            for item in source_include:
                temp = _include(temp, self, item)
            return temp
        elif source_exclude:
            for item in source_exclude:
                _exclude(self, item)
            return self
        return self

    def __getattr__(self, item):
        return self[item]


if __name__ == "__main__":
    #  print(filter(dict(id = 1, name = 'wxnacy', age = 12), 'id', 'name', exclude=['name']))
    #  print(filter([dict(id = 1, name = 'wxnacy', age = 12)] * 3, 'id', 'name', exclude=['name']))
    #  print(filter(dict(book=dict(id = 1, name = 'wxnacy', age = 12)), 'book.id',
        #  'book.name', exclude=['name']))
    data = [{ "id": 1 }]
    _filter(data)
    data = { "id": 1 }
    _filter(data)
