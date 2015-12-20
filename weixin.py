#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
# pyYaml requests==2.5.3 json SQLAlchemy psycopg2
# 
# Syntax:
# python monitor.py --conf-path ${path}
#       serverlist
#       delay --top 10 |--last 10
#       dig ${domain}

from os.path import isdir, join as path_Join
from json import loads as json_Loads, dumps as json_Dumps
from re import match as re_Match,  split as re_Split
from yaml import load as yamlLoad

import psycopg2
import psycopg2.extras
import os
import argparse

# option
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
        sys_exit(0)

    recipe = found[0]
    trmap = dict()
    for root, dirs, files in os.walk(recipe):
        for filespath in files:
            if re_Match('.*ml$', filespath):
                trmap[filespath.split('.')[0]] = expYaml(os.path.join(root, filespath))
    return trmap


def parseCli():

    base = argparse.ArgumentParser(description='secdd.')
    base.add_argument('--conf-path',dest='conf_Path',help='config dir')
    cmds = base.add_subparsers(dest='cmd')

    cmd_list = cmds.add_parser('list')
    cmd_list.add_argument('-f','--filter',help='filter')

    cmd_create = cmds.add_parser('create')
    cmd_create.add_argument('--file',help='devices infomation file')


    cmd_update = cmds.add_parser('update')
    cmd_update.add_argument('--file',help='update devices infomation file')
    return base.parse_args()


def main():

    opts = parseCli()
    rmap = parseParams(opts)
    
    

if  __name__ == '__main__':

    main()
