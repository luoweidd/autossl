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
from nginx_server.nginx_server import nginx_server
from base.mylog import loglog
from base.basemethod import url_extract_doain
import re

class update_name_server_contrllo:

    logs = loglog()
    log = logs.logger

    def nginx_config_options(self,old_domain,new_domain,new_pem,new_key):
        nginx_servers = nginx_server()
        nginx_config_paths = [nginx_server.conf_dir_1,nginx_servers.conf_dir_2]
        for i in nginx_config_paths:
            nginx_config_paths_list = nginx_servers.get_conf_item_path(i)
            for j in nginx_config_paths_list:
                nginx_config_data = nginx_servers.read_config(j)
                if nginx_config_data != None:
                    if len(nginx_config_data) > 1:
                        remove_notes_comments = nginx_servers.remove_notes_comments(nginx_config_data)
                        if remove_notes_comments != None:
                            dict_nginx_conf = nginx_servers.get_nginx_config(remove_notes_comments)
                            if re.match('^\.',old_domain):
                                if dict_nginx_conf != None and re.match('%s;'%old_domain[1::],dict_nginx_conf['server_1'][3]["server_name"]) and re.match('\*\.%s;'%old_domain[1::],dict_nginx_conf["server_2"][3]['server_name']):
                                    dict_nginx_conf['server_2'][5]["ssl_certificate"] = '%s;'%new_pem
                                    dict_nginx_conf['server_2'][6]["ssl_certificate_key"] = '%s;'%new_key
                                    dict_nginx_conf['server_1'][3]["server_name"] = '%s;'%new_domain[1::]
                                    dict_nginx_conf["server_2"][3]['server_name'] = '*%s;'%new_domain
                                    new_conf_data = nginx_servers.nginx_config_write_buffer_fomat(dict_nginx_conf)
                                    update_res = nginx_servers.wirte_file_optertion(j,new_conf_data)
                                    self.log.error(update_res)
                                    if update_res != None:
                                        nginx_config_status = nginx_servers.nginx_conf_check()
                                        if nginx_config_status[0] == 0:
                                            nginx_server_status = nginx_servers.restart_nginx_to_effective()
                                            return nginx_server_status
                                        self.log.error('配置检查不通过，请通知管理员检查配置文件，以及系统。错误信息：%s'%nginx_config_status[1])
                                        return '配置检查不通过，请通知管理员检查配置文件，以及系统。'
                                    return '更新配置文件错误。'
                            else:
                                if dict_nginx_conf != None and re.match('%s;'%old_domain,dict_nginx_conf['server_1'][3]["server_name"]) and re.match('%s;'%old_domain,dict_nginx_conf["server_2"][3]['server_name']):
                                    dict_nginx_conf['server_2'][5]["ssl_certificate"] = '%s;'%new_pem
                                    dict_nginx_conf['server_2'][6]["ssl_certificate_key"] = '%s;'%new_key
                                    dict_nginx_conf['server_1'][3]["server_name"] = '%s;'%new_domain
                                    dict_nginx_conf["server_2"][3]['server_name'] = '%s;'%new_domain
                                    new_conf_data = nginx_servers.nginx_config_write_buffer_fomat(dict_nginx_conf)
                                    update_res = nginx_servers.wirte_file_optertion(j,new_conf_data)
                                    self.log.error(update_res)
                                    if update_res != None:
                                        nginx_config_status = nginx_servers.nginx_conf_check()
                                        if nginx_config_status[0] == 0:
                                            nginx_server_status = nginx_servers.restart_nginx_to_effective()
                                            return nginx_server_status
                                        self.log.error('配置检查不通过，请通知管理员检查配置文件，以及系统。错误信息：%s'%nginx_config_status[1])
                                        return '配置检查不通过，请通知管理员检查配置文件，以及系统。'
                                    return '更新配置文件错误。'
            # self.log.error('未读取到匹配的配置数据，请联系管理员检查。')
            # return '未读取到匹配的配置数据，请联系管理员检查。'
            add_conf = nginx_servers.add_Anti_seal_conf(new_domain,new_pem,new_key)
            if add_conf:
                nginx_config_status = nginx_servers.nginx_conf_check()
                if nginx_config_status[0] == 0:
                    nginx_server_status = nginx_servers.restart_nginx_to_effective()
                    return nginx_server_status
                self.log.error('配置检查不通过，请通知管理员检查配置文件，以及系统。错误信息：%s' % nginx_config_status[1])
                return '配置检查不通过，请通知管理员检查配置文件，以及系统。'
            self.log.error("添加配置失败，联系管理员检查。")
            return '添加配置失败，联系管理员检查。'

    def update_DB(self,Id,itemVal):
        sys_db = sys_config()
        db_ = sys_db.update_collection(Id,itemVal)
        return db_

    def update_contrllor(self,kwargs):
        '''
        Update the nginx configuration and restart the service for the new configuration to take effect.
        If the new service configuration takes effect and there are no exceptions, the database configuration is updated.
        :param kwargs:Contains the database ID where the data is located, the new data value, and the old domain name that needs to be updated.
        :return:configuration result.
        '''
        new_domain = url_extract_doain(kwargs['new_domain'])
        old_domain = url_extract_doain(kwargs['old_domain'])
        nginx_update_status = self.nginx_config_options(old_domain,new_domain,kwargs["new_pem"],kwargs["new_key"])
        if nginx_update_status[0] == 0:
            db_update_status = self.update_DB(kwargs['Id'],kwargs["new_domain"])
            if db_update_status.modified_count > 0 or db_update_status.matched_count > 0:
                return 'ok'
            else:
                return '数据未做任何修改！但执行成功。'
        return nginx_update_status