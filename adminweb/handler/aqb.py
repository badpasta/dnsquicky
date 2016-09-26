#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# # Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:

# Python by version 2.7.

from adminweb.handler.base import BaseHandler
from adminweb.handler.exception import WebErr
from smalltools.opsJson import jsonLoads, convJson, convSimpleJson
from smalltools.status import Message
from smalltools.Other import sqlZip

from tornado.gen import coroutine, Task, Return
from tornado.httpclient import AsyncHTTPClient
from functools import partial

from tornado.websocket import WebSocketHandler


class AQBApiHandler(BaseHandler):
    @coroutine
    def get(self):
        sql = "select a.rid, b.rid, a.sub_domain, a.value, b.value, a.record_type, b.record_type, a.zone_name, a.status from (select rid, zone_name, sub_domain, status, value, record_type from record_view where value like '%aqb.so%') as a, (select rid, zone_name, sub_domain, record_type, value from record_view) as b where a.zone_name = b.zone_name and a.sub_domain = b.sub_domain and b.record_type = 'A';"
        aqb_table = ["rid", "sub_domain", "value", "record_type", "zone_name", "status"]
        #aqb_table = ["a_rid", "b_rid","a_sub_domain", "a_value","b_value", "zone_name", "status"]
        #sql = "select rid, sub_domain, record_type, value, ttl, status, zone_name from record_view where value like '%aqb%';" 
        kw = dict()
        sql_tuple = yield Task(self.db.select, sql, **kw)
        #sql_dict = sqlZip(aqb_table, sql_tuple)

        to_redis = dict()
        to_web = list()
        tuple_que = list()
        for tup in range(len(sql_tuple)):
            s = bool()
            tu = list(sql_tuple[tup])
            if to_redis.has_key(tu[0]): s = True
            if not to_redis.has_key(tu[0]):
                to_redis[tu[0]] = list()
            to_redis[tu[0]].append(tu[1])
            if s:
                num = tuple_que.index(int(tu[0]))
                to_web[num][2] = str(to_web[num][2]) + ',' + str(tu[4])
                continue
            #print tu[4] +" "+tu[6]
            if tu[8]:
                # 注意:list删除元素后长度缩短1
                del tu[6]
                del tu[4]
            else:
                del tu[5]
                del tu[3]
            del tu[1]
            to_web.append(list(tu))
            tuple_que.append(tu[0])
        aqb_list = sqlZip(aqb_table, to_web)
        #print convJson(aqb_list)
        self.finish(convJson(dict(status=True,records=aqb_list)))
        func = partial(self.redisClient.push, param='rpush')
        for key, values in to_redis.items():
            func(key=key, args=values)

    @coroutine
    def post(self): pass
       

class AQBChangeHandler(WebSocketHandler):
    clients = set()
    def open(self):
        self.write_message('初始化..')
        AQBChangeHandler.clients.add(self)
       
    def on_close(self):
        AQBChangeHandler.clients.remove(self)

    def check_origin(self, origin):  
        return True  

    def on_message(self, message):
        data = jsonLoads(message)
        if 'aqb' in data['param']:
            pass
        print message
        self.write_message(message)

