#!/usr/bin/python2
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description: 
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019-06-20
 * Time: 下午3:58
'''

from base.basemethod import CMD
import os
class nginx_server:

    conf_dir = 'C:\\Users\\jeak_\\Downloads\\nginx-1.17.0\\nginx-1.17.0\\conf'


    def get_conf_itme(self):
        items = os.listdir(self.conf_dir)
        return items

    def grep_Keyword(self,keyword,path):
        pass

    def get_nginx_config(self):
        pass

    def analysis_nginx_config(self):
        pass

    def update_nignx_config(self):
        pass

    def restart_nginx_to_effective(self):
        command = 'systemctl restart '
        server_name = 'nginx'
        cmd = CMD(command,server_name)
        return cmd

