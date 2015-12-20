#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
#
# Syntax:


from flask import Flask

app = Flask(__name__)

@app.route('/<username>')
def hello_world(username):
    return 'Hello, %s!' %username


if  __name__ == '__main__':

    app.run(host='0.0.0.0',debug=True)
