#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/23 16:26
# @Author  : luowei
# @FileName: _sys_config.py
# @Software: PyCharm
# @Blog    ：http://……

from DBL.mongodbl import mongoDBL
from base.mylog import loglog

class sys_config:

    _log = loglog()
    log = _log.logger

    def __init__(self):
        try:
            _mongoconnect = mongoDBL()
            self.cur = _mongoconnect.DBConect()
            self.collection="sys_config"
        except Exception as e:
            self.log.error("连接错误，错误消息：%s"%e)

    def get_collection_all(self):
        try:
            collec = self.cur.get_collection(self.collection).find({'eflag':1},{"itemName","itemVal","channelId"})
            return collec
        except Exception as e:
            self.log.error( "获取%s数据错误，错误消息：%s"%(self.collection,e))

    def bychannelid_get_collection_all(self,channleid):
        try:
            collec = self.cur.get_collection(self.collection).find({'eflag':1,"channelId":channleid},{"itemName","itemVal","channelId"})
            return collec
        except Exception as e:
            self.log.error( "获取%s数据错误，错误消息：%s"%(self.collection,e))

    def server_list(self):
        try:
            server_list_all = self.get_collection_all()
            list_all = []
            for i in server_list_all:
                list_all.append(i)
            return list_all
        except Exception as e:
            self.log.error(e)

    def bychannle_server_list(self,channleid):
        try:
            server_list_all = self.bychannelid_get_collection_all(channleid)
            list_all = []
            for i in server_list_all:
                list_all.append(i)
            return list_all
        except Exception as e:
            self.log.error(e)

    def update_collection(self,Id,itemVal):
        try:
            collec = self.cur.get_collection(self.collection).update_one({"_id":int(Id)},{'$set':{"itemVal":itemVal}})
            return collec
        except Exception as e:
             self.log.error("更新%s数据错误，错误消息：%s"%(self.collection,e))
             return