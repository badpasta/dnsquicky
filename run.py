#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
# Flask Flask-WTF 

from badchats  import app
from badchats import index

app.config.from_object('config')
app.run(host='0.0.0.0', port=9001, debug=True)

