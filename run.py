#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description:  
 * Project : autossl
 * Ide tools : PyCharm
 * File name : run.py
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019/7/9
 * Time: 上午9:00
'''

from autossl_view import app

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)