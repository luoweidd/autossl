#!/usr/bin/python2
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description: 
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019-06-04
 * Time: 上午11:37
'''

# from ACME.ssl_cert_apply_v2 import ssl_cert_v2
#
# ssl_cert_obj=ssl_cert_v2()
# print ssl_cert_obj.get_nonce()
# import json
# import hashlib,base64
# from Crypto.Hash.SHA256 import SHA256Hash
# from ACME import myhelper
# bb={"e":"AQAB","kty":"RSA","n":"0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx4cbbfAAtVT86zwu1RK7aPFFxuhDR1L6tSoc_BJECPebWKRXjBZCiFV4n3oknjhMstn64tZ_2W-5JsGY4Hc5n9yBXArwl93lqt7_RN5w6Cf0h4QyQ5v-65YGjQR0_FDW2QvzqY368QQMicAtaSqzs8KJZgnYb9c7d0zgdAZHzu6qMQvRL5hajrn1n91CbOpbISD08qNLyrdkt-bFTWhAI4vMQFh6WeZu0fM4lFd2NcRwr3XPksINHaQ-G_xBniIqbw0Ls1jF44-csFCur-kEgU8awapJzKnqDKgw"}
# bs={"e": "AQAB", "kty": "RSA", "n": "wZ-bb8bpVmtcm12EwKxnETtelJELvlL7ZVmwsBTGy7q_FN7zvTYn5QwI0VTJXi8JTaeChQzw2R9ZR1FLpKrnrg3EEhlKDTptLGZ2D1ErIYghSyYVWk3670vNUBfrFlMta7O5EianoEm5ZCn2Zm-efXkjAyoTTlHruKK910BFrUBv5TPwxiqP5ihSbfYF8OU2-DJw5pfDaLK0v4LpH4d60f9WwymwoBZuxc1dYrSH4SFmwoLkQPGv0MIpU-nYpARYk8xp87Fnxilgfug-JbdkvQ9rXwK00MwM8HFZk3k06xRy_IZVPRhs19WmRtKg9DflfnNBxEJlQBl84sBg7HGvgQ"}
# zy="LoqXcYV8q5ONbJQxbmR7SCTNo3tiAXDfowyjxAjEuX0"
# ll=json.dumps(zy,separators=(',',':')).encode("utf8")
#
# def ascii(ll):
#     json_dumo_arr = []
#     for i in ll:
#         x_2=ord(i)
#         json_dumo_arr.append(x_2)
#     return json_dumo_arr
#
# c_8=ascii(ll)
# print "ascii:",c_8
# hs=SHA256Hash(ll).digest()
# print "hs:",hs
# bs64=myhelper.b64(hs)
# print "bs64:",bs64
#
# zw=[55, 54, 203, 177, 120, 124, 184, 48, 156, 119, 238, 140, 55, 5, 197,
#    225, 111, 251, 158, 133, 151, 21, 144, 31, 30, 76, 89, 177, 17, 130,
#    245, 123]
#
# def ascii_10_to_ascii_16(zw):
#     string = ''
#     for i in zw:
#         ac_16=chr(i)
#         string+=ac_16
#     return string
#
# res= ascii_10_to_ascii_16(zw)
# print "16:",res
# print 'bs64:',myhelper.b64(res)
# import dns.resolver
# try:
#     domain='_acme-challenge.hzqp777.com'
#     cname = dns.resolver.query(domain, 'TXT')
#     for i in cname.response.answer:
#         for j in i.items:
#             j.to_text()
# except dns.resolver.NXDOMAIN as e:
#     print e

# from ACME import myhelper
# csr_file = 'C:\Users\jeak_\Desktop\hzqp777.com\certificate.csr'
# # csr = myhelper.read_csr_file(csr_file)
# # qt = csr.replace('-----BEGIN CERTIFICATE REQUEST-----\n','')
# # qw = qt.replace('\n-----END CERTIFICATE REQUEST-----','')
# # qq = qw.replace("\n",'')
# # # csr_load = myhelper.load_csr_file(csr_file)
# import OpenSSL
# from Crypto.Util.asn1 import DerSequence
# csr = myhelper.read_csr_file(csr_file)
# if csr.startswith('-----BEGIN'):
#     csr_req = OpenSSL.crypto.load_certificate_request(OpenSSL.crypto.FILETYPE_PEM, csr)
# else:
#     csr_req = OpenSSL.crypto.load_pkcs12(csr).get_certificate()
# certificate_key_der = DerSequence()
# certificate_key_der.decode(OpenSSL.crypto.dump_certificate_request(OpenSSL.crypto.FILETYPE_ASN1, csr_req)).encode()
# ll = certificate_key_der.encode()
# print ll
# from base import basemethod
# from ACME import myhelper
# domain_dir = 'haoshunjinrong.com'
# key_name = 'C:\Users\jeak_\Desktop\certificate\haoshunjinrong.com\privte.key'
# import OpenSSL
# from Crypto.Util.asn1 import DerSequence
# key = myhelper.load_private_key(key_name)
# certificate_key_der = DerSequence()
# der_key = certificate_key_der.decode(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, key))
# exported_key = "-----BEGIN PRIVATE KEY-----\n%s-----END PRIVATE KEY-----" % der_key.encode().encode("base64")
# print exported_key
# with open(key_name,'w+')as f:
#     f.write(exported_key)

# import time
# import hashlib
# import base64
# print base64.urlsafe_b64encode(hashlib.sha256(str(time.time())).digest()).decode('utf-8').rstrip("=")

# from DBL._sys_config import sys_config
# sys_obj = sys_config()
#
# sys = sys_obj.get_collection_all()
# server_list = []
# for i in sys:
#     server_list.append(i)
#
# print (server_list)

# import os
# import re
# path = '/etc/nginx/sites-enabled/'
# itmes = os.listdir(path)
# old_domain = 'hzqp777.com'
# domain = 'haoshunjinrong.com'
# for i in itmes:
#     with open('%s%s'%(path,i),'rt')as f:
#         data = f.readlines()
#         for i in data:
#             if re.search('#',i) == None:
#                 if re.search(old_domain,i):
#                     i.replace(old_domain,domain)

# domian = '.haoshunjinrong.com'
# print(domian[1::])

# data =  {'Id': '159',
#          'old_domain': '.cssjl.com',
#          'new_domain': '.abcd.com',
#          'new_pem': '/home/devops/文档/devops/autossl/certificate/m4w2b.cn/certificate.pem',
#          'new_key': '/home/devops/文档/devops/autossl/certificate/m4w2b.cn/privte.key'}
# from contrllo.update_name_server_contrllo import update_name_server_contrllo
# obj =update_name_server_contrllo()
# opt = obj.update_contrllor(data)
# if opt == 'ok':
#     db_update_status = obj.update_DB(data['Id'], data["new_domain"])
#     print(db_update_status)
# print(opt)

# i = '    ssl_certificate   /etc/nginx/cert/certificate_sw41j.cn.pem;'
# print(i.split(' ')[len(i.split(' '))-1].replace(';',''))

# ###++++++++++++++++++++nginx config Resolve into a dictionary object.++++++++++++++++++++++
#
# path = '/etc/nginx/conf.d/ff.conf'
# with open(path,'rt')as f:
#     data = f.readlines()
# import re
# nodes = {}
# node_name = 'server'
# node_conut = 0
# for i in data:
#     i_n = i.replace('\n','')
#     i_ = i_n.strip(' ')
#     if re.match('^%s$'%node_name,i_):
#         node = []
#         node.append(i_)
#         node_conut += 1
#         node_ = '%s_%d'%(node_name,node_conut)
#     elif re.match('{',i_):
#         node.append(i_)
#         continue
#     elif re.match('}',i_):
#         node.append(i_)
#         nodes.update({node_:node})
#         continue
#     else:
#         node.append(i_)
#
# conf = {}
# for j in nodes:
#     server = []
#     for p in nodes[j]:
#         h = p.split(' ')
#         blank_count = h.count('')
#         if blank_count >= 1:
#             for n in range(0,blank_count):
#                 h.remove('')
#         conf_dict = {}
#         if h == [] or h == None :
#             continue
#         elif len(h) > 2 and re.match('^location',h[0]) == None:
#             conf_dict.update({h[0]: h[1::]})
#             server.append(conf_dict)
#         elif len(h) >1 and len(h) <= 2:
#             conf_dict.update({h[0]: h[1]})
#             server.append(conf_dict)
#         elif re.match('^location',h[0]):
#             string =''
#             for e in h:
#                 string += ' %s'%e
#             server.append(string)
#         else:
#             server.append(h[0])
#     conf.update({j:server})
# # print(conf)
#
# ###++++++++++++++++++++nginx config Resolve into a dictionary object.++++++++++++++++++++++
#
# #+++++++++++++++++++++++++++++nginx configtion write config file++++++++++++++++++++++++++++
#
# string_buffer = ''
# for i in conf:
#     for j in conf[i]:
#         if type(j) == dict:
#             for n in j:
#                 tmp = ''
#                 if type(j[n]) == list:
#                     for k in j[n]:
#                         tmp += ' %s'%k
#                     string_buffer += '    %s %s\n'%(n,tmp)
#                 else:
#                     string_buffer += '    %s %s\n'%(n,j[n])
#         else:
#             string_buffer += '%s\n'%j
# print(string_buffer)
# #+++++++++++++++++++++++++++++nginx configtion write config file++++++++++++++++++++++++++++

