#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description: 
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019-06-04
 * Time: 上午11:37
'''



from autosslcontrolle.checkcertbotinstalled import certbot
from base.basemethod import get_os_info
# print get_os_info()
ll= certbot()
l=ll.backcmd()
print l