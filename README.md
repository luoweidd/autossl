# autossl

#### 功能介绍
主要量大模块：  
      1.新申请（刷新）SSL证书(证书有效期90天)，同时新建nginx配置文件，默认http代理8090端口；  
      2.根据mongodb中存储域名进行服务中已有域名SSL证书更新，如果没有找到相关配置文件则新建配置（仅做了nginx配置支持），在更新配置是需要autossl_client（[本仓库](https://gitee.com/luowei_lv)中下载:[autossl_client](https://gitee.com/luowei_lv/autossl_client)）的支持。同时需要在渠道配置中添加可用渠道主机IP端口（分布式管理，主服务端可无须部署到业务主机，可主服务一对多管理。渠道信息记录在channal.dat以json格式存储，未做二进制序列化，同时用户管理也是以json格式未未二进制序列化，所以请注意目录文件安全。）方可执行，当客户端主机nginx配置检查不通过不会应用生效。其它细节就不一一赘述了。敬请体验。如有需要解答，请加QQ：3245554或邮件：[jeak_2003_@hotmail.com](mailto:jeak_2003_@hotmail.com).
    
#### 分享目的
代理写得并不好，所以在这里开源的目的有一下几个想法。  
    1.分享acme SSL证书申请借口  
    2.分享给有能力写得更好的猿们（我只是一个运维，背锅的而已。）  
    3.如果对你们有想就尽情的拿去用吧（业务不同所以这套码应该不会通用，可以用的话自己拿去改改用吧！逼近免费）此源码不用遵循任何协议！  
    4.当然有看得起的可以捐赠一下，以后能写些更多不要钱的工具。

#### 软件架构
基于flask web框架开发，请求第三方ACME官方接口申请pem格式SSL证书，但目前仅实现，且将来也只会有DNS验证方式。所以在验证域名所有的方式必须为DNS验证，这样的话就必须有域名管理账户所有权才能够申请到SSL证书。


#### 安装教程

安装方式，你可以直接运行Python run.py,但我不推荐这样做，我推荐的方式是使用uwsgi一类的方式启动你的autossl程序，然后通过其他代理程序反向代理到uwsgi上，这样做会更好一些。
目前登录使用的本地基础验证方式，所以用户名、密码记录在auth包下的auth_user模块下，这里必须说明一下，密码从前端传入的是MD5加密字符串，所以后端直接存储的是MD5加密字符串，
当然为了安全，你的MD5加密前的明文最好不要太简单，因为目前网络上已经有很多MD5——明文数据字典。
这里就不再写Python、uwsgi的安装教程了，可自行百度。


#### 使用说明

包内没有使用虚拟环境部署方式，这里仅提供程序源码包。
项目第三方依赖（其余全部基于Python内建包）：  
    1.可以运行在Python2.7以上，但是在Python3.X以上包内有一项依赖必须下载pydns源码安装到你的Python系统换进中，也就是：“site-packages”目录下。  
	2.flask（当然运行的最基本要求，flask web框架）  
	3.pyopenssl  
	4.pymongo（这里使用的是mongodb，当然你可以重写数据写入模块使用其它数据库）  
	5.pydns （目前在Python3.X以上支持有一些小问题，目前我的运行方式是使用的pydns2.X版本的源码安装到我的Python3.X环境中的。运行起来貌似没有什么问题。本项目venv目录内有，可直接下载，目录内该包名称：dns）  
	6.pyCrypto

#### 效果图
登录效果
![Image text](https://gitee.com/luowei_lv/autossl/raw/master/static/images/img/QQ截图20190920095545.png)
新申请SSL证书（支持输入原有域名刷新证书）
![Image text](https://gitee.com/luowei_lv/autossl/raw/master/static/images/img/QQ截图20190920095624.png)
刷新已存储域名SSL证书（可更换相应域名）
![Image text](https://gitee.com/luowei_lv/autossl/raw/master/static/images/img/QQ截图20190920095851.png)
添加用户
![Image text](https://gitee.com/luowei_lv/autossl/raw/master/static/images/img/QQ截图20190920095915.png)
修改渠道信息
![Image text](https://gitee.com/luowei_lv/autossl/raw/master/static/images/img/QQ截图20190920100014.png)