#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

#import tornado.options
from tornado.options import define


define("port", type=int)
define("server", type=str)
define("config", type=str)
define("DEBUG", type=bool, default=False)
