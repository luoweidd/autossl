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

from flask import Flask,request,redirect,render_template,current_app,Response,url_for
from base.msgdict import msg
from ACME.ssl_cert_apply_v2 import ssl_cert_v2
from base.mylog import loglog
import json
from datetime import timedelta
from nginx_server.nginx_server import nginx_server
from auth.auth_user import user
from ACME.myhelper import hash_256_digest,b64
from base.basemethod import url_extract_doain,getDomain
from auth.user_model import user_modle
from contrllo.user_contrllo import user_contrlor
import requests,time


logs = loglog()
log = logs.logger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AXxhDYONkOI2-FsnBrQ0FLcpGq43uWAclf6Vp3V8_bU'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

messge=msg()
user_obj = user()
session = user_obj.session_main
stime = time.time()
time_struc = int(round(stime * 1000))
user_contrllor_obj = user_contrlor()

@app.before_request
def before_action():
    if request.path.find('.ico') == -1 and request.path.find('.js') ==-1 and request.path.find('.css') == -1:
        if request.path == '/forget_password':
            return render_template('forget_password.html')
        elif request.path != '/login' and request.path != '/':
            #log.info(session['user'])
            log.info(request.url)
            log.info(session.get('user'))
            if 'user' not in session:
                #session['newurl']=request.path
                if request.method == 'GET':
                    return redirect(url_for('login_login', _scheme="http", _external=True)) #生产环境中,如果部署了https站反向代理，需修改"_scheme"值="https"，且在代理配置中需加入——scheme配置
                result = messge.getmsg(10013)
                result.update({"redirectUrl":'/login'})
                return json.dumps(result)
            elif request.cookies.get(session['user']) != session['cookie']:
                session['newurl']=request.path
                if request.method == 'GET':
                    return redirect(url_for('login_login', _scheme="http", _external=True))

def permission(function):
    def _permission(**kwargs):
        if session.get('name') != 'admin':
            result = messge.getmsg(13)
            return json.dumps(result)
        else:
            result = function(**kwargs)
            return result

@app.route('/favicon.ico')
def favicon():
    return current_app.send_static_file("images/favicon.ico")

@app.route('/',methods=['GET'])
@app.route('/login',methods=['POST','GET'])
def login_login():
    if request.method == 'POST':
        try:
            data =json.loads(request.get_data())
            login_rsult = user_obj.login_validation(data)
            if login_rsult == '登录成功':
                b64_hash256_user = b64(hash_256_digest('%s+%s'%(data['user'],data['passwd'])))
                redirectUrl = '/home'
                result = messge.getmsg(0)
                result['msg'] = {'status':200,'result':login_rsult,'redirectUrl':redirectUrl}
                respon = Response(json.dumps(result))
                respon.set_cookie(data['user'],b64_hash256_user)
                session["cookie"] = b64_hash256_user
                return respon
            elif login_rsult == '用户名密码错误。':
                result = messge.getmsg(12)
                result['msg'] = '用户名密码错误。'
                return json.dumps(result)
            else:
                result = messge.getmsg(10013)
                result['msg'] = login_rsult
                return json.dumps(result)
        except Exception as e:
            result = messge.getmsg(10013)
            result['msg'] = '%s'%e
            return json.dumps(result)
    return render_template('login.html',time_struc=time_struc)

@app.route('/home')
def sslfrom():
    return render_template('applyform.html',user=session['user'],time_struc=time_struc)


@app.route('/applyssl',methods=['POST','GET'])
def applyssl():
    if request.method =='POST':
        data = request.get_data()
        if data != '' or data != None:
            ssl_Cert = ssl_cert_v2()
            domains = [data.decode('utf-8')]
            order = ssl_Cert.new_order(domains)
            if order != None:
                get_auth = ssl_Cert.get_auth(order)
                get_dns_auth = ssl_Cert.dns_auth_info(get_auth)
                if get_dns_auth != None:
                    result=messge.getmsg(0)
                    result['msg']=get_dns_auth
                    return json.dumps(result)
                elif get_dns_auth == 'System error, please contact the system administrator!':
                    result =messge.getmsg(10012)
                    return json.dumps(messge.msg(result))
                elif get_dns_auth == "该域名请求次数过多，请更换域名申请。":
                    result =messge.getmsg(10017)
                    return json.dumps(messge.msg(result))
                else:
                    remsg = messge.getmsg(10015)
                    return json.dumps(messge.msg(remsg))
        remsg =messge.getmsg(100)
        return json.dumps(remsg)
    else:
        remsg=messge.getmsg(10011)
        return json.dumps(messge.msg(remsg))


@app.route('/account_form_info',methods=['GET'])
def account_form_info():
    return render_template('account_info_form.html',user=session['user'],time_struc=time_struc)


@app.route('/apply_ssl_form',methods=['GET'])
def apply_ssl_form():
    return render_template('apply_ssl.html',time_struc=time_struc)


@app.route('/account_info_api',methods=["GET"])
def account_info_api():
    ssl_accounts = ssl_cert_v2()
    result=ssl_accounts.get_account_info()
    if type(result) != dict:
        remsg=messge.getmsg(10012)
        return json.dumps(messge.msg(remsg))
    else:
        res = messge.getmsg(0)
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
        domains = data[0]
        ssl_v2 = ssl_cert_v2()
        auth_link = data[1]
        challeng_link = data[2]
        txt = data[3]
        if auth_link != None:
            validation_result = ssl_v2.dns_validation(txt,domains,challeng_link,auth_link)
            if validation_result != None or validation_result != 'System error, please contact the system administrator!':
                cert = validation_result
                if type(validation_result) == list:
                    nginx = nginx_server()
                    log.info('%s\n%s\n%s\n'%(cert[0],cert[1],cert[2]))
                    nginx.add_Anti_seal_conf(cert[0],cert[1],cert[2])
                    nginx_conf_ceck = nginx.nginx_conf_check()
                    if nginx_conf_ceck[0] == 0:
                        nginx_status = nginx.restart_nginx_to_effective()
                        if nginx_status[0] == 0:
                            result = messge.getmsg(0)
                            result['msg'] = [cert[0],cert[1],cert[2]]
                            return json.dumps(result)
                        else:
                            remsg = messge.getmsg(10016)
                            return json.dumps(messge.msg(remsg))
                    else:
                        remsg = messge.getmsg(10018)
                        return json.dumps(messge.msg(remsg))
                else:
                    remsg = messge.getmsg(10015)
                    return json.dumps(messge.msg(remsg))
            else:
                result = messge.getmsg(10015)
                result['msg'] =validation_result
                return json.dumps(result)
        else:
            remsg = messge.getmsg(10015)
            return json.dumps(messge.msg(remsg))
    else:
        remsg = messge.getmsg(10011)
        return json.dumps(messge.msg(remsg))


@app.route('/forget_password',methods=["POST","GET"])
def forget_password():
    return render_template('forget_password.html')


@app.route('/get_Anti_seal_site_info',methods=['POST','GET'])
def get_Anti_seal_site_info():
    from DBL._sys_config import sys_config
    sys_dates = sys_config()
    sys_conf_info = sys_dates.get_collection_all()
    result = messge.getmsg(0)
    result['msg'] = sys_conf_info
    return json.dumps(result)


@app.route('/logout',methods=['POST'])
def logout():
    if request.method == 'POST':
        user = request.get_data().decode('utf-8').strip(' ')
        result = user_obj.logout_clear()
        remsg = messge.getmsg(0)
        remsg["msg"] = result
        return json.dumps(remsg)
    else:
        resutl = messge.getmsg(10011)
        return json.dumps(resutl)

@permission
@app.route('/name_list',methods=['POST','GET'])
def server_name_list():
    from DBL._sys_config import sys_config
    sys_obj = sys_config()
    user_name = session.get('user')
    user_modl = user_modle()
    user_all = user_modl.read_user_data()
    for i in user_all:
        if user_name == "admin":
            sys = sys_obj.server_list()
            return render_template('server_list_form.html',res=sys)
        elif user_name == i["name"]:
            channleid = i["channle"]
            sys = sys_obj.bychannle_server_list(channleid)
            return render_template('server_list_form.html',res=sys,time_struc=time_struc)
    resutl = messge.getmsg(10)
    return json.dumps(resutl)


@app.route('/update_name_server',methods=['POST'])
def update_name_server():
    if request.method == 'POST':
        data = request.get_data()
        url = request.host_url
        try:
            data = json.loads(data)
            if data["id"] or data["itemVal"]:
                itemVal = url_extract_doain(data['itemVal'])
                itemVal = getDomain(itemVal)
                if itemVal != None:
                    domain = '*.%s' % (itemVal)
                    try:
                        resp = requests.post('%sapplyssl'%url,domain)
                    except requests.RequestException as e:
                        log.error(e)
                        result = messge.getmsg(10013)
                        result["msg"] = "System error, please contact the system administrator!"
                        return json.dumps(result)
                    except Exception as  e:
                        log.error(e)
                        result = messge.getmsg(10013)
                        result["msg"] = "System error, please contact the system administrator!"
                        return json.dumps(result)
                    if resp.status_code < 200 or resp.status_code >= 300:
                        log.error('Error requst applyssl endpoint:%s' % resp.reason)
                        log.error('Status Code:%s' % resp.status_code)
                        result = messge.getmsg(10013)
                        result["msg"] = "System error, please contact the system administrator!"
                        return json.dumps(result)
                    else:
                        result = messge.getmsg(0)
                        res = json.loads(resp.text)
                        res = res["msg"]
                        res.append(data)
                        result["msg"] = res
                        return json.dumps(result)
                else:
                    log.error('域名输入错误：%s'%itemVal)
                    result =messge.getmsg(10019)
                    return json.dumps(result)
        except Exception as e:
            log.error(e)
            result = messge.getmsg(10017)
            return json.dumps(result)
    result = messge.getmsg(10011)
    return json.dumps(result)


@app.route('/update_name_server_validation',methods=['POST'])
def update_name_server_validation():
    if request.method == 'POST':
        data = request.get_data()
        data = eval(data)
        domains = url_extract_doain(data[0])
        domain = getDomain(domains)
        if domain != None:
            ssl_v2 = ssl_cert_v2()
            auth_link = data[1]
            challeng_link = data[2]
            txt = data[3]
            db_ = data[4]
            if auth_link != None:
                validation_result = ssl_v2.dns_validation(txt, domain, challeng_link, auth_link)
                if validation_result != None:
                    cert = validation_result
                    from contrllo.update_name_server_contrllo import update_name_server_contrllo
                    update_name_server_status = update_name_server_contrllo()
                    kwargs = {'Id':db_["id"],'old_domain':db_["old_itemVal"],"new_domain":db_["itemVal"],"new_pem":cert[1],"new_key":cert[2]}
                    update_status = update_name_server_status.update_contrllor(kwargs)
                    log.info('update_status:  ---> %s',update_status)
                    if update_status == 'ok':
                        result = messge.getmsg(0)
                        result['msg'] = '更换完成'
                        return json.dumps(result)
                    elif update_status == '数据未做任何修改！但执行成功。':
                        result = messge.getmsg(0)
                        result['msg'] = '数据未做任何修改！但执行成功。'
                        return json.dumps(result)
                    elif update_status == '未读取到匹配的配置数据，请联系管理员检查。':
                        result = messge.getmsg(0)
                        result['msg'] = '未读取到匹配的配置数据，请联系管理员检查。'
                        return json.dumps(result)
                    elif update_status == '配置检查不通过，请通知管理员检查配置文件，以及系统。':
                        result = messge.getmsg(0)
                        result['msg'] = '配置检查不通过，请通知管理员检查配置文件，以及系统。'
                        return json.dumps(result)
                    else:
                        remsg = messge.getmsg(10015)
                        return json.dumps(remsg)
                else:
                    result = messge.getmsg(10015)
                    return json.dumps(result)
            else:
                remsg = messge.getmsg(10015)
                return json.dumps(messge.msg(remsg))
        else:
            log.error('域名输入错误：%s' % domain)
            result = messge.getmsg(10019)
            return json.dumps(result)
    result = messge.getmsg(10011)
    return json.dumps(result)

@permission
@app.route('/add_new_user',methods=['POST','GET'])
def add_new_user():
    if request.method == 'GET':
        all_channelid = user_contrllor_obj.get_all_channelId()
        return render_template('add_user.html',sys = all_channelid)
    elif request.method == 'POST':
        data = request.get_data()
        try:
            user_data = json.loads(data)
            add_user = user_contrllor_obj.add_new_user(user_data)
            if add_user == 'ok':
                result = messge.getmsg(0)
                result['msg'] = '用户添加成功。'
                return json.dumps(result)
            else:
                result = messge.getmsg(12)
                result['msg'] = '用户添加失败。'
                return json.dumps(result)
        except Exception as e:
            log.error("程序错误： %s"%e)
    else:
        result = messge.getmsg(10013)
        result['msg'] = '不支持:"%s"请求方法'%request.method
        return result

@permission
@app.route('/delete_old_user',methods=['POST','GET'])
def delete_old_user():
    data = request.get_data()
    user_del = user_contrllor_obj.delete_old_user(data)
    if user_del == 'ok':
        result = messge.getmsg(0)
        result['msg'] = '用户已删除。'
        return json.dumps(result)
    else:
        result = messge.getmsg(12)
        result['msg'] = '用户删除失败。'
        return json.dumps(result)

@app.route('/update_old_user_passwd',methods=['POST','GET'])
def update_old_user_passws():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        update_user = user_contrllor_obj.update_old_user(data)
        if update_user == 'ok':
            result = messge.getmsg(0)
            result['msg'] = '密码修改成功。'
            return json.dumps(result)
        else:
            result = messge.getmsg(12)
            result['msg'] = '密码修改失败。'
        return json.dumps(result)
    elif request.method == 'GET':
        return render_template('update_user_passwd.html')

@permission
@app.route('/get_all_user',methods=['POST','GET'])
def get_all_user():
    user_list = user_contrllor_obj.get_all_user()
    log.info('%s'%user_list)
    return render_template('all_user_info.html',user_list = user_list)