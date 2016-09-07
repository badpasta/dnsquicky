#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from adminweb.handler.base import BaseHandler
from smalltools.opsJson import jsonLoads, convJson, convSimpleJson

from tornado.gen import coroutine, Task
from tornado.httpclient import AsyncHTTPClient

import time
import sys


class ChangeLogHandler(BaseHandler):
    @coroutine
    def get(self): 
        origin_json = dict()
        try:
            origin_json['change_id']= self.get_argument('change_id') or '%'
            origin_sql = self.forms['changelog']['select']
            origin_data = yield Task(self.db.select, origin_sql, origin_json)
            table_name = ['time', 'action', 'detail']
            data_list = map(lambda x: dict(zip(table_name, x)), origin_data)
            message = [{"status": True, "message": data_list}]
        except:
            message = [{"status": False, "message": "params not found."}]
        self.write(convJson(message))


    @coroutine
    def post(self):
        origin_json = jsonLoads(self.request.body)
        sql = self.forms['changelog']['insert']
        origin_json['detail'] =  convSimpleJson(origin_json['detail'])
        message = str()
        try:
            result_data = yield Task(self.db.insert, sql, origin_json)
            message = [{"status": True, "message": "sql execution successed."}]
        except:
            message = [{"status": False, "message": "sql execution failed."}]
        self.write(convJson(message))
        
