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
from tornado.gen import coroutine

import adminweb.opstools.resolver


class LoginHandler(BaseHandler):
    @coroutine
    def get(self):
        #if self.current_user:
        #    self.redirect("/index")
        context_dict = self.the_box.copy()
        context_dict['title'] = 'LOGIN'
        self.render('login.html', the_box=context_dict)

    @coroutine
    def post(self):
        origin_json = jsonLoads(self.request.body)
        username = origin_json['username']
        password = origin_json['password']
        message = dict(status='')
        jUrl = 'http://127.0.0.1:8001/dnsmon'
        if username == self.auth['username']:
            if password == self.auth['password']:
                message['status'] = True
                message['url'] = jUrl 
        else:
            message['status'] = False
        self.write(convJson(message))


class RecordsHandler(BaseHandler):
    @coroutine
    def get(self):
        context_dict = self.the_box.copy()
        context_dict['title'] = 'Records List'
        self.render('records.html', the_box=context_dict)


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
        print self.request.body
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


