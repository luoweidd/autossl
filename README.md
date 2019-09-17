# autossl

#### 介绍
{**以下是码云平台说明，您可以替换此简介**
码云是 OSCHINA 推出的基于 Git 的代码托管平台（同时支持 SVN）。专为开发者提供稳定、高效、安全的云端软件开发协作平台
无论是个人、团队、或是企业，都能够用码云实现代码托管、项目管理、协作开发。企业项目请看 [https://gitee.com/enterprises](https://gitee.com/enterprises)}

#### 软件架构
给予flask web框架开发，请求第三方ACME官方接口申请pem格式SSL证书，但目前仅实现，且将来也只会有DNS验证方式。所以在验证域名所有的方式必须为DNS验证，这样的话就必须有域名管理账户所有权才能够申请到SSL证书。


#### 安装教程

安装方式，你可以直接运行Python run.py,但我不推荐这样做，我推荐的方式是使用uwsgi一类的方式启动你的autossl程序，然后通过其他代理程序反向代理到uwsgi上，这样做会更好一些。
目前登录使用的本地基础验证方式，所以用户名、密码记录在auth包下的auth_user模块下，这里必须说明一下，密码从前端传入的是MD5加密字符串，所以后端直接存储的是MD5加密字符串，
当然为了安全，你的MD5加密前的明文最好不要太简单，因为目前网络上已经有很多MD5——明文数据字典。
###***注意:
    如有使用nginx或其它代理工具置于此服务前端，且同时使用了SSL安全链接
    （https，特别是http强转https，在同时开启http和https会出现验证证书结束时报错，此处报错会出现借口被重复执行，返回错误结果。），
    记得对证书目录做静态处理配置，否者客户端程序无法下载到证书文件，导致配置出错。

#### 使用说明

包内没有使用虚拟环境部署方式，这里仅提供程序源码包。
项目第三方依赖（其余全部基于Python内建包）：
	可以运行在Python2.7以上，但是在Python3.X以上包内有一项依赖必须下载pydns源码安装到你的Python系统换进中，也就是：“site-packages”目录下。
	flask（当然运行的最基本要求，flask web框架）
	pyopenssl
	pymongo（这里使用的是mongodb，当然你可以重写数据写入模块使用其它数据库）
	pydns （目前在Python3.X以上支持有一些小问题，目前我的运行方式是使用的pydns2.X版本的源码安装到我的Python3.X环境中的。运行起来貌似没有什么问题。）
	pyCrypto

#### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request


#### 码云特技

1. 使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2. 码云官方博客 [blog.gitee.com](https://blog.gitee.com)
3. 你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解码云上的优秀开源项目
4. [GVP](https://gitee.com/gvp) 全称是码云最有价值开源项目，是码云综合评定出的优秀开源项目
5. 码云官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6. 码云封面人物是一档用来展示码云会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
