#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description:  
 * Project : autossl
 * Ide tools : PyCharm
 * File name : user_contrllo.py
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019/7/24
 * Time: 上午8:57
'''

from auth.user_model import user_modle
from  DBL.tb_user import tb_user
from base.mylog import loglog
import json

class user_contrlor:

    log = loglog.logger

    def add_new_user(self,user_dict):
        user_contr = user_modle(user_dict["name"],user_dict["passwd"],user_dict["channle"])
        status = user_contr.create_new_user()
        if status == True:
            return 'ok'
        return status

    def delete_old_user(self,username):
        user_contr = user_modle()
        status = user_contr.delete_user(username.decode("utf-8"))
        if status == True:
            return 'ok'
        return status

    def update_old_user(self,update_dict):
        user_contr = user_modle()
        status = user_contr.update_passwd(update_dict)
        if status == True:
            return 'ok'
        return status

    def get_all_user(self):
        user_object = user_modle()
        users = user_object.read_user_data()
        user_list = []
        for i in users:
            i.pop("passwd")
            user_list.append(i)
        return user_list

    def get_all_channelId(self):
        user_ = tb_user()
        user = user_.get_all_channle()
        user_list = []
        for i in user:
            if i :
                if i not in user_list and i["channelId"] != 'admin':
                    user_list.append(i)
        return user_list

    def all_channelId_LIST(self):
        all_channleid =self.get_all_channelId()
        all_channle = []
        for i in all_channleid:
            all_channle.append(i["channelId"])
        return all_channle