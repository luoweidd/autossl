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

from DBL._sys_config import sys_config
sys_obj = sys_config()

sys = sys_obj.get_collection_all()
server_list = []
for i in sys:
    server_list.append(i)

print server_list