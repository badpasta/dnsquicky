#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from adminweb.opstools.localdns import IxfrRecord


record_dict = {'sub_domain':u'testdd.ops', 'value':u'119.254.119.150', 'record_type':u'A','ttl':u'60'}
host = '10.0.31.16'
branch = 'delete'
#branch = 'update'
origin = 'bj0.daling.com'

ixfr = IxfrRecord(origin, branch, host)
ixfr.post(**record_dict)




