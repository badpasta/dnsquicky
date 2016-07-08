#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
# momoko

from yaml import load as yamlLoad
from os.path import isdir
from re import match as re_match, search as re_search, split as re_split
from tornado.options import define, options
from dbpool.postgresql import Momoko
from smalltools import convJson, jsonLoads
from tornado.gen import coroutine, Return, Task
from configParse import parseParams
from tornado.httpclient import AsyncHTTPClient
from tornado import gen 

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import momoko


define("PORT", type=int)
define("SERVER", type=str)
define("LOGINUSER", type=str)
define("LOGINPASS", type=str)
define("DBHOST", type=str)
define("DBPORT", type=int)
define("DBUSER", type=str)
define("DBPASS", type=str)
define("DATABASE", type=str)
define("DEBUG", type=bool, default=False)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/login", LoginHandler), 
                    (r"/logout", LogoutHandler), 
                    (r"/adduser", AddUserHandler), 
                    (r"/api/getuser", GetUserListHandler), 
                    (r"/api/getuserinfo", GetUserInfoHandler), 
                    (r"/api/insertuser", InsertUserHandler), 
                    (r"/api/updateuser", UpdateUserHandler), 
                    (r"/api/deluser", DeleteUserHandler), 
                    (r"/index/(\d+)", IndexHandler),
                    (r"/index", IndexHandler)]
        settings = dict(template_path='badchats/templates1',
                        static_path='badchats/static',
                        cookie_secret = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                        login_url = "/login",
                        ui_modules = {'userlist': UserListModule},
                        debug=options.DEBUG
                       )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    @property
    def db(self):
        return self.application.db

    @property
    def forms(self):
        return self.application.forms

    @property
    def extend_config(self):
        return self.application.extend_config

    @property
    def the_box(self):
        self.box = dict()
        self.box['title'] = 'daling.com'
        self.box['alert'] = dict()
        self.box['alert']['tag'] = False
        self.box['alert']['status'] = "warning"
        return self.box


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @coroutine
    def get(self, page_num=1):
        context_dict = self.the_box.copy()
        context_dict['title'] = 'Index'
        context_dict['nav_herf'] = 'index'
        context_dict['api'] = self.extend_config['api']['getuser']
        self.render('index.html', the_box=context_dict)


class UserListModule(tornado.web.UIModule):
    def render(self, api):
        return self.render_string('modules/userlist.html', api=api)

    def javascript_files(self):
        js_list = ["js/userlist.js", "js/notify.min.js"]
        return js_list


class AddUserHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @coroutine
    def get(self):
        context_dict = self.the_box.copy()
        context_dict['title'] = 'AddUser'
        context_dict['nav_herf'] = 'adduser'
        self.render('adduser_new.html', the_box=context_dict)
      

class InsertUserHandler(BaseHandler):
    @coroutine
    def post(self):
        origin_data = jsonLoads(self.request.body)
        sql = self.forms['radcheck']['insert']
        select_api = self.extend_config['api']['getuserinfo']
        user_data = {'username': origin_data['username']}
        status = ''
        http_client = AsyncHTTPClient()
        info_res = yield http_client.fetch(select_api, method='POST', body=convJson(user_data))
        user_info = jsonLoads(info_res.body)
        if len(user_info) is 0:
            try:
                yield Task(self.db.insert, sql, origin_data)
                status = 0
            except:
                status = 1
        else:
           status = 2 
        the_data = {'status': status}
        self.write(convJson(the_data))


class UpdateUserHandler(BaseHandler):
    @coroutine
    def post(self):
        origin_data = jsonLoads(self.request.body)
        sql = self.forms['radcheck']['update_pass']
        status = ''
        try:
            yield Task(self.db.delete, sql, origin_data)
            status = True
        except:
            status = False
        the_data = {'status': status}
        self.write(convJson(the_data))


class DeleteUserHandler(BaseHandler):
    @coroutine
    def post(self):
        origin_data = jsonLoads(self.request.body)
        sql = self.forms['radcheck']['delete']
        status = ''
        try:
            yield Task(self.db.delete, sql, origin_data)
            status = True
        except:
            status = False
        the_data = {'status': status}
        self.write(convJson(the_data))


class GetUserInfoHandler(BaseHandler):
    @coroutine
    def post(self):
        origin_json = jsonLoads(self.request.body)
        sql = self.forms['radcheck']['select_info']
        key = origin_json.keys()[0]
        value = origin_json.values()[0]
        sql_context = sql % (key, key, value)
        origin_data = yield Task(self.db.select, sql_context)
        the_data = map(lambda x: list(x), origin_data)
        self.write(convJson(the_data))
      

class GetUserListHandler(BaseHandler):
    @coroutine
    def post(self):
        origin_json = jsonLoads(self.request.body)
        sql_table = 'id, username'
        sql_key = origin_json.keys()[0] or 'username'
        sql_keyword = '%' + origin_json.values()[0] + '%'
        print sql_keyword
        sql_dict = dict(tables = sql_table, 
                        key = sql_key, 
                        keyword = sql_keyword)
        sql = self.forms['radcheck']['select_user']
        sql_context = sql % sql_dict
        origin_data = yield Task(self.db.select, sql_context)
        table_name = re_split(', ', sql_table)
        user_list = map(lambda x: dict(map(lambda z,d: (d,z), 
                                 x,table_name)), origin_data)
        the_data = { "userlist": user_list,
                     "tables_name": table_name}
        self.write(convJson(the_data))


class LoginHandler(BaseHandler):
    def get(self):
        #if self.current_user:
        #    self.redirect("/index")
        context_dict = self.the_box.copy()
        context_dict['title'] = 'LOGIN'
        self.render('login_new.html', the_box=context_dict)

    def post(self):
        context_dict = self.the_box.copy()
        context_dict['title'] = 'LOGIN'
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username ==  options.LOGINUSER:
            if password == options.LOGINPASS:
                self.set_secure_cookie("user", username)
                self.redirect('/index')
                return
            else:
                context_dict['alert']['context'] = "Password invaid."

        else:
            context_dict['alert']['context'] = "User invaid."

        context_dict['alert']['tag'] = True
        self.render('login_new.html', the_box=context_dict)


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect('/login')


def main():
    config_file = 'web-conf.d/radius.conf'
    form_path = 'forms'
    extend_config_path = 'conf.d/'
    tornado.options.parse_config_file(config_file)
    io_loop = tornado.ioloop.IOLoop.instance()
    application = Application()
    application.forms = parseParams(form_path)
    application.extend_config = parseParams(extend_config_path)
    application.db = Momoko()
    application.db.connect(io_loop, options.DBHOST, options.DATABASE,
                           options.DBUSER, options.DBPASS, options.DBPORT)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.PORT)
    io_loop.start()

if  __name__ == '__main__':

    main()
