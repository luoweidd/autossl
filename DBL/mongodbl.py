#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/23 16:22
# @Author  : luowei
# @FileName: mongodbl.py
# @Software: PyCharm
# @Blog    ：http://……

import pymongo
from base.mylog import loglog

class mongoDBL:

    _log = loglog()
    log = _log.logger

    def __init__(self):

        # mongodb: // user:passwd @ localhost:27017 /?authSource = game_server
        self.database = 'red_packet_game_server'
        self.db_user = ''
        self.db_passwd = ''
        self._connect_str = 'mongodb://127.0.0.1:27017/%s?authSource=%s' % (self.database, self.database)

    def DBConect(self):
        try:
            connection=pymongo.MongoClient(self._connect_str)
            db=connection.get_database(self.database)
            connection.close()
            return db
        except Exception as e:
            self.log.error("连接错误，错误消息：%s"%e)

