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
from tornado.httpclient import HTTPError
from functools import partial

import dns.reversename
import time
import sys
import json

class RecordHandler(BaseHandler): 
    @coroutine
    def get(self):
        origin_json = self.request.arguments
        data =dict()
        status = str()
        result = dict()
        try:
            if not origin_json.has_key('zid'):
                sql_select_zid = "select zid from record_zones where zone_name = %(zone_name)s;"
                tuple_data =yield Task(self.db.select, sql_select_zid, zone_name=origin_json['zone_name'][0])
                data['zid'] = str(tuple_data[0][0])
            else:
                data['zid'] = origin_json['zid'][0] or '%'
            origin_sql = self.forms['record_list']['select_by_zid']
            table_name = ['rid','sub_domain','record_type','value','ttl','weight','mx','record_line','status','zid','rgid','description']
            origin_data = yield Task(self.db.select, origin_sql, **data)
            data_list = sqlZip(table_name, origin_data)
            status = True
            result['records'] = data_list
        except:
            status = False
            result['message'] = "params not found."
        result['status'] = status
        self.write(convJson(result))

    @coroutine
    def post(self):
        #print self.request.body
        ixfr_server = self.extend_config['ixfr']['server']
        origin_json = jsonLoads(self.request.body)
        dns_list = origin_json['values']
        domain_id = origin_json['zid']
        sql_branch = origin_json['param']
        domain_name, domain_group = yield self._CheckGroup(domain_id)
        to_func = None
        result = list()
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
                    result.append(dict(status=False,message=message))
                    continue
                struct['dst'].update(dict(rid=older_data['rid']))
            elif 'insert' not in sql_branch: # len(older_data) = 0 and 'insert' not in sql_branch
                message = 'Do not option this record. The record not exits.'
                result.append(dict(status=False,message=message))
                continue
            status, message = yield Task(to_func, branch=sql_branch, **struct)
            if status: 
                message = yield Task(self._insertChangeLog, sql_branch, **struct)
            result.append(dict(status=status,message=message))
        print convJson(result)
        self.write(convJson(result))

    @coroutine
    def _CheckGroup(self, zid):
        message = str()
        try:
            origin_info = yield Task(self.db.select, self.forms['record_zones']['select_view_zid'], zid=zid)
            message = (origin_info[0][1], origin_info[0][3])
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
        print branch
        print dst['value']
        if 'delete' in branch and 'aqb.so' in dst['value']:
            print 'delete rid: %s' %dst['rid']
            delete_url_sql = 'delete from aqb_urlinfo where rid = %(rid)s'
            yield Task(self.db.insert, delete_url_sql, **dst)
            self.redisClient.get('delete', dst['rid'])
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
        if kw.has_key('mx') and 'MX' not in kw['record_type']: del kw['mx']
        return kw

    def _pickPTR(self, origin, **kw):
        #print dns.reversename.from_address(kw['value'])
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
        ptr_status = False
        if dst['record_type'] == 'A': ptr_status = True
        sql = self.forms['record_list'][branch]
        the_dict = self._pickLocalDNS(**dst)
        if ptr_status: 
            the_ptr = self._pickPTR(origin, **dst)
            origin_list = filter(lambda x: x['zone'] in the_ptr['sub_domain'],ptr_list)
            ptr_origin =  origin_list[0]['zone'] if len(origin_list) else str()
            ixfr_func = IxfrRecord(ptr_origin, master_server=self.extend_config['ixfr']['server'])
        dst['time'] = int(time.time())
        try:
            #one_time = time.time()
            if dst['status'] is False:
                func.post('delete', **the_dict)
                if ptr_status: ixfr_func.post('delete', **the_ptr)
                #two_time = time.time()
                #print(two_time - one_time)
            elif 'update' not in branch:
                func.post(branch, **the_dict)
                if ptr_status: ixfr_func.post(branch, **the_ptr)
            else:
                the_src = self._pickLocalDNS(**src)
                func.post('delete', **the_src)
                func.post('insert', **the_dict)
                if ptr_status:
                    ptr_src = self._pickPTR(origin, **src)
                    src_origin_list = filter(lambda x: x['zone'] in ptr_src['sub_domain'],ptr_list)
                    src_ptr_origin =  src_origin_list[0]['zone'] if len(src_origin_list) else str()
                    ixfr_src_func = IxfrRecord(src_ptr_origin, master_server=self.extend_config['ixfr']['server'])
                    ixfr_src_func.post('delete', **ptr_src)
                    ixfr_func.post('insert', **the_ptr)
            message = 'record options successed.'
        except:
            message = 'record options failed.'
            raise Return((False, message))
        #print sql
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

class RecordNumHandler(BaseHandler):
    @coroutine
    def get(self):
        origin_json = dict()
        status = str()
        result = dict()

        try:
            origin_json['zid']= self.get_argument('zid') or '%'
            origin_sql = self.forms['record_list']['select_count_by_zid']
            origin_data = yield Task(self.db.select, origin_sql, **origin_json)
            status = True
            result['record_num'] = origin_data[0][0]
        except:
            status = False
            result['message'] = "params not found."
        result['status'] = status
        self.write(convJson(result))


class GetRecordIdHandler(BaseHandler):
    @coroutine
    def get(self):
        origin = self.request.arguments
        origin_json = dict()
        status = bool()
        result = dict()
        sql = self.forms['record_list']['select_get_rid']
        try:
            if not origin.has_key('zid'):
                sql_select_zid = "select zid from record_zones where zone_name = %(zone_name)s;"
                tuple_data =yield Task(self.db.select, sql_select_zid, zone_name=origin['zone_name'][0])
                origin_json['zid'] = str(tuple_data[0][0])
            else:
                origin_json['zid'] = self.get_argument('zid')
            origin_json['sub_domain'] = self.get_argument('sub_domain')
            origin_json['record_type'] = self.get_argument('record_type')
            origin_json['value'] = self.get_argument('value')
            origin_data = yield Task(self.db.select, sql, **origin_json)
            status = True
            result['rid'] = origin_data[0][0]
        except:
            status = False
            result['message'] = 'params not found.'
        result['status'] = status
        self.write(convJson(result)) 

    @coroutine
    def post(self):
        origin_json = jsonLoads(self.request.body)
        status = bool()
        result = dict()
        sql = self.forms['record_list']['select_get_rid']
        try:
            if origin_json.has_key('zone_name'):
                sql_select_zid = "select zid from record_zones where zone_name = %(zone_name)s;"
                tuple_data =yield Task(self.db.select, sql_select_zid, zone_name=origin_json['zone_name'])
                origin_json['zid'] = str(tuple_data[0][0])
            origin_data = yield Task(self.db.select, sql, **origin_json)
            status = True
            result['rid'] = origin_data[0][0]
        except:
            status = False
            result['message'] = 'params not found.'
        result['status'] = status
        self.write(convJson(result)) 


class DisableRecordHandler(BaseHandler):
    @coroutine
    def post(self):
        '''
            {
            status=,
            rid=,
            zone_name=,
            }
        '''
        rid = int()
        domain_name = str()
        record_status = str()
        try:
            rid = self.get_argument('rid')
            domain_name = self.get_argument('zone_name')
            record_status = 'enable' if 'True' in self.get_argument('status') else 'disable'
        except:
            raise HTTPError('params is error!!')
        func = yield self.initRequest()
        domain_id = yield Task(self._Domainid, func, domain_name)
        request = yield func.urlPost(self.dnspod_api['record']['disable'], domain_id=domain_id, record_id=rid, status=record_status)
        print request[0]
        print request[1]
        if request[0]:
            self.write(convJson(request[1]))
        else:
            raise HTTPError(request[1])


