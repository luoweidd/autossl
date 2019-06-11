#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description: 
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019-06-11
 * Time: 上午9:49
'''

import requests
import logging

class ssl_cert_v2:

    log=logging.getLogger("lw-ghy-acme")

    base_path = 'https://acme-staging-v02.api.letsencrypt.org/'

    #request headers
    headers = {
        'User-Agent': 'lw-ghy-acme-client/1.0',
        'Accept-Language': 'zh',
    }

    #new resources path
    directory="directory"
    nonec_path="newNonce"
    nonec="Replay-Nonce"
    account_path="newAccount"
    order_path="newNonce"
    Authz_path="newAuthz"
    revokeCert="revokeCert"
    keyChange="keyChange"

    def get_directory(self):
        try:
            directorys = requests.get(self.base_path, headers=self.headers)
        except requests.exceptions.RequestException as error:
            self.log.info(error)
        return directorys

    def get_nonce(self):
        directorys = self.get_directory()
        dir_json = directorys.json()
        new_nonec_path = dir_json[self.nonec_path]
        nonce = requests.head(new_nonec_path).headers[self.nonec]
        return nonce

