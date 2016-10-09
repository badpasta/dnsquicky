#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# # Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:

# Python by version 2.7.

from adminweb.handler.base import BaseHandler, BaseWebSocketHandler
from adminweb.handler.exception import WebErr
from adminweb.opstools.resolver import CheckDnsRecords
from adminweb.opstools.http import AsyncHttpClient
from smalltools.opsJson import jsonLoads, convJson, convSimpleJson
from smalltools.status import Message
from smalltools.Other import sqlZip

from tornado.gen import coroutine, Task, Return
from functools import partial
from tornado.httputil import HTTPHeaders
from tornado.httpclient import HTTPError

class AQBApiHandler(BaseHandler):
    @coroutine
    def get(self):
        sql = "select a.rid, b.rid, a.sub_domain, a.value, b.value, a.record_type, b.record_type, a.zone_name, a.status from (select rid, zone_name, sub_domain, status, value, record_type from record_view where value like '%aqb.so%') as a, (select rid, zone_name, sub_domain, record_type, value from record_view) as b where a.zone_name = b.zone_name and a.sub_domain = b.sub_domain and b.record_type = 'A';"
        aqb_table = ["rid", "sub_domain", "value", "record_type", "zone_name", "status"]
        kw = dict()
        sql_tuple = yield Task(self.db.select, sql, **kw)
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
        self.finish(convJson(dict(status=True,records=aqb_list)))
        for key, values in to_redis.items():
            self.redisClient.push('rpush', key, *values)

    @coroutine
    def post(self): pass
       

class AQBChangeHandler(BaseWebSocketHandler):
    clients = set()
    def open(self):
        AQBChangeHandler.clients.add(self)
       
    def on_close(self):
        self.write_message('CHANNEL CLOSED.')
        AQBChangeHandler.clients.remove(self)

    def check_origin(self, origin):  
        return True  

    @coroutine
    def on_message(self, message):
        data = jsonLoads(message)
        record = data['sub_domain']+'.'+data['zone_name'] if '@' not in data['sub_domain'] else data['zone_name']
        if 'aqb' in data['param']:
            tmp_mess = '记录: ' + record +'初始化..'
            self.write_message(tmp_mess)
            print tmp_mess
            try:
                status = yield self.goCurl(record, **data)
                assert status
            except:
                raise HTTPError(4001)

            yield self.switchDNS(record, **data)

    @coroutine
    def goCurl(self, record, **kw):
        rid = kw['rid']
        status = str()
        add_list, url_path = yield self.getRecordSomethingByRid('114.114.114.114', record, **kw)
        tmp_mess = '返回安全宝ip地址列表:' + str(add_list)
        print tmp_mess
        self.write_message(tmp_mess)
        url_list = map(lambda x: ('http://' + x + url_path), add_list)
        httpClient = AsyncHttpClient()
        for request in httpClient.getUrl(url_list, host=record):
            try:
                result = yield httpClient.http_client.fetch(request)
                status = str(result.code)
            except HTTPError, e:
                status = str(e.code)
            self.write_message('url:' + request.url)
            self.write_message('状态:' + status)
            if '405' not in status and '40' in status or '50' in status:
                self.write_message('服务器访问异常,请检查相关配置.')
                self.write_message('停止切换动作.')
                raise Return(False)
        self.write_message('服务器访问正常.')
        self.write_message('开始切换记录.')
        raise Return(True)
        
    @coroutine
    def getRecordSomethingByRid(self, nameserver, record, **kw):
        dns = CheckDnsRecords()
        dns.nameServer(nameserver)
        select_sql_value = 'select value, url_path from  (select a.rid, value, url_path from (select rid, value from record_list) as a right  join aqb_urlinfo as b on a.rid = b.rid) as c where rid = %(rid)s'
        values = yield Task(self.db.select, select_sql_value, rid=kw['rid'])
        values_list = list(values[0])
        if not kw['status']:
            values_list[0] = record
        url_path = values_list[1]
        add_list = dns.address(values_list[0], 'A')
        raise Return((add_list, url_path))

    @coroutine
    def switchDNS(self, record, **kw):
        key_list = self.redisClient.get('lrange', kw['rid'], '0', '-1')
        aqb_list = [(kw['rid'], kw['status'])]
        slave_map = map(lambda x: (x, not kw['status']), key_list)
        http = AsyncHttpClient()
        url = 'http://127.0.0.1:8001/api/record.disable'
        for rid, status in (aqb_list + slave_map):
            request = http.request('POST', url, zone_name=kw['zone_name'], rid=rid, status=status)
            result = yield http.push(request)
            if 200 != result.code:
                raise HTTPError(result.code) 

