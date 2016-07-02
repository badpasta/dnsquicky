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

    found = opts.conf_Path

    if not found:
        print "configuration directory is not exit!"
        sys.exit(0)

    recipe = found
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
    base.add_argument('--file',dest='csv_File',help='csv_file')
    base.add_argument('--action',dest='action',help='add or delete or update')

    return base.parse_args()
# -----

@contextmanager
def _operadius(**kw):

    try:
        conn = psycopg2.connect("dbname=%(database)s user=%(user)s host=%(host)s password=%(password)s" %kw)
    except:
        print "sql is not connection!"
        sys.exit(0)
    yield conn.cursor()
    conn.commit()
    conn.close()


def oDBSelect(sql, values, **kw):

    with _operadius(**kw) as sketch:
        sketch.execute(sql % values)
        the_list = sketch.fetchall()
        sketch.close()

    return the_list


def oDBoper(sql, the_list, **kw):

    for values in the_list:
        with _operadius(**kw) as sketch:
            sql_context = sketch.mogrify(sql % values)
            print sql_context
            try:
                status = sketch.execute(sql % values)
                sketch.close()
            except: 
                status = "err"
                return status

    status = "all is ok."

    return status


def challengeDB(the_file, sql, data_list, **sqlconn):

    import datetime


    the_date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    oDBoper(sql, data_list, **sqlconn)
    os.renames(the_file, (the_file + '.' + the_date + '.bak'))

#class DBFormat:
#
#    def __init__(self, info):
#
#        values = {'username': "wangjingyu",
#                  'attribute': "Cleartext-Password",
#                  'op': ":=",
#                  'password': "wolegequ@123"}
        

def loadXlsx(file_name):

    import xlrd

    workbook = xlrd.open_workbook(file_name)

    the_sheet = workbook.sheet_by_index(0) 
    cols_num = the_sheet.ncols
    rows_num = the_sheet.nrows

    sheet_context = filter(lambda g: g[0] is not '', 
                            [map(lambda x: the_sheet.cell(r_num, x).value.encode('utf-8'), 
                                range(0, cols_num)) for r_num in range(0, rows_num)])

    table_line = sheet_context[0]
    user_LineNum = filter(lambda x: 'UserName' in table_line[x], range(0, len(table_line)))[0]
    pass_LineNum = filter(lambda x: 'PassWord' in table_line[x], range(0, len(table_line)))[0]

    origin_list = map(lambda x:  [sheet_context[x][user_LineNum], sheet_context[x][pass_LineNum]], 
                        range(1, len(sheet_context)))

    result_list = list()
    for i in origin_list:
        result_list.append(
                {'username': i[0],
                 'attribute': "Cleartext-Password",
                 'op': ":=",
                 'password': i[1]}
        )

    return result_list


def main():

    opts =parseCli()
    rmap = parseParams(opts)
    file_path = rmap['config']['file_dir']
    if isdir(file_path) is not True:
        print "dir %s is not exist!!" %file_path
        sys.exit(0)

    file_list = os.listdir(file_path)
    for the_file in file_list:
        if re_match(r'.*\.bak$', the_file):
            continue
        if re_match(r'adduser.*', the_file):
            add_list = loadXlsx((file_path + the_file))
            challengeDB((file_path + the_file), rmap['radcheck']['insert'], add_list, **rmap['sqlconn'])
        if re_match(r'deluser.*', the_file):
            del_list = map(lambda x: x['username'],
                            loadXlsx((file_path + the_file)))
            challengeDB((file_path + the_file), rmap['radcheck']['insert'], del_list, **rmap['sqlconn'])
        if re_match(r'updateuser.*', the_file):
            update_list = loadXlsx((file_path + the_file))
            challengeDB((file_path + the_file), rmap['radcheck']['insert'], update_list, **rmap['sqlconn'])


if  __name__ == '__main__':

    main()
