#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/12 2:38
# @Author  : luowei
# @FileName: auth_user.py
# @Software: PyCharm
# @Blog    ：http://……

import json

class user:
    User = "admin"
    Passwd = "123456"

    def init_user(self):
        pass

    def read_file(self):
        with open("user",'r+') as f:
            read = f.readlines()
            f.close()
            return read

    def write_file(self,data):
        pass