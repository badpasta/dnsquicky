#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from adminweb.handler.base import BaseHandler
from tornado.gen import coroutine, Task, Return

class ThisDemo(BaseHandler):
    @coroutine
    def get(self):
        self.render('index.html', the_box=context_dict)
