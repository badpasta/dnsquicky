#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.

from flask import render_template, flash, redirect
from badchats import app
from .forms import LoginForm

@app.route('/')
@app.route('/token')
def token():
    token = 'OdwGW5Enraa35OSsJXaq'
    return render_template('token.html',
                title = 'token',
                token = token)

@app.route('/index')
def index():
    user = { 'name': 'badpastas'}
    return render_template("index.html",
                title = 'Home',
                user = user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = { 'name': 'badpasta'}
    if form.validate():
        flash('Login requested for OpenId="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
                title = 'Sing Get',
                user = user, form = form)

@app.route('/tab')
def tab():
    user = { 'name': 'aiyouwoqu' }
    return render_template("tab.html", title='tab', user = user)
