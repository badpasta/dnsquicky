#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from yaml import load as yamlLoad
from os.path import isdir
from re import match as re_match, search as re_search, split as re_split

from smalltools.parseConfig import parseParams
from dbpool.postgresql import Momoko
from adminweb.application.Application import WebApplication

from tornado.options import options

import adminweb.application.define
import adminweb.handler.work

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def main():
    config_file = 'web-conf.d/default.conf'
    form_path = 'forms'
    extend_config_path = 'conf.d/'
    extend_config = parseParams(extend_config_path)
    external_api = dict(domain=extend_config['domain_api'], record=extend_config['record_api'])
    db_conf = extend_config['db']
    tornado.options.parse_config_file(config_file)
    io_loop = tornado.ioloop.IOLoop.instance()
    application = WebApplication()
    application.auth = dict(username=options.LOGINUSER,
                            password=options.LOGINPASS)
    #application.setting['debug'] = options.DEBUG
    application.forms = parseParams(form_path)
    application.extend_config = extend_config['config']
    application.external_api = external_api
    application.local_api = extend_config['local_api']
    application.db = Momoko()
    application.db.connect(io_loop, db_conf['DBSERVER'], db_conf['DBNAME'],
                           db_conf['DBUSER'], db_conf['DBPASS'], db_conf['PORT'])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.PORT)
    io_loop.start()


if  __name__ == '__main__':

    main()
