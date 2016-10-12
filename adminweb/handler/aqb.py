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
from adminweb.opstools.http import AsyncHttpClient, NewAsyncHttpClient
from smalltools.opsJson import jsonLoads, convJson, convSimpleJson
from smalltools.status import Message
from smalltools.Other import sqlZip

from tornado.gen import coroutine, Task, Return
from functools import partial
from tornado.httputil import HTTPHeaders
from tornado.httpclient import HTTPError

from smalltools.opsJson import jsonLoads, convJson, convSimpleJson

import requests
import time
import json

class AQBApiHandler(BaseHandler):
    @coroutine
    def get(self):
        sql = "select * from record_aqb_view;"
        aqb_table = ["rid", "sub_domain", "value", "record_type", "zone_name", "status", "url"]
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
    def post(self):
        origin_json = jsonLoads(self.request.body)
        url_path=origin_json['url_path']
        select_zid_sql = "select zid from record_zones where zone_name = %(zone_name)s;"
        origin_zid = yield Task(self.db.select, select_zid_sql, zone_name=origin_json['zone_name'])
        origin_json['zid'] = int(origin_zid[0][0])
        record_dict = self.initRecord(**origin_json)
        post_dict = {
            "param": "insert",
            "zid": origin_json['zid'],
            "values": [record_dict,]
            }
        result = yield Task(self.recordHttpPost, **post_dict)
        if result.code != 200:
            status = False
        else:
            getRid_sql = 'select rid from record_list where zid = %(zid)s and sub_domain = %(sub_domain)s and value = %(value)s and record_type = %(record_type)s;'
            insert_url_sql = 'insert into aqb_urlinfo values (%(rid)s, %(url_path)s);'
            try:
                get_rid  = yield Task(self.db.select ,getRid_sql, **record_dict)
                rid = get_rid[0][0]
                yield Task(self.db.insert, insert_url_sql, rid=rid, url_path=url_path)
                self.redisClient.push('rpush', rid, *tuple(origin_json['rids']))
                status = True
            except:
                status = False
        message = jsonLoads(result.body)[0]['message']
        print convJson(dict(message=message, status=status))
        self.write(convJson(dict(message=message, status=status)))

    @coroutine
    def recordHttpPost(self, **kw):
        url = 'http://127.0.0.1:8001/api/record'
        client = NewAsyncHttpClient.initialize()
        request = client.request('json', 'POST', url, **kw)
        http = client.http_client()
        result = yield http.fetch(request)
        raise Return(result)


    @staticmethod
    def initRecord(**kw):
        record_key = ('zid', 'sub_domain', 'value', 'ttl')
        get_key_func = lambda key: kw[key]
        record_dict = dict(zip(record_key, map(get_key_func, record_key)))
        record_extend = {
            "status": "False", 
            "record_type": "CNAME", 
            "record_line": u"默认",
            "weight": "0",
            "mx": '0',
            "description": "",
            "rgid": "1",
            "rid": ""
            }
        record_dict.update(record_extend)
        return record_dict


class AQBChangeHandler(BaseWebSocketHandler):
    clients = set()
    @coroutine
    def open(self):
        #body_dict = {
        #    'target':'daling.ng_lua.tengine3.http_code.http_200',
        #    'from':1475996617,
        #    'until':1476082974,
        #    'format':'json'
        #    }
        self.write_message('OPEN.')
        AQBChangeHandler.clients.add(self)
        #yield self.getAQBMonitor(**body_dict)

       
    def on_close(self):
        #self.write_message('CHANNEL CLOSED.')
        print 'MESSAGE: _________CHANNEL CLOSED.'
        self.isClose(True)
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
            me = '域名切换成功.'
            self.write_message(me)
            print me


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

    def isClose(self, status=False):
        self.status = status
    
    @property
    def connection_status(self):
        return self.status

    @coroutine
    def getAQBMonitor(self, interval=3, **kw):
        print 'START AQB MONITOR PROCESS.'
        self.isClose()
        while not self.connection_status:
            result = yield self.httpAQBMonitor(**kw)
            print result.code
            #print result.body
            if 200 != result.code:
                self.isClose(True)
            time.sleep(interval)

    @coroutine
    def httpAQBMonitor(self, **kw):
        url = 'http://monitor.corp.daling.com/render'
        client = NewAsyncHttpClient.initialize()
        request = client.request('json', 'POST', url, **kw)
        http = client.http_client()
        result = yield http.fetch(request)
        raise Return(result)


class AQBMonitorHandler(BaseHandler):
    @coroutine
    def get(self):
        body_dict = {
            #'target':'daling.ng_lua.tengine3.http_code.http_200',
            'target':'alias(sumSeries(removeBelowValue(derivative(scaleToSeconds(daling.access_log.*.http_200, 1)), 0)), "HTTP_200")',
            'from':1475996179,
            'until':1476082565,
            'format':'json'
            }
        yield self.getAQBMonitor(**body_dict)

    def isClose(self, status=False):
        self.status = status
    
    @property
    def connection_status(self):
        return self.status

    @coroutine
    def getAQBMonitor(self, interval=3, **kw):
        print 'START AQB MONITOR PROCESS.'
        #self.isClose()
        #while not self.connection_status:
        result = yield self.httpAQBMonitor(**kw)
        if 200 == result.code:
            #print convJson(result.body)
            print result.code
            #if 200 != result.code:
            #    self.isClose(True)
            #time.sleep(interval)

    @coroutine
    def httpAQBMonitor(self, **kw):
        url = 'http://monitor.corp.daling.com/render'
        client = NewAsyncHttpClient.initialize()
        request = client.request('json', 'POST', url, **kw)
        http = client.http_client()
        result = yield http.fetch(request)
        re = requests.post(url, data=kw)
        re.status_code
        print re.json()
        #print convJson(re.json()[0])
        raise Return(result)

class AQBURLHandler(BaseHandler):
    @coroutine
    def get(self): pass

    @coroutine
    def post(self):
        origin_json = jsonLoads(self.request.body)
        url_path = origin_json['url']
        rid = origin_json['rid']
        reponse = dict()
        sql = 'update aqb_urlinfo SET url_path = %(url_path)s where rid = %(rid)s;'
        try:
            yield Task(self.db.insert, sql, url_path=url_path, rid=rid) 
            reponse['status'] = True
            reponse['message'] = 'URL update successful!'
        except:
            reponse['status'] = False
            reponse['message'] = 'URL update failed!'
        print convJson(reponse)
        self.write(convJson(reponse))




