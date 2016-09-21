#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from adminweb.handler.base import BaseHandler
from smalltools.opsJson import jsonLoads, convJson
from smalltools.Other import  sqlZip

from tornado.gen import coroutine, Task
from tornado.httpclient import AsyncHTTPClient

import time
import sys


class ZoneHandler(BaseHandler):
    @coroutine
    def get(self):
        origin_json = dict()
        try:
            origin_json['zid']= self.get_argument('zid') or '%'
            origin_sql = self.forms['record_zones']['select']
            origin_data = yield Task(self.db.select, origin_sql, origin_json)
            table_name = ['zid', 'domain_name', 'zgid', 'description']
            data_list = sqlZip(table_name, origin_data)
            message = {"status": True, "message": data_list}
        except:
            message = {"status": False, "message": "params not found."}
        self.write(convJson(message))

    @coroutine
    def post(self):
        origin_json = jsonLoads(self.request.body)
        sql_list = origin_json['values']
        sql_branch = origin_json['param']
        origin_sql = self.forms['record_zones'][sql_branch]
        time_now = time.time()
        data_now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time_now))
        for sql_dict in sql_list:
            if sql_branch == 'update':
                zid = sql_dict['zid']
                select_sql = self.forms['record_zones']['select']
                http_client = AsyncHTTPClient()
                older_data = yield http_client.fetch('http://127.0.0.1:8001/api/zone?id=%s' %zid)
            if sql_branch == 'insert':
                sql_dict['time'] = int(time_now)
            try:
                result_data = yield Task(self.db.insert, origin_sql, sql_dict)
                message = [{"status": True, "message": "sql execution successed."}]
            except:
                message = [{"status": False, "message": "sql execution failed."}]
        self.write(convJson(message))


class ZoneGroupHandler(BaseHandler):
    @coroutine
    def get(self):
        origin_json = dict()
        origin_json['zgid']= self.get_argument('zgid') or '%'
        origin_sql = self.forms['zone_groups']['select']
        origin_data = yield Task(self.db.select, origin_sql, **origin_json)
        table_name = ['zgid', 'group_name', 'description']
        data_list = sqlZip(table_name, origin_data)
        #data_list = map(lambda x: dict(zip(table_name, x)), origin_data)
        message = {"status": True, "message": data_list}

        #try:
        #except:
        #    message = {"status": False, "message": "params not found."}
        self.write(convJson(message))

    @coroutine
    def post(self):
        origin_json = jsonLoads(self.request.body)
        sql_list = origin_json['values']
        sql_branch = origin_json['param']
        origin_sql = self.forms['zone_groups'][sql_branch]
        time_now = time.time()
        data_now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time_now))
        for sql_dict in sql_list:
            if sql_branch == 'update':
                zgid = sql_dict['zgid']
                select_sql = self.forms['zone_groups']['select']
                http_client = AsyncHTTPClient()
                older_data = yield http_client.fetch('http://127.0.0.1:8001/api/zone?id=%s' %zgid)
            if sql_branch == 'insert':
                sql_dict['time'] = int(time_now)
            try:
                result_data = yield Task(self.db.insert, origin_sql, sql_dict)
                message = [{"status": True, "message": "sql execution successed."}]
            except:
                message = [{"status": False, "message": "sql execution failed."}]
        self.write(convJson(message))



class ZoneNumHandler(BaseHandler):
    @coroutine
    def get(self):
        origin_json = dict()
        status = str()
        result = dict()
        try:
            origin_json['zgid']= self.get_argument('zgid') or '%'
            origin_sql = self.forms['record_zones']['select_num_by_zgid']
            origin_data = yield Task(self.db.select, origin_sql, **origin_json)
            status = True
            result['record_num'] = origin_data[0][0]
        except:
            status = False
            result['message'] = "params not found."
        result['status'] = status
        self.write(convJson(result))
