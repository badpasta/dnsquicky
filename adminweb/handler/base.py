#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.


from adminweb.opstools.dnspodapi2 import  BaseRequestUrl, domainId
from smalltools.Other import sqlZip

from tornado.gen import coroutine, Task, Return
from tornado.httpclient import AsyncHTTPClient

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def db(self):
        return self.application.db

    @property
    def redisClient(self):
        return self.application.redis

    @property
    def forms(self):
        return self.application.forms

    @property
    def extend_config(self):
        return self.application.extend_config

    @property
    def auth(self):
        return self.application.auth

    @property
    def the_box(self):
        self.box = dict()
        self.box['title'] = 'daling.com'
        return self.box

    @property
    def dnspod_api(self):
        return self.application.external_api

    @property
    def local_api(self):
        return self.application.local_api

    @property
    def http_Client(self):
        return AsyncHTTPClient()

    # Get domain_id
    @coroutine
    def _Domainid(self, f, domain_name):
        domainlist_api = self.dnspod_api['domain']['list']
        domain_result = yield domainId(f, domain_name, domainlist_api)
        domain_id = domain_result[1]
        raise Return(domain_id)
    #

    #Get dnspod account info in db.
    @coroutine
    def __CheckDnspodInfo(self):
        sql = self.forms['dnspod_info']['select']
        origin_data = yield Task(self.db.select, sql, account_id='%')
        table_name = ['account_id', 'account_name', 'd_format', 'ttl', 'default_line', 'token_id', 'token']
        dict_info = sqlZip(table_name, origin_data)
        raise Return(dict_info)

    @coroutine
    def initRequest(self):
        info_list = yield Task(self.__CheckDnspodInfo)
        info = info_list[0]
        login_token = '%s,%s' %(info['token_id'], info['token'])
        f = BaseRequestUrl(info['default_line'], login_token=login_token, format=info['d_format'])
        raise Return(f)
