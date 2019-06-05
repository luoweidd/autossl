#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description: 
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019-06-05
 * Time: 下午2:59
'''

# Let's Encrypt ACME Version 2 Examples - Create Certificate Key
import os
from Crypto.PublicKey import RSA

def make_certificate_key(domainname):
    filename = './%s/%s.key'%(domainname,domainname)
    key = RSA.generate(4096)
    if not os.path.exists(domainname):
        os.makedirs('./%s'%domainname,mode=0775)
    with open(filename,'w') as f:
        f.write(key.exportKey().decode('utf-8'))

# make_certificate_key('3123123.com')