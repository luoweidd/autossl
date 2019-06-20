#!/usr/bin/python2
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description: 
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019-06-03
 * Time: 下午2:01
'''

from flask import Flask,request,redirect,render_template
from base.msgdict import msg
from ACME.ssl_cert_apply_v2 import ssl_cert_v2
from base.mylog import loglog
import json

logs = loglog()
log = logs.logger

app = Flask(__name__)

re=msg()

@app.route('/index')
@app.route('/login')
@app.route('/')
def hello_world():
    return render_template('login.html')

@app.route('/home')
def sslfrom():
    return render_template('applyform.html')

@app.route('/applyssl',methods=['POST','GET'])
def applyssl():
    if request.method =='POST':
        data = request.get_data()
        ssl_Cert = ssl_cert_v2()
        domains = [data]
        order = ssl_Cert.new_order(domains)
        get_auth = ssl_Cert.get_auth(order)
        get_dns_auth = ssl_Cert.dns_auth_info(get_auth)
        if get_dns_auth != None:
            result=re.getmsg(0)
            result['msg']=get_dns_auth
            return json.dumps(result)
        else:
            remsg = re.getmsg(10015)
            return json.dumps(re.msg(remsg))
    else:
        remsg=re.getmsg(10015)
        return json.dumps(re.msg(remsg))

@app.route('/account_form_info',methods=['GET'])
def account_form_info():
    return render_template('account_info_form.html')

@app.route('/apply_ssl_form',methods=['GET'])
def apply_ssl_form():
    return render_template('apply_ssl.html')

@app.route('/account_info_api',methods=["GET"])
def account_info_api():
    ssl_accounts = ssl_cert_v2()
    result=ssl_accounts.get_account_info()
    if type(result) != dict:
        remsg=re.getmsg(10012)
        return json.dumps(re.msg(remsg))
    else:
        res = re.getmsg(0)
        res['msg']=result
        return json.dumps(res)

@app.route('/account_order',methods=["GET"])
def account_order():
    ssl_cert_obj = ssl_cert_v2()
    account_orders = ssl_cert_obj.old_order()
    return account_orders

@app.route('/dns_validation',methods=["POST"])
def dns_validation():
    if request.method =='POST':
        data = request.get_data()
        data = eval(data)
        domains = [data[0]]
        ssl_v2 = ssl_cert_v2()
        auth_link = data[1]
        challeng_link = data[2]
        txt = data[3]
        if auth_link != None:
            validation_result = ssl_v2.dns_validation(txt,domains,challeng_link,auth_link)
            if validation_result is True:
                cert = ssl_v2.get_cert()
                '''
                补齐nginx配置文件修改，并重启nginx服务，使配置生效。需做判断如出现配置错误回滚配置，并返回提示！
                '''
                nginx_status = ''
                if nginx_status != None:
                    result = re.getmsg(0)
                    result['msg'] = nginx_status
                    return json.dumps(result)
                else:
                    remsg = re.getmsg(10015)
                    return json.dumps(re.msg(remsg))
            else:
                result = re.getmsg(10015)
                result['msg'] =validation_result
                return json.dumps(result)
        else:
            remsg = re.getmsg(10015)
            return json.dumps(re.msg(remsg))
    else:
        remsg = re.getmsg(10015)
        return json.dumps(re.msg(remsg))

@app.route('/forget_password',methods=["POST","GET"])
def forget_password():
    return render_template('forget_password.html')



if __name__ == '__main__':
    app.run()
