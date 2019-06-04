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

import platform,subprocess


def get_os_info():
    return platform.linux_distribution()

def CMD(command,check_name=None):
    checkresult = subprocess.check_output('%s%s'%command,check_name)
    return checkresult