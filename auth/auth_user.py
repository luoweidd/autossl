#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/12 2:38
# @Author  : luowei
# @FileName: auth_user.py
# @Software: PyCharm
# @Blog    ：http://……

import json
from functools import wraps
from flask.sessions import SecureCookieSession
from base.mylog import loglog
from base import basemethod
from base.msgdict import msg
from auth.user_model import user_modle



class user:

    _User = "admin"
    _Passwd = "fba5b21c21c0c82d29645532680d7a20"
    #_mwpasswd = 'J0oIJ1%$2'
    session_main = SecureCookieSession()
    res = msg()
    log = loglog.logger

    def passwd_md5(self,passwd):
        passwd_md5 = basemethod.MD5(passwd)
        return passwd_md5

    def login_validation(self,users):
        if users != None or users != '':
            user_model = user_modle()
            user_all = user_model.read_user_data()
            for i in user_all:
                if users['user'] == i['name'] and users['passwd'] == i['passwd']:
                    self.session_main['user'] = users['user']
                    return '登录成功'
            return '用户名密码错误。'
        return '用户名密码不能为空。'

    def logout_clear(self):
        resutl = self.session_main.pop("user")
        return resutl






