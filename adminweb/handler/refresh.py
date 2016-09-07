#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from adminweb.handler.base import BaseHandler
from adminweb.opstools.resolver import CheckDns
from adminweb.opstools.dnspodapi2 import PickCookie
from smalltools.opsJson import jsonLoads, convJson
from adminweb.opstools.localdns import parseRecordFromFile

from tornado.gen import coroutine, Task, Return

import adminweb.opstools.resolver
import time

class RefreshHandler(BaseHandler):
    @coroutine
    def post(self):
        origin_json = jsonLoads(self.request.body)
        self.group_name = origin_json['group_name']
        group_sql = self.forms['record_zones']['select_by_group']
        flush_sql = self.forms['record_list']['delete_by_zone']
        zone_list = yield Task(self.db.select, group_sql, group_name=self.group_name)
        func = str()
        if self.group_name == 'DNSPOD': func = self.__FromDNSPOD
        if self.group_name == 'LOCAL': func = self.__FromFilePath
        result = list()
        for zid, name, file_path in zone_list:
            delete_status = yield Task(self.db.insert, flush_sql, zid=zid)
            zone_stat = yield Task(func, name, zid, file_path)
            result.append(zone_stat)
        self.write(convJson(dict(result=result)))

    @coroutine
    def __FromDNSPOD(self, name, *arg, **kw):
        zid, _ = arg
        status_dict = dict(domain_name=name, status=str())
        api = self.dnspod_api['record']['list']
        f = yield self.initRequest()
        domain_id = yield Task(self._Domainid, f, name)
        origin_record_list = yield Task(f.urlPost, api, domain_id=domain_id)
        record_list = origin_record_list[1]['records'] if origin_record_list[0] else list()
        status = yield Task(self._InsertRecordList, record_list, zid=zid)
        status_dict['status'] = status
        raise Return(status_dict)

    @coroutine
    def __FromFilePath(self, name, *arg, **kw): 
        zid, file_path = arg
        zone_file = file_path + '/'+ name
        status_dict = dict(domain_name=name, status=str())
        record_table = ['name', 'ttl', 'type', 'value', 'enabled']
        record_list = map(lambda x: dict(zip(record_table, x)), 
                            parseRecordFromFile(zone_file, name))
        status = yield Task(self._InsertRecordList, record_list, zid=zid)
        status_dict['status'] = status
        raise Return(status_dict)

    @coroutine
    def _InsertRecordList(self, record_list, **kw):
        #status_dict = map(lambda record_dict: 
        #                    dict(zone=name,status=self._InsertRecord(record_dict)), 
        #                    record_list)
        status = list()
        the_dict = kw
        for record_dict in record_list:
            the_dict.update(record_dict)
            cookie = PickCookie(**the_dict)()
            #print cookie
            result = yield Task(self._InsertRecord, cookie)
            status.append(result)
        raise Return(status)

    @coroutine
    def _InsertRecord(self, record):
        time_now = time.time() 
        record.update(time=time_now)
        sql = str()
        if 'LOCAL' in self.group_name:
            sql = self.forms['record_list']['insert']
        if 'DNSPOD' in self.group_name:
            sql = self.forms['record_list']['insert_dnspod']
        try:
            result = yield Task(self.db.insert, sql, **record)
            status = True
        except:
            status = False
        raise Return(status)


