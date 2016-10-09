#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# Python by version 2.7.

from adminweb.opstools.dnspodapi2 import  BaseRequestUrl, domainId


class DisableRecord:
    def __init__(self, sql_func):
        self.sql = sql_func
        self.sql_context = "update record_list set status = %(status)s where rid = %(rid)s;"

    def __go(self,  domain_id, rid, status):
        self.sql.insert(self.sql_context, rid=rid, status=status)
        
    __call__ = __go
