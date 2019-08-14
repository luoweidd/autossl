#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description:  
 * Project : autossl
 * Ide tools : PyCharm
 * File name : nginxextension.py
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019/8/12
 * Time: 上午9:37
'''

import socket
from base.mylog import loglog

class socketclient:

    def __init__(self):
        self.log = loglog.logger
        self.client_addr = ('127.0.0.1',8782)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.client_addr)
        self.client.settimeout(15)

    def recv(self):
        while True:
            try:
                data = self.client.recv(10240)
                if data != b'':
                    self.log.error('\n接收到新消息：“%s”'%data.decode('utf-8'))
                    return data
                else:
                    self.client.close()
                    self.log.error('\n服务连接断开！')
                    return '服务连接断开'
            except OSError as e:
                self.client.close()
                break
                if e is object:
                    for i in e:
                        self.log.error(i)
                else:
                    self.log.error(e)

    def send(self):
        while True:
            msg = input('请输入：')
            if msg != None and msg != b'':
                if msg != 'close':
                    try:
                        msg = Message_Encapsulation(msg)
                        self.client.sendall(msg)
                    except OSError as e:
                        self.client.close()
                        break
                        if e is object:
                            for i in e:
                                self.log.error(i)
                        else:
                            self.log.error(e)


    def heartbeat(self):
        while True:
            import time
            time.sleep(10)
            try:
                msg = '{"heard":"heartbeat","msg":{"check":"On-line"}}'
                #msg = b'{"heard":"nginx_ssl","msg":{"domain":"*.1a27d.cn","old_domain":"*.g8d6c.cn","ca_key":"-----BEGIN CERTIFICATE----- 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-----END CERTIFICATE----- -----BEGIN CERTIFICATE-----MIIEkjCCA3qgAwIBAgIQCgFBQgAAAVOFc2oLheynCDANBgkqhkiG9w0BAQsFADA/MSQwIgYDVQQKExtEaWdpdGFsIFNpZ25hdHVyZSBUcnVzdCBDby4xFzAVBgNVBAMTDkRTVCBSb290IENBIFgzMB4XDTE2MDMxNzE2NDA0NloXDTIxMDMxNzE2NDA0NlowSjELMAkGA1UEBhMCVVMxFjAUBgNVBAoTDUxldCdzIEVuY3J5cHQxIzAhBgNVBAMTGkxldCdzIEVuY3J5cHQgQXV0aG9yaXR5IFgzMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnNMM8FrlLke3cl03g7NoYzDq1zUmGSXhvb418XCSL7e4S0EFq6meNQhY7LEqxGiHC6PjdeTm86dicbp5gWAf15Gan/PQeGdxyGkOlZHP/uaZ6WA8SMx+yk13EiSdRxta67nsHjcAHJyse6cF6s5K671B5TaYucv9bTyWaN8jKkKQDIZ0Z8h/pZq4UmEUEz9l6YKHy9v6Dlb2honzhT+Xhq+w3Brvaw2VFn3EK6BlspkENnWAa6xK8xuQSXgvopZPKiAlKQTGdMDQMc2PMTiVFrqoM7hD8bEfwzB/onkxEz0tNvjj/PIzark5McWvxI0NHWQWM6r6hCm21AvA2H3DkwIDAQABo4IBfTCCAXkwEgYDVR0TAQH/BAgwBgEB/wIBADAOBgNVHQ8BAf8EBAMCAYYwfwYIKwYBBQUHAQEEczBxMDIGCCsGAQUFBzABhiZodHRwOi8vaXNyZy50cnVzdGlkLm9jc3AuaWRlbnRydXN0LmNvbTA7BggrBgEFBQcwAoYvaHR0cDovL2FwcHMuaWRlbnRydXN0LmNvbS9yb290cy9kc3Ryb290Y2F4My5wN2MwHwYDVR0jBBgwFoAUxKexpHsscfrb4UuQdf/EFWCFiRAwVAYDVR0gBE0wSzAIBgZngQwBAgEwPwYLKwYBBAGC3xMBAQEwMDAuBggrBgEFBQcCARYiaHR0cDovL2Nwcy5yb290LXgxLmxldHNlbmNyeXB0Lm9yZzA8BgNVHR8ENTAzMDGgL6AthitodHRwOi8vY3JsLmlkZW50cnVzdC5jb20vRFNUUk9PVENBWDNDUkwuY3JsMB0GA1UdDgQWBBSoSmpjBH3duubRObemRWXv86jsoTANBgkqhkiG9w0BAQsFAAOCAQEA3TPXEfNjWDjdGBX7CVW+dla5cEilaUcne8IkCJLxWh9KEik3JHRRHGJouM2VcGfl96S8TihRzZvoroed6ti6WqEBmtzw3Wodatg+VyOeph4EYpr/1wXKtx8/wApIvJSwtmVi4MFU5aMqrSDE6ea73Mj2tcMyo5jMd6jmeWUHK8so/joWUoHOUgwuX4Po1QYz+3dszkDqMp4fklxBwXRsW10KXzPMTZ+sOPAveyxindmjkW8lGy+QsRlGPfZ+G6Z6h7mjem0Y+iWlkYcV4PIWL1iwBi8saCbGS5jN2p8M+X+Q7UNKEkROb3N6KOqkqm57TH2H3eDJAkSnh6/DNFu0Qg== -----END CERTIFICATE-----","privte_key":"-----BEGIN RSA PRIVATE KEY-----  MIIJKAIBAAKCAgEAzq74PFBwZ4N4b3cTw7YxEx6+9ogNtdmLoAx2W2pQZResCnLmhSpnHW8ImTEJ3CPxgZNIUs8y0eNzlFix9V93VtRs8G6T6G8QgXFjBgD7CkfvRx8skBIpjagz8hSIOtyBQh/3R5ZolVm+DRQGlVTzGd6bfUYEWbEoPArhi5ntswJJDBNt+MuMCV7bsbGsVrE1xHoyBYjXKLVA5rhFFFsk0SHTNqeCqz3kNhq9jm6GXm/wDXmE8/v3jgyhhCZE2yPu6VjVQiVBJwSUneFidhWcC0IBnA/D+EDEtCa98uSEd/v+tvDvyR7bUa0svbSIVU67czxQ2EKCf0iQfr+h3MGD+spPs2apQ7xA9+VQ4DykRsmuAMQv4l5xbAvG+KDpcARCO2Np3KyJEAr/zwVgOEfydm8a1kXkntXDY/ZXuF/kujuSiyIqPLlWjMVYO9q4BPTwQvVZvz6B4FGVbpftIfMxZc89pWyKapxjX/fghflXQA76+1j7EHp5LZaJUBuCX84rHsBiKoX5mWrn/qvGH/puozO/5MZYtVPZBfNeTKt79bZjxQMuYdHl60E2nnEx+Bzj9BbwqLEAYKUzcnGgQgqbo1MvEibVSe/1q6OgqDXrC4IvTv2MQkHCmzY18EGW06Kz3YnVVyP118Oz1OD48fVK7kWsmhcOkxKJpt1TFCa3p2UCAwEAAQKCAgA96P1km7e/2grGYMXj1vxGPOx4znJE6aBAVdtSMLtaPMgE7TwN4ZC3qV3K/Xx1m7Ko3KRKYdRYOKiTZCoSVQFbWhAzyPu3ISWxkHRYBQ0tnDSZekYP9dDKpPrCZdIUx55UX1zj7bLwIcyjAD+klaioNB0hXkrJTx69NYkwFvCzsViOLHfBkb8lw2tNg+oaocR4UR4QuFey0vBY7BONMGwL1PT+pximEMj+R+5F7ueC/EbM0ny31N7nhvMOsaPofJABB+IBiUVF2cJmtG+Y7YoreR8gTzylbUk+qWg2jKr9gddflzZMaVjK03PWc3BvFUFjGEsjLHEIjYTy4pYqmTDd8WxOTIjLlt6+EKZ2RUS6XPmjfIrbFBbShj0+DlWv9+FUZtWFn6uupUZ1jDm83m1dQ7cGsRdFfV6wQavwIm6Pqa2hyPEWwrzu3WvPpxXZFixL0MYIW01P34v8QA+jajZ3dAXzolDSb7A5TT7A8kSiSh8h/IQJOQ1lr+hmYSAPxI4vfiPVDaRr6rBdCyPvweRuFp7s9yJC8AOlrzzMGulZL+vg1+z8q1JWf91OQyAhi5xYkqsGoSwTzwcqRN3p+7HHSJUpdlC1doF/Uvj1DalzAXzIFm3/9dOjBr29fOd8Zaab/tLlusGgmAS8D0i/iHjXu8T/k/+yaRmY3lBQ8/KftQKCAQEA1Q7QUlwBitBBPM7mNmpnaAYaRHt+pYHHhVM3deNK2RC4rrkCMe8A2oh3ulddBbQD5GHc2B+lukADQlRZIXs9BK9KrVy7MB2pChQHus/mwvWW8GudJHwvzOi9px053gED2tQTTMjorq97izWrUF5cVijchCN/oiJEvLnMSEPGb+McqVVsbQLUwAeA34e04wA9RPU32gYERnJi94oBqzQ3EpVCT+P3PaizWApR+o6Z2TKPQt9sIoKYrMbb4si4ZMHkmWHm/SprHF5amWV2OOqtEMnrQX+SgGaEtlhkYir7Igeweylb07rY5WTVT1MnInk1JW5JKB6JSkVZx3B8wzsGKwKCAQEA+FdBWhSv1G4vOftVYJJEPcf5Z8VLi70aM+iA0XbqlTxUoZmzTWzX7H9I9zFfVPDs0pKNKgl7FnoptM5dUm7wWMNp5E0wvR1hDAtLIS2b61v+fLJx1y4w+6iqDfxDtTzhQCxI0cEN6abJX0Yjm980kFZWcOy4l3erw8IASnS4DsyoEQioiQP/RT903xnNOWmgJTW+g535W98ivnQ0kzc/PiQtZCzzKYp1z9nKBpaUZjnSfJH02AFIZJH4vX+yuxjIl8J5h9F/417nt8xFhy+lOmgYM16xm/2Y/eflytScJiGwgDsRqA3iMl0veteVa1z+ex0i5msmL/ct7sLLftNQrwKCAQAZRd6URnGwY6+5ZNmODuUhQ8gN45BMVa6zNAHaLBIO2ZrurueBwNYbFiENq5tPN+FWT/2AbZCdHUbFsXe5LwM38QsssVlLBdmtZl7cXBkFe1hiQIGteEW7SshkcGUS3o/0fz+i1hozzoEbLEycBfVyCvrNeeCD/QimUmvXDqMVVp1pwMZR0AoolTtGSLS+UKLz8Rqk9B3BtYPj1S0Jf/IgdDAfhe0oFUDg6qh6zjuVthekWRhcp50wsY4XwrOM0Csrvp9F3KhD/zVECPMTIVNSMIGFjXp1XLPVZXrS4kJT8RGQKoHIBdwAqgtbk4OK5VHWlNR8u9KRStSxgbhq+C9tAoIBAQDqHaAPYwcrtcAx4h3nz5wjvh0CVf3VO62zF9IxJfEaRWjne7WMHTslyg0odFQSCJrKHLyVz6BJXVtqB031A37zvy1Zu+dhsYumxhLKsWuXIv+z4KnvmK024heG3bWa60zSqazwiRYrmj+m4MF7FZ5BIBOXm6KdsISuJHsPth86XHdor4fqu2jwiFUOag2NvWTrD1KOU+QbVy0y7OwPiPrHA2YDVVjbZZuRGhkZwuUdxg8HvrVa2UK9BNvBEdyWA1Q/tWfKwZbV68d4/0rgmesjN7Tw4KmBjD6pxu9cGrkmPYZeLNGFY6lFn5G+NfS35VBHEf2vyX2TpGuZ9evPoTkjAoIBABvJh4XBDoPc9rt8nzcGV6eqMdJayR2TF5DRo2HZdJ9pvd/SuOoUdSSDoOW39oWsHXFbakvnZzQ1BbX2iQH2hHgAK3FbZ07Fnk8CJdlOQbSNQhbc4BKrth4bt6HXrtH76iJgtgYsZ/oc1+0gHc3H2QRFNiXs3rIOCGF/SpuHZZlSihoWzjNfqi/g24Pi1+rH0wXMWn+SVuSBfPTHM864jZHC4zacGpK2fUsH1tFHbedoTi/g9pgH9El2zyXDxR2rgm4JnmKsjHr4pgnbyqZDoSFxon9doqwq9BdCp9rQODibmMLkO83m9F9gLyHqOiTV506TleH6rD4t8315P5tJUD4= -----END RSA PRIVATE KEY-----"}}'
                msg = Message_Encapsulation(msg)
                self.client.sendall(msg)
            except Exception as e:
                self.client.close()
                break
                if e is object:
                    for i in e:
                        self.log.error(i)
                else:
                    self.log.error(e)

    def data_send(self,data):
        msg = data
        if msg != None and msg != b'':
            if msg != 'close':
                try:
                    msg = self.Message_Encapsulation(msg)
                    self.client.sendall(msg)
                    return True
                except OSError as e:
                    if e is object:
                        for i in e:
                            self.log.error(i)
                    else:
                        self.log.error(e)


    def Message_Encapsulation(self,msg):
        '''
        Message Encapsulation
        :param msg: <type>:str
        :return: <type>:byte  explear: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1b\xdb{"heard":"nginx_ssl","msg":{"domain":"*.1a27d.cn","old_domain":"*.g8d6c.cn"}}'
        '''
        return len(msg).to_bytes(20,'big')+msg.encode('utf-8')