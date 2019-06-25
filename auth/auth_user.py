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
from base.msgdict import msg


def login_check(func):
    res = msg()
    @wraps(func)
    def login():

        User = user()
        if sessions["user"] == User._User and sessions["passwd"] == User._Passwd:
            result = func()
            return result
        else:
            result = msg.getmsg(10)
            return result
    remsg = res.getmsg(11)
    return res.msg(remsg)

class user:
    res = msg()
    _User = "admin"
    _Passwd = "123456"
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


