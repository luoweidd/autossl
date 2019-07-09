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
from base.mylog import loglog
import os

class nginx_server:

    conf_dir_1 = '/etc/nginx/conf.d/'
    conf_dir_2 = '/etc/nginx/sites-enabled/'
    logs = loglog()
    log = logs.logger

    __doc__ = '''
    This class provides two functions. One is to get the configuration file according to 
    the parameters of the incoming path and convert it into a dictionary object. 
    The other is to write the configuration file according to the input road 
    strength parameters. Specifically:

        The nginx configuration file excludes all annotated file data..


        The nginx configuration object is converted and written to the configuration file. 
        (Write the corresponding file according to the parameters of the incoming path. 
        Note that the writing mode here is:'W+', so delete the original data writing.) 
        Create a new write if the file is not pure.
    '''



    def get_conf_itme(self,conf_path):
        '''
        Get param path dir list.
        :param conf_path: config path
        :return: path dir list
        '''
        items = os.listdir(conf_path)
        if len(items) > 0 or items != None:
            return items
        return None

    def get_conf_item_path(self,conf_path):
        '''
        Get the list of all items in the incoming path, and then update the absolute path of the list file to encapsulate the new list.
        :param conf_path:dir path ,must absolute path.
        :return:absolute path of the list file to encapsulate the new list
        '''
        dir_itme = self.get_conf_itme(conf_path)
        if dir_itme != None:
            new_conf_dir_1_itme = []
            for i in dir_itme:
                new_path = '%s%s'%(conf_path,i)
                new_conf_dir_1_itme.append(new_path)
            return new_conf_dir_1_itme

    def read_config(self,file_path):
        '''
        read configtion files
        :return: data
        '''
        try:
            with open(file_path,'rt')as f:
                data = f.readlines()
                if data != None:
                    return data
                return None
        except Exception as e:
            print(e)
            self.log.error('文件读取异常，请留意。')
            return None

    def remove_notes_comments(self,conf_file_date_obj):
        '''
        Delete configuration file comments.
        :param conf_file_date_obj:
        :return: no comments data
        '''
        data = []
        for i in conf_file_date_obj:
            import re
            if re.search('#',i) == None:
                data.append(i)
        return data

    def get_nginx_config(self, data_buffer):
        '''
        Nginx configuration file data is parsed into dictionary objects.
        :param data_buffer: Bufer after excluding comments
        :return: dict or error
        '''
        try:
            import re
            nodes = {}
            node_name = 'server'
            node_conut = 0
            for i in data_buffer:
                i_n = i.replace('\n', '')
                i_ = i_n.strip(' ')
                if re.match('^%s$'%node_name, i_) or re.match('^%s {'%node_name, i_):
                    node = []
                    node.append(i_)
                    node_conut += 1
                    node_ = '%s_%d' % (node_name, node_conut)
                elif re.match('{', i_):
                    node.append(i_)
                    continue
                elif re.match('}', i_):
                    node.append(i_)
                    nodes.update({node_: node})
                    continue
                else:
                    node.append(i_)

            conf = {}
            for j in nodes:
                server = []
                for p in nodes[j]:
                    h = p.split(' ')
                    blank_count = h.count('')
                    if blank_count >= 1:
                        for n in range(0, blank_count):
                            h.remove('')
                    conf_dict = {}
                    if h == [] or h == None:
                        continue
                    elif len(h) > 2 and re.match('^location', h[0]) == None:
                        conf_dict.update({h[0]: h[1::]})
                        server.append(conf_dict)
                    elif len(h) > 1 and len(h) <= 2:
                        conf_dict.update({h[0]: h[1]})
                        server.append(conf_dict)
                    elif re.match('^location', h[0]):
                        string = ''
                        for e in h:
                            string += ' %s' % e
                        server.append(string)
                    else:
                        server.append(h[0])
                conf.update({j: server})
            return conf
        except Exception as e:
            self.log.error( 'Conversion error，error info：%s'%e.__context__)
            return None

    def nginx_config_write_buffer_fomat(self, config_object_data):
        '''
        nginx configtion write config file
        :param config_object_data: file buffer
        :return: ok or error
        '''
        try:
            string_buffer = ''
            for i in config_object_data:
                for j in config_object_data[i]:
                    if type(j) == dict:
                        for n in j:
                            tmp = ''
                            if type(j[n]) == list:
                                for k in j[n]:
                                    tmp += ' %s' % k
                                string_buffer += '    %s %s\n' % (n, tmp)
                            else:
                                string_buffer += '    %s %s\n' % (n, j[n])
                    else:
                        string_buffer += '%s\n' % j
            return string_buffer
        except Exception as e:
            self.log.error( 'Wirte error,error info:%s' % e)
            return None

    def wirte_file_optertion(self, wirte_config_path, str_buffer):
        '''
        write opertion
        :param wirte_config_path: /etc/nginx/conf.d/xxx.conf
        :param str_buffer: Nginx recognizable format.
        :return: ok or error
        '''
        if str_buffer != None:
            try:
                with open(wirte_config_path, 'w')as f:
                    f.write(str_buffer)
                    return 'ok'
            except Exception as e:
                self.log.error( 'Write file error, error info:%s' % e)
                return None
        return None

    def restart_nginx_to_effective(self):
        '''
        Execute the system shell command and restart the nginx service.
        :return:
        '''
        command = 'systemctl restart '
        server_name = 'nginx'
        cmd = CMD(command,server_name)
        return cmd

    def nginx_conf_check(self):
        '''
        Execute the system shell command and check the nginx config file.
        :return:
        '''
        command = 'nginx '
        options = '-t'
        cmd = CMD(command,options)
        if cmd != None:
            return cmd
        else:
            return 'ok'

    def add_Anti_seal_conf(self,domain,pem,key,conf_dir=None):
        '''
        Add the nginx service configuration of the anti-blocking site.
        :param domain:
        :param pem:
        :param key:
        :return:
        '''
        if domain != None and pem !=None and key != None:
            import time
            import hashlib
            import base64
            from ACME.myhelper import DomainDewildcards
            conf_name = base64.urlsafe_b64encode(hashlib.sha256(str(time.time()).encode('utf-8')).digest()).decode('utf-8').rstrip("=")
            domain = DomainDewildcards(domain)
            if conf_dir == None:
                conf_dir = self.conf_dir_1
            config_info = '''server
    {
            listen 80;
            server_name %s;
            rewrite ^(.*)$ https://${server_name}$1 permanent;
    }
    server
    {
        listen 443 ssl;
        server_name *.%s;
        ssl on;
        ssl_certificate   %s;
        ssl_certificate_key  %s;
        ssl_session_timeout 5m;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        location / {
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_pass http://127.0.0.1:8086;
                }
        access_log /var/log/nginx/fangfeng_access.log;
    }
            '''%(domain,domain,pem,key)
            try:
                with open('%s%s.conf'%(conf_dir,conf_name),'w+')as f:
                    f.write(config_info)
                    return True
            except IOError as e:
                return '系统没有写权限。'
