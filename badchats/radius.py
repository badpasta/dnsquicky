#!/usr/bin/env python
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
# gittle-0.5.0
# 
# request:
# postgresql-libs
# show

from os.path import isdir
from yaml import load as yamlLoad
from re import match as re_match, search as re_search
from contextlib import contextmanager

import argparse
import os
import sys
import psycopg2

# Analysis opts.
def expYaml(d):

    fTmp = open(d)
    yTmp = yamlLoad(fTmp) # select for python dict
    fTmp.close()

    return yTmp


def parseParams(opts):

    found = filter(lambda x: isdir(x),
                    (opts.conf_Path, '/etc/secdd/conf'))

    if not found:
        print "configuration directory is not exit!"
        sys.exit(0)

    recipe = found[0]
    trmap = dict()
    for root, dirs, files in os.walk(recipe):
        for filespath in files:
            if re_match('.*ml$', filespath):
                filename = re_search(r'(.*)\..*ml$', filespath).group(1)
                trmap[filename] = expYaml(os.path.join(root, filespath))

    return trmap


def parseCli():

    base = argparse.ArgumentParser(description='secdd.')
    base.add_argument('--conf-path',dest='conf_Path',help='config dir')
    #cmds = base.add_subparsers(dest='cmd')

    return base.parse_args()
# -----

@contextmanager
def _operadius(**kw):

    try:
        conn = psycopg2.connect("dbname=%(database)s user=%(user)s host=%(host)s password=%(password)s" %kw)
    except:
        print "sql is not connection!"
    yield conn.cursor()
    conn.commit()
    conn.close()


def oDBSelect(sql, values, **kw):

    with _operadius(**kw) as sketch:
        sketch.execute(sql % values)
        the_list = sketch.fetchall()
        sketch.close()

    return the_list


def oDBoper(sql, values, **kw):

    with _operadius(**kw) as sketch:
        sql_context = sketch.mogrify(sql % values)
        try:
            status = sketch.execute(sql % values)
            sketch.close()
        except: 
            status = "err"
            return status

    return status


def main():

    opts =parseCli()
    rmap = parseParams(opts)
    values = {'username': "wangjingyu",
              'attribute': "Cleartext-Password",
              'op': ":=",
              'password': "wolegequ@123"}

    tmp = oDBoper(rmap['radcheck']['insert'], values, **rmap['sqlconn']) 

    print tmp


if  __name__ == '__main__':

    main()
