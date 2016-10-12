#!/usr/bin/env python
# -*- coding: utf-8 -*-
# # Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# Python by version 2.7.

from adminweb.handler.exception import WebErr
from smalltools.opsJson import jsonLoads, convJson, convSimpleJson

from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado.gen import coroutine, Task, Return
from urllib import urlencode

import types


class AsyncHttpClient(object):
    def __init__(self, user_agent=''):
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36" if not len(user_agent) else user_agent
        self.headers = dict()
        AsyncHTTPClient.__init__(self)

    def setHeaders(self, **kw):
        '''dict("User-Agent":user_agent,"Host":host)'''
        self.headers.update(**kw)

    def header_dict(self, host='', user_agent=''):
        agent = user_agent if len(user_agent) else self.user_agent
        head_dict = {"User-Agent": agent}
        if len(host): head_dict.update(dict(Host=host))
        return head_dict

    @property
    def http_client(self):
        return AsyncHTTPClient()

    def request(self, method, *args, **kw):
        url = str()
        if len(args) == 2:
            url = args[0] + args[1]
        elif len(args) == 1:
            url = args[0]
        else:
            raise WebErr('AsynchttpClient Request params err!')
        body = urlencode(kw) if len(kw) else None
        return HTTPRequest(url=url,headers=self.headers, method=method, body=body) 

    @coroutine
    def push(self, request,  method='GET', *args, **kw):
        http_request = None
        if isinstance(request, types.MethodType):
            http_request = self.request(method, *args, **kw)
        else:
            http_request = request
        result = yield self.http_client.fetch(http_request)
        raise Return(result)

    def getUrl(self, url_list, method='GET', **headers):
        http_headers = self.setHeaders(**headers)
        for url in url_list:
            request = self.request(method, url)
            yield request


class NewAsyncHttpClient(object):
    def __init__(self, user_agent='', **kw):
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36" if not len(user_agent) else user_agent
        self.headers = dict()
        self.headers.update(**kw)

    @classmethod
    def initialize(cls, **kw):
        '''dict("User-Agent":user_agent,"Host":host)'''
        func = cls(**kw)
        return func

    @staticmethod
    def header_dict(host='', user_agent=''):
        agent = user_agent if len(user_agent) else self.user_agent
        head_dict = {"User-Agent": agent}
        if len(host): head_dict.update(dict(Host=host))
        return head_dict

    @staticmethod
    def http_client():
        return AsyncHTTPClient()

    @staticmethod
    def format_body(body_format='json', **kw):
        #if 'origin'  in body_format:
        #    return kw
        if 'json' in body_format:
            return convSimpleJson(kw)
        if 'urlencode' in body_format:
            return urlencode(kw)

    def request(self, body_format='urlencode', method='GET', *args, **kw):
        url = str()
        if len(args) == 2:
            url = args[0] + args[1]
        elif len(args) == 1:
            url = args[0]
        else:
            raise Exception('AsynchttpClient Request params err!')
        body = self.format_body(body_format, **kw) if len(kw) else None
        return HTTPRequest(url=url,headers=self.headers, method=method, body=body) 

    @coroutine
    def push(self, request,  body_format='urlencode', method='GET', *args, **kw):
        http_request = None
        if isinstance(request, types.MethodType):
            http_request = self.request(body_format, method, *args, **kw)
        else:
            http_request = request
        result = yield self.http_client.fetch(http_request)
        raise Return(result)

    def getUrl(self, url_list, method='GET', **headers):
        http_headers = self.setHeaders(**headers)
        for url in url_list:
            request = self.request(method, url)
            yield request


def main():
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
    body_dict = {
        'target':'daling.ng_lua.tengine3.http_code.http_200',
        'from':1475996617,
        'until':1476082974,
        'format':'json'
        }
    request = NewAsyncHttpClient.initialize(user_agent=user_agent)
    request.request('json', 'POST', **body_dict)
    http = request.http_client()
    result = http.fetch(request)
    print result.code
    print result.body

if __name__ == '__main__':
    main()
