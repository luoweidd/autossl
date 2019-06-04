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
import json


app = Flask(__name__)

re=msg()

@app.route('/')
def hello_world():
    return '''你走错了，这里什么也没有！<br>
            你以为这里是此地无银三百两么，别这么向了，此地无银三百两，黄“精”却有五百两！<br/>
            放心吧这就是一个测试服务地址而已…… <br>
            <img class="currentImg" id="currentImg"  onload="alog &amp;&amp; 
            alog('speed.set', 'c_firstPageComplete', +new Date); alog.fire &amp;&amp; alog.fire('mark');" 
            src="https://timgsa.baidu.com/timg?image&amp;quality=80&amp;size=b9999_10000&amp;sec=1559555190391&amp;
            di=12efd2602cc4cc34fab88952e16b30ae&amp;imgtype=0&amp;src=http%3A%2F%2Fimg.mp.itc.cn%2Fupload%2F20170518%2F8e54925342144841a82058a7d825c07a.jpg" 
            width="295" height="210" style="top: 320px; left: 256px; width: 1000px; height: 610px; cursor: pointer;" log-rightclick="p=5.102" title="点击查看源网页">
            '''

@app.route('/applysslfrom')
def sslfrom():
    return render_template('applyform.html')

@app.route('/applyssl',methods=['POST','GET'])
def applyssl():
    if request.method =='POST':
        data = request.get_data()
        result=re.getmsg(0)
        result['msg']=data
        return json.dumps(result)
    else:
        remsg=re.getmsg(10015)
        return json.dumps(re.msg(remsg))

if __name__ == '__main__':
    app.run()
