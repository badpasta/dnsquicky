#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
import sys
import os
#print os.path.abspath(sys.argv[0])
print os.path.split(os.path.realpath(__file__))[0] 
