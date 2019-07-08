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
import re

def get_os_info():
    return platform.linux_distribution()

def CMD(command,check_name=None):
    checkresult = subprocess.getstatusoutput('%s %s'%(command,check_name))
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

def url_extract_doain(url):
    if re.match('^http://',url):
        domain = re.sub('^http://','',url)
        domain = domain.split('/')[0]
        return domain
    elif re.match('^https://',url):
        domain = re.sub('https://','',url)
        domain = domain.split('/')[0]
        return domain
    else:return url

def getDomain(domain):
    root_doamin = [".com", ".cn", ".com.cn", ".gov", ".net", ".edu.cn", ".net.cn", ".org.cn", ".co.jp", ".gov.cn", ".co.uk",
               "ac.cn", ".edu", ".tv", ".info", ".ac", ".ag", ".am", ".at", ".be", ".biz", ".bz", ".cc", ".de", ".es",
               ".eu", ".fm", ".gs", ".hk", ".in", ".info", ".io", ".it", ".jp", ".la", ".md", ".ms", ".name", ".nl",
               ".nu", ".org", ".pl", ".ru", ".sc", ".se", ".sg", ".sh", ".tc", ".tk", ".tv", ".tw", ".us", ".co", ".uk",
               ".vc", ".vg", ".ws", ".il", ".li", ".nz"]
    for root in root_doamin:
        regex = re.compile(r'[0-9a-zA-Z_-]+'+ root +'$')
        m = regex.findall(domain)
        if len(m) > 0:
            return m[0]