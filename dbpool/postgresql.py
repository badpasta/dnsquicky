#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
# momoko

from tornado import gen
from tornado.gen import Return, coroutine
import momoko


class Momoko(object):
    def connect(self, ioloop, host, 
                dbname, user, passwd, port=5432):
        
        dsn = (("dbname=%s user=%s password=%s \
                host=%s port=%d" %(dbname, user, passwd, host, port)))

        self.db = momoko.Pool(dsn=dsn, 
                              size=5,
                              ioloop=ioloop)
        future = self.db.connect()
        ioloop.add_future(future, lambda x: ioloop.stop())
        ioloop.start()
        future.result()

    @coroutine
    def insert(self, sql, data):
        sql_data = data
        sql_data.update({
                        'attribute': "Cleartext-Password",
                        'op': ":="
                        })
        sql_context = sql % sql_data
        yield self.db.execute(sql_context)

    @coroutine
    def delete(self, sql,data):
        sql_context = sql % data
        yield self.db.execute(sql_context)

    @coroutine
    def select(self, sql):
        cursor = yield self.db.execute(sql)
        raise Return(cursor.fetchall())
