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
from nginx_server.nginxextension import socketclient
from channle.channle_modle import channlemodle
from auth.auth_user import user
import re,json

class update_name_server_contrllo:

    logs = loglog()
    log = logs.logger
    user_obj = user()
    session = user_obj.session_main

    # old local nginx config option function
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
                                if dict_nginx_conf != None and re.match('\*\.%s;'%old_domain,dict_nginx_conf['server_1'][3]["server_name"]) and re.match('\*\.%s;'%old_domain[1::],dict_nginx_conf["server_2"][3]['server_name']):
                                    dict_nginx_conf['server_2'][5]["ssl_certificate"] = '%s;'%new_pem
                                    dict_nginx_conf['server_2'][6]["ssl_certificate_key"] = '%s;'%new_key
                                    dict_nginx_conf['server_1'][3]["server_name"] = '*%s;'%new_domain
                                    dict_nginx_conf["server_2"][3]['server_name'] = '*%s;'%new_domain
                                    new_conf_data = nginx_servers.nginx_config_write_buffer_fomat(dict_nginx_conf)
                                    update_res = nginx_servers.wirte_file_optertion(j,new_conf_data)
                                    self.log.error(update_res)
                                    if update_res == 'ok':
                                        nginx_config_status = nginx_servers.nginx_conf_check()
                                        self.log.error(nginx_config_status)
                                        if nginx_config_status[0] == 0:
                                            nginx_server_status = nginx_servers.restart_nginx_to_effective()
                                            self.log.info(nginx_server_status)
                                            return nginx_server_status
                                        self.log.info('配置检查不通过，请通知管理员检查配置文件，以及系统。错误信息：%s'%nginx_config_status[1])
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
            add_conf = nginx_servers.add_Anti_seal_conf(new_domain[1::],new_pem,new_key)
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

    # new network nginx config option function
    def update_contrllor(self,kwargs):
        '''
        Update the nginx configuration and restart the service for the new configuration to take effect.
        If the new service configuration takes effect and there are no exceptions, the database configuration is updated.
        :param kwargs:Contains the database ID where the data is located, the new data value, and the old domain name that needs to be updated.
        :return:configuration result.
        '''
        new_domain = url_extract_doain(kwargs['new_domain'])
        old_domain = url_extract_doain(kwargs['old_domain'])
        # nginx_update_status = self.nginx_config_options(old_domain,new_domain,kwargs["new_pem"],kwargs["new_key"])   #version v_1.0.x
        from base.basemethod import systemc_dir_flag,getDomain
        if re.match('^\.',new_domain):  #匹配到是以.开头的域名，则为域名添加*号
            ca_key_down_link = kwargs["request_host"]+'/static/certificate/'+new_domain[1:]+ systemc_dir_flag()+'certificate.pem' #version v_1.1.x
            privte_key_down_link = kwargs["request_host"]+'/static/certificate/'+new_domain[1:]+ systemc_dir_flag()+ 'privte.key' #version v_1.1.x
            new_domain = '*%s'%new_domain
            old_domain = '*%s'%old_domain
        else:
            ca_key_down_link = kwargs["request_host"]+'/static/certificate/'+getDomain(new_domain)+ systemc_dir_flag()+'certificate.pem' #version v_1.1.x
            privte_key_down_link = kwargs["request_host"]+'/static/certificate/'+getDomain(new_domain)+ systemc_dir_flag()+ 'privte.key' #version v_1.1.x
        #nginx配置客户端请求数据格式以及该接口字段要求
        '''
        heard：协议路由头
        msg：消息解析所必要字段
        msg-value：该路由请求必要字段[old_domain,domain,ca_key_down_link,privte_key_down_link]
        '''
        data = {"heard":"nginx_ssl_update","msg":{"old_domain":old_domain,"domain":new_domain,"ca_key_down_link":ca_key_down_link,"privte_key_down_link":privte_key_down_link}} #version v_1.1.x
        Channle = channlemodle()
        client_address = (Channle.get_channle_addr(kwargs["channlename"]))
        if client_address != None:
            recv_res = self.send_client(client_address,data)
            if  recv_res != '客户端不在线，请核实是否已停止。':
                client_res = self.updata_conf_update_db(kwargs,recv_res)
                return client_res
        return '远程客户端主机配置不存在或远程主机客服端服务不在线，请检查渠道主机配置。'

    def updata_conf_update_db(self,kwargs,recv_res):
        try:
            recv_res = json.loads(recv_res)
            if recv_res["msg"]:
                if recv_res["msg"][0] == 0:
                    db_update_status = self.update_DB(kwargs['Id'],kwargs["new_domain"])
                    if db_update_status.modified_count > 0 or db_update_status.matched_count > 0:
                        return 'ok'
                    else:
                        return '数据未做任何修改！但执行成功。'
            return recv_res
        except KeyError:
            self.log.error(recv_res["error"])
            return recv_res["error"]
        except Exception as e:
            self.log.error(e)
            return e

    #new network update nginx config send data function
    def send_client(self,args,data):
        '''

        :param args:client address <type>:tupel
        :param data:
        :return:
        '''
        try:
            socket_client = socketclient(args)
            socket_client.data_send(json.dumps(data))
            recv_res = socket_client.recv()
            if recv_res == '服务连接断开':
                socket_client.data_send(json.dumps(data))
                recv_res = socket_client.recv()
            return recv_res
        except Exception as e:
            try:
                socket_client.client.close()
            except UnboundLocalError:
                return '客户端不在线，请核实是否已停止。'
            if e is object:
                for i in e:
                    self.log.error(i)
            else:
                self.log.error(e)

    def new_conf_contrllo(self,domain,request_host):
        new_domain = url_extract_doain(domain)
        # nginx_update_status = self.nginx_config_options(old_domain,new_domain,kwargs["new_pem"],kwargs["new_key"])   #version v_1.0.x
        from base.basemethod import systemc_dir_flag,getDomain
        if re.match('^\.',new_domain):  #匹配到是以.开头的域名，则为域名添加*号
            ca_key_down_link = request_host+'/static/certificate/'+new_domain[1:]+ systemc_dir_flag()+'certificate.pem' #version v_1.1.x
            privte_key_down_link = request_host+'/static/certificate/'+new_domain[1:]+ systemc_dir_flag()+ 'privte.key' #version v_1.1.x
            new_domain = '*%s'%new_domain
        elif re.match('^\*\.',new_domain):
            new_domain = new_domain[2:]
            ca_key_down_link = request_host+'/static/certificate/'+new_domain+ systemc_dir_flag()+'certificate.pem' #version v_1.1.x
            privte_key_down_link = request_host+'/static/certificate/'+new_domain+ systemc_dir_flag()+ 'privte.key' #version v_1.1.x
        else:
            ca_key_down_link = request_host+'/static/certificate/'+new_domain+ systemc_dir_flag()+'certificate.pem' #version v_1.1.x
            privte_key_down_link = request_host+'/static/certificate/'+new_domain+ systemc_dir_flag()+ 'privte.key' #version v_1.1.x
        data = {"heard": "new_nginx_conf",
                "msg": {"domain": new_domain, "ca_key_down_link": ca_key_down_link,
                        "privte_key_down_link": privte_key_down_link}}
        from auth.user_model import user_modle
        User = user_modle()
        channle = User.get_user_channle(self.session.get('user'))
        self.log.info('Getting the clients remote address through the current session ,now login user: %s'%channle)
        Channle = channlemodle()
        client_address = (Channle.get_channle_addr(channle))
        if client_address != None:
            recv_res = self.send_client(client_address, data)
            if  recv_res != '客户端不在线，请核实是否已停止。':
                try:
                    return json.loads(recv_res)["msg"]
                except KeyError:
                    return json.loads(recv_res)["error"]
        return '远程客户端主机配置不存在或远程主机客服端服务不在线，请检查渠道主机配置。'