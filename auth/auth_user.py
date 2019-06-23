#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/12 2:38
# @Author  : luowei
# @FileName: auth_user.py
# @Software: PyCharm
# @Blog    ：http://……

import json
from functools import wraps
from flask import sessions
from base.mylog import loglog
from base import basemethod

class user:
    User = "admin"
    Passwd = "123456"
    log = loglog.logger
    session_cookie = sessions.SecureCookieSession()

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

    def login_validation(self):
        pass

    def logout_clear(self):
        pass

    def login_check(func):
        @wraps(func)
        def login(users):
            User = user()
            if users["user"] == User.User and users["passwd"] == User.Passwd:
                '''补齐功能'''
                result = func(users)
            else:
                return '请登录'

        return '非法请求，请按正确方式访问。'
