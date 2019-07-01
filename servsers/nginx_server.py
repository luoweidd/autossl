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
                new_path = '%s%s'%(self.conf_path,i)
                new_conf_dir_1_itme.append(new_path)
            return new_conf_dir_1_itme


    def keyword_get_conf_path(self,keyword,paths):
        '''
        Find documents according to key points.
        :param keyword: keyword
        :param paths: path list
        :return: Data object with keyword file
        '''
        for path in paths:
            with open(path,'rt')as f:
                data = f.readlines()
                if keyword in data:
                    return data

    def get_nginx_config(self,conf_file_date_obj):
        '''
        Delete configuration file comments.
        :param conf_file_date_obj:
        :return: no comments data
        '''
        data = ''
        for i in conf_file_date_obj:
            import re
            if re.match('#',i) == None:
                data +=i
        return data

    def get_pem_and_key_path(self,nginx_config_data):
        old_pem_flag = 'ssl_certificate'
        old_key_flage = 'ssl_certificate_key'
        for i in nginx_config_data:
            import re
            if re.match(old_pem_flag,i):
                old_pem_path = i.split('')[1].split(";")[0]
            elif re.match(old_key_flage,i):
                old_key_path = i.split(""[1]).split("")[0]
        return old_pem_path,old_key_path

    def update_config_data(self,new_content,old_content,repl_content):
        import re
        try:
            res = re.sub('%s'%old_content,new_content,repl_content)
            return res
        except Exception as e:
            self.log.error('ERROR:%s'%e)

    def update_nignx_config(self,conf_content,conf_name):
        '''
        Update nginx configuration file.
        :param conf_content:
        :param conf_name:
        :return: ''ok
        '''
        try:
            with open(conf_name,'wt')as f:
                f.writelines(conf_content)
                return 'ok'
        except Exception as e:
            self.log.error('ERROR:%s'%e)

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

    def add_Anti_seal_conf(self,domain,pem,key):
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
            conf_name = base64.urlsafe_b64encode(hashlib.sha256(str(time.time())).digest()).decode('utf-8').rstrip("=")
            domain = DomainDewildcards(domain)
            config_info = '''
            server
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
            with open('%s%s'%(self.conf_dir,conf_name),'w+')as f:
                f.write(config_info)
                return True
