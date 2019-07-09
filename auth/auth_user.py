#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/12 2:38
# @Author  : luowei
# @FileName: auth_user.py
# @Software: PyCharm
# @Blog    ：http://……

import json
from functools import wraps
from flask import Session
from base.mylog import loglog
from base import basemethod
from base.msgdict import msg




class user:

    _User = "admin"
    _Passwd = "fba5b21c21c0c82d29645532680d7a20"
    #_mwpasswd = 'J0oIJ1%$2'
    session_main = Session()
    res = msg()
    log = loglog.logger


    def init_user(self):
        pass

    def read_file(self):
        with open("user",'r+') as f:
            read = f.readlines()
            f.close()
            return read

    def write_file(self,data):
        pass

    def passwd_md5(self,passwd):
        passwd_md5 = basemethod.MD5(passwd)
        return passwd_md5

    def login_validation(self,users):
        if users != None or users != '':
            if users['user'] == self._User and users['passwd'] == self._Passwd:
                self.session_main['user'] = users['user']
                return '登录成功'
            return '用户名密码错误。'
        return '用户名密码不能为空。'

    def logout_clear(self):
        resutl = self.session_main.pop("user")
        return resutl






