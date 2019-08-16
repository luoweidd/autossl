#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description:  
 * Project : autossl
 * Ide tools : PyCharm
 * File name : channle_modle.py
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019/8/15
 * Time: 下午3:49
'''

import os,json

class channlemodle:

    base_path = os.getcwd()
    user_data_file = "./channal.dat"
    _module_file = "%s%s" % (base_path, user_data_file[1::])

    def __init__(self,channle = None,channle_Seal_proof_mainframe = None,channle_Seal_proof_port = None):
        self.channle = channle
        self.channle_Seal_proof_mainframe = channle_Seal_proof_mainframe
        self.channle_Seal_proof_port = channle_Seal_proof_port

    def create_modle_data(self,channle):
        '''
        初始化用户清空channledata数据，重新写入
        :param channle: channle集合：{"channle":"channle","channle_Seal_proof_mainframe":"channle_Seal_proof_mainframe","channle_Seal_proof_port":"channle_Seal_proof_port"}
        :return: True
        '''
        with open(self._module_file,'w+')as f:
            f.writelines(channle);
            return True

    def create_append_channle(self,channle):
        '''
        新添加用户追加到channledata中
        :param channle: channle集合：{"channle":"channle","channle_Seal_proof_mainframe":"channle_Seal_proof_mainframe","channle_Seal_proof_port":"channle_Seal_proof_port"}
        :return: True
        '''
        with open(self._module_file,'a+')as f:
            f.writelines("\n%s"%channle);
            return True

    def create_new_channle(self):
        channle = {"channle":self.channle,"channle_Seal_proof_mainframe":self.channle_Seal_proof_mainframe,"channle_Seal_proof_port":self.channle_Seal_proof_port}
        create_stus = self.create_append_channle(json.dumps(channle))
        if create_stus is True:
            return True
        return '数据写入失败。'


    def read_channle_data(self):
        with open(self._module_file,'r')as f:
            data = f.readlines()
            new_data = []
            for i in data:
                import re
                if re.search('\n',i):
                    i = i.replace('\n','')
                new_data.append(json.loads(i))
        return new_data

    def get_channle_addr(self,channle):
        channle_list = self.read_channle_data()
        for i in channle_list:
            if channle == i['channle']:
                return (i["channle_Seal_proof_mainframe"],i["channle_Seal_proof_port"])

    def delete_channle(self,del_channle):
        user_all = self.read_channle_data()
        for i in user_all:
            if del_channle == i['channle']:
                user_all.remove(i)
        rewreite_data = self.new_data_write_channle_data(user_all)
        res = self.create_modle_data(rewreite_data)
        return res

    def update_host(self):
        channle_all = self.read_channle_data()
        for i in channle_all:
            if self.channle == i["channle"]:
                i["channle_Seal_proof_mainframe"] = self.channle_Seal_proof_mainframe
                i["channle_Seal_proof_port"] = self.channle_Seal_proof_port
        rewreite_data = self.new_data_write_channle_data(channle_all)
        res = self.create_modle_data(rewreite_data)
        return res

    def new_data_write_channle_data(self,res):
        tmp = ''
        for i in res:
            tmp += '%s\n'%json.dumps(i)
        return tmp[:-1]

    def all_channel_LIST(self):
        all_channleid =self.read_channle_data()
        all_channle = []
        for i in all_channleid:
            all_channle.append(i["channle"])
        return all_channle

if os.path.exists(channlemodle._module_file) is False:
    _channle = '0'
    _channle_Seal_proof_mainframe = '127.0.0.1'
    _channle_Seal_proof_port = 8782

    user = {"channle": _channle, "channle_Seal_proof_mainframe":_channle_Seal_proof_mainframe, "channle_Seal_proof_port":_channle_Seal_proof_port}
    user_modl = channlemodle()
    user_modl.create_modle_data(json.dumps(user))