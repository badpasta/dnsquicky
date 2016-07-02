#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
# pip install pyYaml 


from os.path import isdir
from yaml import load as yamlLoad
from sys import exit as sys_exit
from re import match as re_match

import os
import sys

# Analysis opts.
def expYaml(d):

    fTmp = open(d)
    yTmp = yamlLoad(fTmp) # select for python dict
    fTmp.close()

    return yTmp


def expfile(d):
    
    with closing(open(d)) as f:
        tmp_list = f.read().splitlines()
            
    return tmp_list


def parseParams(config_Path):

    found = filter(lambda x: isdir(x),
                    (config_Path, '/etc/secdd/conf'))

    if not found:
        print "configuration directory is not exit!"
        sys_exit(0)

    recipe = found[0]
    trmap = dict()
    for root, dirs, files in os.walk(recipe):
        for filespath in files:
            if re_match('.*ml$', filespath):
                trmap[filespath.split('.')[0]] = expYaml(os.path.join(root, filespath))
    
    return trmap

# -----
def main():

    rmap = parseParams('../conf.d/')
    print rmap


if  __name__ == '__main__':

    main()
