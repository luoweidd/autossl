#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/23 16:26
# @Author  : luowei
# @FileName: _sys_config.py
# @Software: PyCharm
# @Blog    ：http://……

from mongodbl import mongoDBL

class sys_config:

    def __init__(self):
        try:
            _mongoconnect = mongoDBL()
            self.cur = _mongoconnect.conect_cur
            self.collection="sys.config"
        except Exception as e:
            print "连接错误，错误消息：%s"%e

    def gat_collection_all(self):
        try:
            collec = self.cur.get_collection(self.collection).find({"eflag":1})
            return collec
        except Exception as e:
            self.log.error( "获取%s数据错误，错误消息：%s"%(self.collection,e))

    def update_collection_all(self,Id,**kwargs):
        try:
            collec = self.cur.get_collection(self.collection).update_one({"_id":Id},kwargs)
            return collec
        except Exception as e:
             self.log.error("更新%s数据错误，错误消息：%s"%(self.collection,e))