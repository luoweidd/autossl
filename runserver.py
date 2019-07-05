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

from flask import Flask,request,redirect,render_template,current_app,url_for,Response
from base.msgdict import msg
from ACME.ssl_cert_apply_v2 import ssl_cert_v2
from base.mylog import loglog
import json,datetime
from datetime import timedelta
from servsers.nginx_server import nginx_server
from auth.auth_user import user
from ACME.myhelper import hash_256_digest,b64


logs = loglog()
log = logs.logger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AXxhDYONkOI2-FsnBrQ0FLcpGq43uWAclf6Vp3V8_bU'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

re=msg()
user_obj = user()
session =user_obj.session_cookie

@app.before_request
def before_action():
    if request.path.find('.ico') == -1 and request.path.find('.js') ==-1 and request.path.find('.css') == -1:
        if request.path != '/login':
            if 'user' not in session:
                session['newurl']=request.path
                return redirect(url_for('login_login'))


@app.route('/favicon.ico')
def favicon():
    return current_app.send_static_file("images/favicon.ico")

@app.route('/login',methods=['POST','GET'])
def login_login():
    if request.method == 'POST':
        try:
            data =json.loads(request.get_data())
            login_rsult = user_obj.login_validation(data)
            if login_rsult == '登录成功':
                time = datetime.datetime.now()
                b64_hash256_time = b64(hash_256_digest(str(time)))
                redirectUrl = '%shome'%request.host_url
                result = re.getmsg(0)
                result['msg'] = {'status':200,'result':login_rsult,'redirectUrl':redirectUrl}
                respon = Response(json.dumps(result))
                respon.set_cookie(data['user'],b64_hash256_time)
                return respon
            else:
                result = re.getmsg(10013)
                result['msg'] = login_rsult
                return json.dumps(result)
        except Exception as e:
            result = re.getmsg(10013)
            result['msg'] = '%s'%e
            return json.dumps(result)
    return render_template('login.html')

@app.route('/home')
def sslfrom():
    return render_template('applyform.html',user=session['user'])


@app.route('/applyssl',methods=['POST','GET'])
def applyssl():
    if request.method =='POST':
        data = request.get_data()
        if data != '' or data != None:
            ssl_Cert = ssl_cert_v2()
            domains = [data.decode('utf-8')]
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
        remsg =re.getmsg(100)
        return json.dumps(remsg)
    else:
        remsg=re.getmsg(10011)
        return json.dumps(re.msg(remsg))


@app.route('/account_form_info',methods=['GET'])
def account_form_info():
    return render_template('account_info_form.html',user=session['user'])


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


@app.route('/new_site_dns_validation',methods=["POST"])
def new_site_dns_validation():
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
            if validation_result or validation_result != None:
                cert = ssl_v2.get_cert()
                nginx = nginx_server()
                nginx.add_Anti_seal_conf(cert[0],cert[1],cert[2])
                nginx_status = nginx.restart_nginx_to_effective()
                if nginx_status == None:
                    result = re.getmsg(0)
                    result['msg'] = cert
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
        remsg = re.getmsg(10011)
        return json.dumps(re.msg(remsg))


@app.route('/forget_password',methods=["POST","GET"])
def forget_password():
    return render_template('forget_password.html',user=session['user'])


@app.route('/get_Anti_seal_site_info',methods=['POST','GET'])
def get_Anti_seal_site_info():
    from DBL._sys_config import sys_config
    sys_dates = sys_config()
    sys_conf_info = sys_dates.get_collection_all()
    result = re.getmsg(0)
    result['msg'] = sys_conf_info
    return json.dumps(result)


@app.route('/logout',methods=['POST'])
def logout():
    if request.method == 'POST':
        user = request.get_data().decode('utf-8').strip(' ')
        result = user_obj.logout_clear(user)
        remsg = re.getmsg(0)
        remsg["msg"] = result
        return json.dumps(remsg)
    else:
        resutl = re.getmsg(10011)
        return json.dumps(resutl)


@app.route('/name_list',methods=['POST','GET'])
def server_name_list():
    from DBL._sys_config import sys_config
    sys_obj = sys_config()
    sys = sys_obj.server_list()
    return render_template('server_list_form.html',res=sys)


@app.route('/update_name_server',methods=['POST'])
def update_name_server():
    if request.method == 'POST':
        data = request.get_data()
        url = request.host_url
        try:
            data = json.loads(data)
            if data["id"] or data["itemVal"]:
                domain = '*%s'%(data["itemVal"])
                import requests
                try:
                    resp = requests.post('%sapplyssl'%url,domain)
                except requests.RequestException as e:
                    log.error(e)
                    result = re.getmsg(10013)
                    result["msg"] = "System error, please contact the system administrator!"
                    return json.dumps(result)
                except Exception as  e:
                    log.error(e)
                    result = re.getmsg(10013)
                    result["msg"] = "System error, please contact the system administrator!"
                    return json.dumps(result)
                if resp.status_code < 200 or resp.status_code >= 300:
                    log.error('Error requst applyssl endpoint:%s' % resp.reason)
                    log.error('Status Code:%s' % resp.status_code)
                    result = re.getmsg(10013)
                    result["msg"] = "System error, please contact the system administrator!"
                    return json.dumps(result)
                else:
                    result = re.getmsg(0)
                    res = json.loads(resp.text)
                    res = res["msg"]
                    res.append(data)
                    result["msg"] = res
                    return json.dumps(result)
        except Exception as e:
            log.error(e)
            result = re.getmsg(100)
            return json.dumps(result)
    result = re.getmsg(10011)
    return json.dumps(result)


@app.route('/update_name_server_validation',methods=['POST'])
def update_name_server_validation():
    if request.method == 'POST':
        data = request.get_data()
        data = eval(data)
        domains = [data[0]]
        ssl_v2 = ssl_cert_v2()
        auth_link = data[1]
        challeng_link = data[2]
        txt = data[3]
        db_ = data[4]
        if auth_link != None:
            validation_result = ssl_v2.dns_validation(txt, domains, challeng_link, auth_link)
            if validation_result or validation_result != None:
                cert = validation_result
                from contrllo.update_name_server_contrllo import update_name_server_contrllo
                update_name_server_status = update_name_server_contrllo()
                kwargs = {'Id':db_["id"],'old_domain':db_["old_itemVal"],"new_domain":db_["itemVal"],"new_pem":cert[1],"new_key":cert[2]}
                update_status = update_name_server_status.update_contrllor(kwargs)
                if update_status == None and update_status == 'ok' :
                    result = re.getmsg(0)
                    result['msg'] = '更换完成'
                    return json.dumps(result)
                elif update_status == '数据未做任何修改！但执行成功。':
                    result = re.getmsg(0)
                    result['msg'] = '数据未做任何修改！但执行成功。'
                    return json.dumps(result)
                else:
                    remsg = re.getmsg(10015)
                    return json.dumps(re.msg(remsg))
            else:
                result = re.getmsg(10015)
                result['msg'] = validation_result
                return json.dumps(result)
        else:
            remsg = re.getmsg(10015)
            return json.dumps(re.msg(remsg))
    result = re.getmsg(10011)
    return json.dumps(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
