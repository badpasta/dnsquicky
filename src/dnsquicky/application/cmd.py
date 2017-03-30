#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from dnsquicky.utils.parseConfig import parseParams

from tornado.options import options, parse_command_line 


def setup_options():
    parse_command_line()
    config_path = options.config
    config = parseParams(config_path)
    pass

def start_api_server():
    setup_options()
    pass
