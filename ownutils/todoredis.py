#!/usr/bin/env python
# -*- coding: utf-8 -*-
# # Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# Python by version 2.7.

from redis import ConnectionPool,Redis

from contextlib import contextmanager


class NonAsyncRedis(object):
    def __init__(self, server='127.0.0.1', port=6379,db=0): 
        pool = ConnectionPool(host=server, port=port,db=db)
        self.redis = Redis(connection_pool=pool)
        self.pipe = self.redis.pipeline()

    def push(self, param, key, *args):
        #self.redis.delete(key)
        message = str()
        if not self.redis.llen(key):
            p = eval('self.pipe.'+param)
            message = p(key, *args)
            self.pipe.execute()

        #print "key:%s" %key
        return message
        #print "key:%s" %key
        #print  "redis push done."

    def get(self, param, key, *args):
        message = str()
        if self.redis.llen(key):
            p = eval('self.redis.'+param)
            message = p(key, *args)
        return message

    def parseData(self, key, *args): pass
       

def main():
    server = 'l-dnstools1.ops.bj2.daling.com'
    redis = NonAsyncRedis(server=server)
    print redis.get('lrange', '107338936', '0', '-1')

if __name__ == '__main__':
    main()
