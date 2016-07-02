#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
# Flask Flask-WTF

from wtforms import Form, StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('save', default=False)
