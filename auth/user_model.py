#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description:  
 * Project : autossl
 * Ide tools : PyCharm
 * File name : user_model.py
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019/7/23
 * Time: 上午10:49
'''

import json,os

class user_modle:

    base_path = os.getcwd()
    user_data_file = "./userdata.dat"
    file_path = "%s%s" % (base_path, user_data_file[1::])

    def __init__(self,user = None,passwd = None,channle = None):
        self.name = user
        self.passwd = passwd
        self.channle = channle

    def create_modle_data(self,user):
        '''
        初始化用户清空userdata数据，重新写入
        :param user: user集合：{"name":"name","passwd":"passwd","channle":"channle"}
        :return: True
        '''
        with open(self.file_path,'w+')as f:
            f.writelines(user);
            return True

    def create_append_user(self,user):
        '''
        新添加用户追加到userdata中
        :param user: user集合：{"name":"name","passwd":"passwd","channle":"channle"}
        :return: True
        '''
        with open(self.file_path,'a+')as f:
            f.writelines("\n%s"%user);
            return True

    def create_new_user(self):
        user_all = self.read_user_data()
        user = {"name":self.name,"passwd":self.passwd,"channle":self.channle}
        for i in user_all:
            if user['name'] == i["name"]:
                return '用户已存在，请更换用户名。'
        else:
            user = json.dumps(user)
            create_stus = self.create_append_user(user)
            if create_stus is True:
                return True
            return '数据写入失败。'

    def read_user_data(self):
        with open(self.file_path,'r')as f:
            data = f.readlines()
            new_data = []
            for i in data:
                new_data.append(json.loads(i))
        return new_data

    def get_user_channle(self,name):
        user_list = self.read_user_data()
        for i in user_list:
            if name == 'admin':
                return '0'
            if name == i["name"]:
                return i['channle']

    def delete_user(self,del_user):
        user_all = self.read_user_data()
        for i in user_all:
            if del_user == i['name']:
                user_all.remove(i)
        rewreite_data = self.new_data_write_user_data(user_all)
        res = self.create_modle_data(rewreite_data)
        return res

    def update_passwd(self,user):
        user_all = self.read_user_data()
        for i in user_all:
            if user["name"] == i["name"]:
                if user["old_passwd"] == i["passwd"]:
                    i["passwd"] = user["passwd"]
                else:
                    return '旧密码输入错误，密码修改失败。'
        rewreite_data = self.new_data_write_user_data(user_all)
        res = self.create_modle_data(rewreite_data)
        return res

    def new_data_write_user_data(self,res):
        tmp = ''
        for i in res:
            tmp += '%s\n'%json.dumps(i)
        return tmp[:-1]

if os.path.exists(user_modle.file_path) is False:
    _name = "admin"
    _passwd = "fba5b21c21c0c82d29645532680d7a20"
    #passwd: J0oIJ1%$2
    _channle = "admin"

    user = {"name": _name, "passwd": _passwd, "channle": _channle}
    user_modl = user_modle()
    user_modl.create_modle_data(json.dumps(user))