#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from adminweb.handler.base import BaseHandler
from adminweb.opstools.resolver import CheckDns
from smalltools.opsJson import jsonLoads, convJson
from smalltools.Other import sqlZip

from tornado.gen import coroutine, Task, Return
from tornado.web import authenticated

import adminweb.opstools.resolver


class LoginHandler(BaseHandler):
    @coroutine
    def get(self):
        if self.current_user:
            self.redirect("/records")
        context_dict = self.the_box.copy()
        context_dict['title'] = 'LOGIN'
        self.render('login.html', the_box=context_dict)

    @coroutine
    def post(self):
        origin_json = jsonLoads(self.request.body)
        username = origin_json['username']
        password = origin_json['password']
        message = dict(status='')
        jUrl = '/records'
        if username == self.auth['username']:
            if password == self.auth['password']:
                message['status'] = True
                message['url'] = jUrl 
                self.set_secure_cookie("user", username)
        else:
            message['status'] = False
        self.write(convJson(message))


class LogoutHandler(BaseHandler):
    @coroutine
    def get(self):
        self.clear_cookie('user')
        self.redirect('/login')


class RecordsHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        context_dict = self.the_box.copy()
        context_dict['title'] = 'Records List'
        self.render('records.html', the_box=context_dict)


class AQBHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        context_dict = self.the_box.copy()
        context_dict['title'] = 'AnQuanBao'
        self.render('aqb.html', the_box=context_dict)



class ZonesHandler(BaseHandler):
    @coroutine
    def get(self):
        context_dict = self.the_box.copy()
        context_dict['title'] = 'Zone List'
        self.render('dnszone.html', the_box=context_dict)


class DNSMonHandler(BaseHandler):
    @coroutine
    def get(self):
        context_dict = self.the_box.copy()
        context_dict['title'] = 'DNSMonitor'
        self.render('dnsmon.html', the_box=context_dict)


class CheckDnsDefault(BaseHandler):
    @coroutine
    def post(self):
        origin_json = jsonLoads(self.request.body)
        nameserver = origin_json['nameserver']
        record = origin_json['record']
        rdtype = origin_json['rdtype']
        resolver = CheckDns(nameserver)
        res = resolver.Status(record, rdtype)
        message = dict(data=[res,])
        self.write(convJson(message))


class GetDnsTypeList(BaseHandler):
    @coroutine
    def get(self):
        message = dict(rdtypeList=self.extend_config['rdtype_list']) 
        self.write(convJson(message))


class CheckZoneList(BaseHandler):
    @coroutine
    def get(self):
        table_name = ['zid', 'zone_name', 'zgid', 'group_name', 'description']
        origin_list = yield Task(self.db.select, self.forms['record_zones']['select_view_like'], zid='%')
        zone_groups = sqlZip(table_name, origin_list)
        zone_map = dict()
        for i in zone_groups:
            l = i['group_name']
            if not zone_map.has_key(l):
                zone_map[l] = list()
            zone_map[l].append(dict(id=i['zid'],name=i['zone_name']))
        self.write(convJson(zone_map))
