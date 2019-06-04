#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description: 
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019-06-04
 * Time: 上午9:13
'''


class msg:
    _msgdict = [
        {'code':0,'msgtype':'success','msg':None},
        {'code': 10010, 'msgtype': 'error', 'msg': 'Data type error, please pass in the correct data type according to the interface requirements'},
        {'code': 10011, 'msgtype': 'error', 'msg': 'Must POST method ,not support GET method'},
        {'code': 10012, 'msgtype': 'error', 'msg': 'Unknown error, please contact the administrator'}
    ]

    def getmsg(self,code):
        for i in self._msgdict:
            if code == i['code']:
                return i
        else:
            return {'code': -1, 'msgtype': 'error', 'msg': 'The error message is undefined, please contact the administrator'}

    def msg(self,result):
        if type(result) == dict:
            msg = {"msg": result['msg'], "msgcode": result['code'], "msgtype": result['msgtype']}
            return msg
        else:
            assert 'data type error, must dict type date.'