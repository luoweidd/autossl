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
from DBL._sys_config import sys_config
from servsers.nginx_server import nginx_server
from base.mylog import loglog

class update_name_server_contrllo:

    logs = loglog()
    log = logs.logger

    def nginx_config_options(self,old_domain,new_domain,new_pem,new_key):
        nginx_servers = nginx_server()
        nginx_config_paths = [nginx_server.conf_dir_1,nginx_servers.conf_dir_2]
        for i in nginx_config_paths:
            nginx_config_paths_list = nginx_servers.get_conf_item_path(i)
            for j in nginx_config_paths_list:
                nginx_config_data = nginx_servers.keyword_get_conf_path(old_domain,j)
                if nginx_config_data != None:
                    old_pem = nginx_servers.get_pem_and_key_path(nginx_config_data)[0]
                    old_key = nginx_servers.get_pem_and_key_path(nginx_config_data)[1]
                    new_domain_nginx_config_data = nginx_servers.update_config_data(old_domain,new_domain,nginx_config_data)
                    new_pem_nginx_config_data = nginx_servers.update_config_data(old_pem,new_pem,new_domain_nginx_config_data)
                    new_key_nignx_config_data = nginx_servers.update_config_data(old_key,new_key,new_pem_nginx_config_data)
                    update_res = nginx_servers.update_nignx_config(new_key_nignx_config_data,j)
                    self.log.info(update_res)
                self.log.error('未读取到匹配的配置数据，请联系管理员检查。')
                return '未读取到匹配的配置数据，请联系管理员检查。'
        nginx_config_status = nginx_servers.nginx_conf_check()
        if nginx_config_status == None:
            nginx_server_status = nginx_servers.restart_nginx_to_effective()
            return nginx_server_status

    def update_DB(self,Id,itemVal):
        sys_db = sys_config()
        db_ = sys_db.update_collection_all(Id,itemVal)
        return db_

    def update_contrllor(self,**kwargs):
        '''
        Update the nginx configuration and restart the service for the new configuration to take effect.
        If the new service configuration takes effect and there are no exceptions, the database configuration is updated.
        :param kwargs:Contains the database ID where the data is located, the new data value, and the old domain name that needs to be updated.
        :return:configuration result.
        '''
        nginx_update_status = self.nginx_config_options(kwargs["old_domain"],kwargs["new_domain"],kwargs["new_pem"],kwargs["new_key"])
        if nginx_update_status == 'ok':
            db_update_status = self.update_DB(kwargs['Id'],kwargs["itemVal"])
            return db_update_status
        return nginx_update_status