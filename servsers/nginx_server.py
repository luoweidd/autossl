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

    conf_dir = '/etc/nginx/conf.d/'
    conf_dir_ = '/etc/nginx/sites-enabled/'


    def get_conf_itme(self,conf_path):
        items = os.listdir(conf_path)
        if len(items) > 0 or items != None:
            return items
        return None

    def get_conf_path(self,keyword,path):
        pass

    def get_nginx_config(self,conf_name):
        pass

    def analysis_nginx_config(self,conf_content):
        pass

    def update_nignx_config(self,conf_content,conf_name):
        pass

    def restart_nginx_to_effective(self):
        command = 'systemctl restart '
        server_name = 'nginx'
        cmd = CMD(command,server_name)
        return cmd

    def add_Anti_seal_conf(self,domain,pem,key):
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
