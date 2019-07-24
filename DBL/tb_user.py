#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description:  
 * Project : autossl
 * Ide tools : PyCharm
 * File name : tb_user.py
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019/7/24
 * Time: 上午11:33
'''

from DBL.mongodb import mongoDB
from base.mylog import loglog

class tb_user:

    _log = loglog()
    log = _log.logger

    def __init__(self):
        try:
            _mongoconnect = mongoDB()
            self.cur = _mongoconnect.DBConect()
            self.collection="tb_user"
        except Exception as e:
            self.log.error("连接错误，错误消息：%s"%e)

    def get_all_channle(self):
        try:
            users = self.cur.get_collection(self.collection).find({},{"channelId":1,"_id":0})
            return users
        except Exception as e:
            self.log.error( "获取%s数据错误，错误消息：%s"%(self.collection,e))