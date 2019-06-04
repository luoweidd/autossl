#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description: 
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019-06-04
 * Time: 上午10:55
'''

from base.basemethod import CMD
from requests import Request,Response
import requests

class autossl:

    _base_url='https://acme-v02.api.letsencrypt.org'

    def generatessl(self,domain):
        cmd=CMD('certbot certonly --manual --preferred-challenges dns -d %s'%domain)
        return cmd
    def DNSverification(self):
        pass

    def acmerequest(self,uri,headers=None,**kwargs):
        req=Request()
        req.url='%s%s'%self._base_url,uri
        req.headers=headers
        req.params=kwargs
        requests.request(req)


    def newnonce(self):
        req=requests
        req.url='%s/acme/new-nonce'
        result=requests.request(req)
        return result

    def newacct(self):
        req=requests
        req.headers={"Content-Type":"application/jose+json"}
        req.params={}
        req.url='https://acme-v02.api.letsencrypt.org/acme/new-acct'
        result=requests.request(req)
        return result

    def neworder(self):
        req=requests
        req.__url__='https://acme-v02.api.letsencrypt.org/directory'
        result=requests.request(req)
        return result