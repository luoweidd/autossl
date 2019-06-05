#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description: 
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019-06-04
 * Time: 上午10:54
'''

from base.basemethod import get_os_info,CMD
from ACME.get_account_url import GetAccountURL
import subprocess

class certbot:

    _rpm_grep='rpm -qa|grep '
    _dpkg_grep='dpkg -qa|grep '
    _yum_yum='yum install '
    _os_info=get_os_info()

    def backcmd(self):
        os_info=self._os_info[0].split(' ')[0]
        if os_info == 'CentOS' or os_info == 'Redhat':
            return self._rpm_grep
        elif os_info == 'Ubuntu' or os_info == 'Debian' or os_info == 'Deepin' or os_info == 'Arch':
            return self._dpkg_grep
        else:
            print '不支持的系统版本：%s'%(str(self._os_info))

    def ComponentSupport(self,name):
        if self.backcmd() !=None:
            _command=CMD(self.backcmd(),name)
            print _command
            if _command == None:
                pro_command=CMD('%s%s* -y'%(self._yum_yum,name))
                if pro_command == '没有可用软件包 %s'%name:
                    creat_repo=CMD('touch /etc/yum.repos.d/epel.repo')
                    add_repo=CMD('''cat >> /etc/yum.repos.d/epel.repo << EOF
                    [epel]
                    name=Extra Packages for Enterprise Linux 7 - $basearch
                    #baseurl=http://download.fedoraproject.org/pub/epel/7/$basearch
                    metalink=https://mirrors.fedoraproject.org/metalink?repo=epel-7&arch=$basearch
                    failovermethod=priority
                    enabled=0
                    gpgcheck=0
                    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7 EOF''')
                    self.ComponentSupport(name)