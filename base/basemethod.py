#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description: 
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019-06-04
 * Time: 上午8:59
'''

import platform,subprocess,os,hashlib


def get_os_info():
    return platform.linux_distribution()

def CMD(command,check_name=None):
    checkresult = subprocess.check_output('%s%s'%command,check_name)
    return checkresult

def get_root_path():
    root_path = os.getcwd()
    return root_path

def system():
    systemc = platform.system()
    return systemc

def systemc_dir_flag():
    if system() == 'Windows':
        return '\\'
    else:
        return '/'

def MD5(value):
    md5_v = hashlib.md5(value).digest()
    return md5_v