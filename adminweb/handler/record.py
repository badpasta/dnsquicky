#!/usr/bin/env python
# # Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from adminweb.handler.base import BaseHandler
from adminweb.handler.exception import WebErr
from smalltools.opsJson import jsonLoads, convJson, convSimpleJson
from smalltools.status import Message
from smalltools.Other import sqlZip
from adminweb.opstools.dnspodapi2 import PushDNS, domainId
from adminweb.opstools.localdns import IxfrRecord

from tornado.gen import coroutine, Task, Return
from tornado.httpclient import AsyncHTTPClient
from functools import partial

import dns.reversename
import time
import sys


class RecordHandler(BaseHandler): 
    @coroutine
    def get(self):
        origin_json = dict()
        status = str()
        try:
            origin_json['rid']= self.get_argument('rid') or '%'
            origin_sql = self.forms['record_list']['select']
            table_name = list('rid','r_name','r_type','r_value','r_ttl','weight','mx','r_line','r_status','zid','rgid','description')
            origin_data = yield Task(self.db.select, origin_sql, origin_json)
            data_list = sqlZip(table_name, origin_data)
            status = True
            message = data_list
        except:
            status = False
            message = "params not found."
        Message = {"status": status, "message": message}
        self.write(convJson(Message))

    @coroutine
    def post(self):
        ixfr_server = self.extend_config['ixfr']['server']
        origin_json = jsonLoads(self.request.body)
        dns_list = origin_json['values']
        domain_name = origin_json['domain_name']
        sql_branch = origin_json['param']
        domain_group = yield self._CheckGroup(domain_name)
        to_func = None
        message = str()
        if 'DNSPOD' in domain_group:
            func = yield self.initRequest()
            domain_id = yield Task(self._Domainid, func, domain_name)
            a_func = PushDNS(func, domain_id, self.dnspod_api['record'][sql_branch])
            to_func = partial(eval('self.' + '_toDNSPOD'), func=a_func)
        if 'LOCAL' in domain_group:
            ptr_list = yield Task(self.getPTRList, ptrid='%')
            a_func = IxfrRecord(domain_name, master_server=ixfr_server)
            to_func = partial(eval('self.' + '_toLOCALDNS'), func=a_func, ptr_list=ptr_list, origin=domain_name)
        struct = dict()
        for record_dict in dns_list:
            if 'insert' in sql_branch:
                older_data = yield Task(self.checkOlderRecord, record_dict)
            else:
                older_data = yield Task(self.checkOlderRecordByRid, record_dict)
            struct['src'] = older_data
            struct['dst'] = record_dict
            if len(older_data): # len(older_data) > 0
                if 'insert' in sql_branch:
                    message = 'record already exits.'
                    continue
                struct['dst'].update(dict(rid=older_data['rid']))
            elif 'insert' not in sql_branch: # len(older_data) = 0 and 'insert' not in sql_branch
                message = 'Do not option this record. The record not exits.'
                continue
            status, message = yield Task(to_func, branch=sql_branch, **struct)
            if status is False: continue
            if not message: continue
            message = yield Task(self._insertChangeLog, sql_branch, **struct)
            #!!!!error
        self.write(convJson(dict(message=message)))

    @coroutine
    def _CheckGroup(self, domain_name):
        message = str()
        try:
            origin_info = yield Task(self.db.select, self.forms['record_zones']['select_view_name'], domain_name=domain_name)
            message = origin_info[0][3]
        except:
            raise WebErr('Unkown error in this function..')
        raise Return(message)

    @coroutine
    def checkOlderRecord(self, record_dict):
        older_table = ['rid','sub_domain','record_type','value','ttl','weight','mx','record_line','status','zid','rgid','description']
        older_tuple = yield Task(self.db.select, self.forms['record_list']['select_like'], **record_dict)
        older = sqlZip(older_table, older_tuple)[0] if len(older_tuple) else list()
        raise Return(older)

    @coroutine
    def checkOlderRecordByRid(self, record_dict):
        older_table = ['rid','sub_domain','record_type','value','ttl','weight','mx','record_line','status','zid','rgid','description']
        older_tuple = yield Task(self.db.select, self.forms['record_list']['select_rid'], rid=record_dict['rid'])
        older = sqlZip(older_table, older_tuple)[0] if len(older_tuple) else list()
        raise Return(older)

    @coroutine
    def _toDNSPOD(self, func, branch, **kw):
        src = kw['src']
        dst = kw['dst']
        status, result = yield Task(func.post, **dst)
        if status:
            if 'insert' in branch:
                dst.update(dict(rid=result['record']['id']))
                sql = self.forms['record_list']['insert_dnspod']
            elif 'update' in branch:
                sql = self.forms['record_list']['update']
            elif 'delete' in branch:
                sql = self.forms['record_list']['delete']
        else:
            message = result['status']['message']
            raise Return((False, message))
        try:
            yield Task(self.db.insert, sql, **dst)
        except:
            raise Return((False, 'DB write failed.'))
        raise Return((True, 'record option success.'))

    def _pickLocalDNS(self, **kw):
        if kw.has_key('record_line'): del kw['record_line']
        if kw.has_key('status'): del kw['status']
        if kw.has_key('description'): del kw['description']
        if kw.has_key('rid'): del kw['rid']
        if kw.has_key('rgid'): del kw['rgid']
        if kw.has_key('zid'): del kw['zid']
        if kw.has_key('weight'): del kw['weight']
        return kw

    def _pickPTR(self, origin, **kw):
        return dict(sub_domain=str(dns.reversename.from_address(kw['value'])).upper(),
                    ttl=kw['ttl'],
                    record_type='PTR',
                    value=kw['sub_domain'] + '.' + origin + '.')

    @coroutine
    def getPTRList(self, ptrid):
       the_list = yield Task(self.db.select, self.forms['ptr_zones']['select_like'], ptrid=ptrid)
       the_table = ['ptrid','name','zone','description']
       raise Return(sqlZip(the_table, the_list))

    @coroutine
    def _toLOCALDNS(self, func, branch, origin, ptr_list, **kw):
        src = kw['src']  
        dst = kw['dst']
        message = str()
        the_dict = self._pickLocalDNS(**dst)
        the_ptr = self._pickPTR(origin, **dst)
        origin_list = filter(lambda x: x['zone'] in the_ptr['sub_domain'],ptr_list)
        ptr_origin =  origin_list[0]['zone'] if len(origin_list) else str()
        ixfr_func = IxfrRecord(ptr_origin, master_server=self.extend_config['ixfr']['server'])
        dst['time'] = int(time.time())
        try:
            if 'update' not in branch:
                if 'delete' in branch:
                    sql = self.forms['record_list']['delete']
                else:
                    sql = self.forms['record_list']['insert']
                func.post(branch, **the_dict)
                ixfr_func.post(branch, **the_ptr)
            else:
                sql = self.forms['record_list']['update']
                the_src = self._pickLocalDNS(**src)
                ptr_src = self._pickPTR(origin, **src)
                src_origin_list = filter(lambda x: x['zone'] in ptr_src['sub_domain'],ptr_list)
                src_ptr_origin =  src_origin_list[0]['zone'] if len(src_origin_list) else str()
                ixfr_src_func = IxfrRecord(src_ptr_origin, master_server=self.extend_config['ixfr']['server'])
                func.post('delete', **the_src)
                ixfr_src_func.post('delete', **ptr_src)
                func.post('insert', **the_dict)
                ixfr_func.post('insert', **the_ptr)
            message = 'record options successed.'
        except:
            message = 'record options failed.'
            raise Return((False, message))
        yield Task(self.db.insert, sql, **dst)
        raise Return((True, message))

    @coroutine
    def _insertChangeLog(self, branch, **kw):
        the_dict = dict(option_act=branch,
                        detail=convSimpleJson(kw))
        the_dict['time'] = '%s' %int(time.time())
        yield Task(self.db.insert, self.forms['changelog']['insert'], **the_dict)
        try:
            yield Task(self.db.insert, self.forms['changelog']['insert'], **the_dict)
            message = 'record option successed.'
        except: 
            message = 'Changelog writing failed.'
        raise Return(message)


