#!/usr/bin/env python
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding=utf-8 -*-
# Python by version 2.7.
# gittle-0.5.0
# 
# Syntax:
# show

from os.path import isdir, basename
from yaml import load as yamlLoad
from re import match as re_match
from dnspodapi import DomainId, RecordList, RecordRemove, RecordCreate
from json import  loads as json_loads
from prettytable import PrettyTable
from mako.template import Template
from gitoper import GitOper
from smalltools import vimFile, writeFile, convJson, openFile, readFile
from operdns import reverseTrans, parseNamedConf
from contextlib import contextmanager

import argparse
import requests # select to http://docs.python-requests.org/en/latest/user/quickstart/
import os
import sys
import copy


# Analysis opts.
def expYaml(d):

    fTmp = open(d)
    yTmp = yamlLoad(fTmp) # select for python dict
    fTmp.close()

    return yTmp


def parseParams(opts):

    ''' trmap = ['record_api', 'config', 'domain_api', 'default'] '''

    found = filter(lambda x: isdir(x),
                    (opts.conf_Path, '/etc/secdd/conf'))

    if not found:
        print "configuration directory is not exit!"
        sys.exit(0)

    recipe = found[0]
    trmap = []
    for root, dirs, files in os.walk(recipe):
        for filespath in files:
            if re_match('.*ml$', filespath):
                trmap.append(expYaml(os.path.join(root, filespath)))

    return trmap


def parseCli():

    base = argparse.ArgumentParser(description='secdd.')
    base.add_argument('--conf-path',dest='conf_Path',help='config dir')
    cmds = base.add_subparsers(dest='cmd')

    #
    cmd_recordlist = cmds.add_parser('recordlist')
    cmd_recordlist.add_argument('--domain', help='domain_name')

    #
    cmd_grouplist = cmds.add_parser('grouplist')

    #
    cmd_grouplist = cmds.add_parser('clear')

    # 
    cmd_edit = cmds.add_parser('edit')
    cmd_edit.add_argument('--domain', help='domain_name')

    # 
    cmd_commit = cmds.add_parser('commit')
    cmd_commit.add_argument('-m',dest='commit_message', help='commit messages.')

    # 
    cmd_push = cmds.add_parser('push')
    #
    cmd_reset = cmds.add_parser('reset')

    #
    cmd_add = cmds.add_parser('add')
    cmd_add.add_argument('zone')

    return base.parse_args()
# -----

class RecordOper:

    def __init__(self, domain, domain_api, line, ttl, **kw):

        self.domain_id = DomainId(domain_api, domain, **kw)
        self.domain = domain
        self.line = line.encode('utf-8')
        self.ttl = ttl
        self.base_info = dict()
        self.base_info.update(kw)
      
  
    def Info(self, record_api):

        tList = RecordList(self.domain_id, **self.base_info).urlPost(record_api)

        return tList['info']['record_total'], tList['records']


    def Rm(self, del_list, records, remove_uri):

        intersection = lambda set_a, set_b: set_a.issubset(set_b)

        try:
            ids = map(lambda x: filter(lambda y: intersection(set(x), y.values()), records)[0]['id'], del_list)
            for the_id in ids:
                status = RecordRemove(self.domain_id, the_id, **self.base_info).urlPost(remove_uri)
                print status
        except:
            print 'No records in DNS server!'


    def Add(self, add_list, add_uri):

        record_key = ['sub_domain', 'record_type', 'value', 'status']
        record_dict = map(lambda x: dict(zip(record_key,x)), add_list)

        for record in record_dict:
            the_post = copy.deepcopy(self.base_info)
            the_post.update(record)
            the_post['record_line'] = self.line
            the_post['ttl'] = self.ttl
            status = RecordCreate(self.domain_id, **the_post).urlPost(add_uri)
            print status['status']['message']


def remotePush(diff_file, record_api, domain_api, line, ttl, **kw):

    local_domain = list()
    the_illusion = json_loads(openFile(diff_file))
    for records in the_illusion:
        for domain,values in records.items():
            add_list = list()
            del_list = list()
            if 'zone' not in domain:
                if not re_match(r'(\w+\.){2}', domain):
                    push_record = RecordOper(domain, domain_api, line, ttl, **kw)
                    _, record_list = push_record.Info(record_api['list'])
                    for x in values:
                        if '-' in x[0]:
                            x[0] = x[0].strip('-')
                            if ';' in x[0]:
                                x[0] = x[0].strip(';')
                                x.append('0')
                            del_list.append(x)
                            continue
                        if '+' in x[0]:
                            x[0] = x[0].strip('+')
                            if ';' in x[0]:
                                x[0] = x[0].strip(';')
                                x.append('disable')
                            add_list.append(x)
                            continue
                    push_record.Rm(del_list, record_list, record_api['remove'])
                    push_record.Add(add_list, record_api['create'])
                else:
                    local_domain.append(domain)

    return local_domain


def recordList(original_record): 

    tables_name = ['name', 'type', 'mx', 'value', 'enabled']

    # Row in use to parameter return.
    record_list = [map(lambda x:rec[x], tables_name) for rec in original_record]

    return tables_name, record_list
    

def groupParse(dns_path):

    align_name = 'group_name'
    tables_name = ['group_name', 'description']
    description = ''
   
    file_list = list() 
    for root, dirs, files in os.walk(dns_path):
        for the_file in files:
            if 'zone' not in the_file and re_match(r'(\w+\.)', the_file):
                file_list.append(the_file)
    
    group_list = list(set(map(lambda x: (x,description), file_list)))

    return  tables_name, group_list


def rootDomain(templ_path, file_path, domain, function):

    ''' 1.download record list. (function recordList)
        2.conv to file.
        3.write file and save.
        ...'''

    tables_name, record_list = function
    the_file = file_path + domain
    del tables_name[-1]

    for record in record_list:
        if '0' in record[-1]:
            record[0] = ';' + record[0]
        del record[-1]
        if '0' in record[-2]: record[-2] = ''

    context = _useMako(templ_path, record_list, domain)
    vimFile(context, the_file) 


def localDomain(dns_path, domain):

    the_file = dns_path + domain
    context = openFile(the_file)
    vimFile(context, the_file) 


def makeSerial(dns_path, domain_list):

    import datetime

    new_serial = "%s01" %datetime.datetime.now().strftime("%Y%m%d")
    for domain in domain_list:
        the_file = dns_path + domain
        #print "Check Serial of the_file: %s" %the_file
        context = openFile(the_file)
        for line in context.split('\n'):
            if 'Serial' in line:
                old_serial = line.split()[0]
                #print "The old serial is %s" %old_serial
                serial_number = new_serial < old_serial and old_serial + 1 or new_serial
                #print "The new serial is %s" %serial_number
                break
        context = context.replace(old_serial, serial_number)
        writeFile(context, the_file)


def makeReverseDns(file_path, templ_path, ptr_map):

    file_list = list()
    for key, record_list in ptr_map.items():
        context = _useMako(templ_path, record_list)
        file_name = key + '.zone'
        the_file = file_path + file_name 
        writeFile(context, the_file)
        file_list.append(file_name)

    makeSerial(file_path, file_list)


def _useMako(templ_file, rrdatas='', domain='daling.com', ttl=60):

    context = Template(filename=templ_file).render(ttl=ttl, domain=domain, rrdatas=rrdatas) 
    
    return context


def convTable(function, border_stat=True, header_stat=True):

    tables_name, tlist = function
    xlist = PrettyTable(tables_name)
    xlist.border = border_stat
    xlist.header = header_stat
    xlist.align = "l"
    xlist.padding_width = 1

    for r in tlist:
        xlist.add_row(r)

    return xlist


def operationPid(pid_file, file_path):

    user_name = os.popen('whoami').read().split('\n')[0]
    user_file = "%suser.%s" %(file_path, user_name)

    try:
        os.mkdir(file_path)
        os.mknod(pid_file)
        os.mknod(user_file)
        print "Operation DNS by %s" %user_name
    except:
        in_use = filter(lambda x: 'user' in x, os.listdir(file_path))
        if user_name not in in_use[0]:
            print "dns program in used. User:" + str(in_use)
            sys.exit(0)
        else:
            return


def clearPid(file_path):

    assert not os.system("rm -rf %s" %file_path)
    print "The dns path was clear." 
    

def main():

    opts = parseCli()
    default, domain_api, record_api, config  = parseParams(opts)

    output_format = default['format']
    login_token = "%s,%s" %(default['token_id'], default['token'])
    base = {'format': output_format,
            'login_token': login_token}

    dns = GitOper(config['dns_path'], config['dns_repo'])

    if hasattr(opts, 'domain') and not re_match(r"(\w+\.){2}", opts.domain):
        record_oper = RecordOper(opts.domain, domain_api['list'], default['line'], default['ttl'], **base)
        record_count, original_record = record_oper.Info(record_api['list'])


    dns_diff = config['diff_file'] + '.dns'
    if opts.cmd == 'edit':
        operationPid(config['pid_file'], config['file_path'])
        try:
            dns.clone()
        except OSError: pass
        if not re_match(r"(\w+\.){2}", opts.domain):
            rootDomain(config['resolv_templ'], config['dns_path'], opts.domain, recordList(original_record))
        else:
            localDomain(config['dns_path'], opts.domain)
    elif opts.cmd == 'recordlist':
        if not re_match(r"(\w+\.){2}", opts.domain):
            print convTable(recordList(original_record))
        else:
            print convTable(lcoalrecord())
    elif opts.cmd == 'grouplist':
        print convTable(groupParse(config['dns_path']))
    elif opts.cmd == 'commit':

        diff_context = dns.commit(config['file_path'], opts.commit_message)
        print '\nAll files with check different..'
        #print convJson(diff_context)
        print 'diff file write in %s' %dns_diff
        writeFile(convJson(diff_context), dns_diff)
        print '\033[1;31;40m WARNNING: Do not repeat to "commit" if you have multi-edit!!\033[0m'
    elif opts.cmd == 'push':
        domain_list = remotePush(dns_diff, record_api, domain_api['list'], default['line'], default['ttl'], **base)
        makeSerial(config['dns_path'], domain_list)
        zone_list = parseNamedConf(config['named_path'], config['named_repo'])
        ptr_map = reverseTrans(config['dns_path'], zone_list)
        makeReverseDns(config['dns_path'], config['ptr_templ'], ptr_map)
        dns.push()
        clearPid(config['file_path'])
    if opts.cmd == 'clear':
        clearPid(config['file_path'])


if  __name__ == '__main__':

    main()
