#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from adminweb.handler.work import LoginHandler, DNSMonHandler, CheckDnsDefault, GetDnsTypeList, RecordsHandler, ZonesHandler
from adminweb.handler.zone import ZoneHandler, ZoneGroupHandler
from adminweb.handler.refresh import RefreshHandler
from adminweb.handler.log import ChangeLogHandler
from adminweb.handler.record import RecordHandler
from tornado.web import Application
from tornado.options import options




class WebApplication(Application):
    def __init__(self):
        handlers = [(r"/login", LoginHandler),
                    (r"/dnsmon", DNSMonHandler),
                    (r"/api/checkdnsdefault", CheckDnsDefault),
                    (r"/api/getdnstypelist", GetDnsTypeList),
                    (r"/api/zone", ZoneHandler),
                    (r"/api/record", RecordHandler),
                    (r"/api/zonegroup", ZoneGroupHandler),
                    (r"/api/changelog", ChangeLogHandler),
                    (r"/api/refresh", RefreshHandler),
                    (r"/records", RecordsHandler),
                    (r"/zones", ZonesHandler)]
        settings = dict(template_path='adminweb/templates',
                        static_path='adminweb/static',
                        cookie_secret = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                        login_url = "/login",
                        debug=options.DEBUG
                       )
        print "DEBUG Options is %s." %options.DEBUG
        Application.__init__(self, handlers, **settings)

