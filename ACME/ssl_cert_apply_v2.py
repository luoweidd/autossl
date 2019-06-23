#!/usr/bin/python3
# _*_coding:utf8_*_

'''
 * Created with IntelliJ Pycharm.
 * Description: ssl_cert_v2
 * Author <a href="mailto:3245554@qq.com">罗卫</a>
 * User: devops
 * Date: 2019-06-11
 * Time: 上午9:49
 * Thank: John Hanley (myhelper,help,myutils)
'''

import requests
import json
import myhelper
import os,time
from base.mylog import loglog
from base import basemethod


class ssl_cert_v2:

    logs = loglog()
    log = logs.logger
    base_path_test = 'https://acme-staging-v02.api.letsencrypt.org/directory'
    base_path = 'https://acme-v02.api.letsencrypt.org/directory'

    #request headers
    headers = {
        'User-Agent': 'lw-ghy-acme-client/1.0',
        'Accept-Language': 'zh',
        'Content-Type':"application/jose+json"
    }

    #new resources path
    nonec_path="newNonce"
    nonec="Replay-Nonce"
    account_path="newAccount"
    order_path="newOrder"
    account_order = 'orders?cursor=2>,rel="next"'
    # old_order = 'orders?cursor=2>,rel="next"'
    Authz_path="newAuthz"
    revokeCert="revokeCert"
    keyChange="keyChange"

    AccountKeyFile = '%s%scertificate%saccount.key'%(basemethod.get_root_path(),basemethod.systemc_dir_flag(),basemethod.systemc_dir_flag())
    EmailAddresses = ['mailto:654622452@qq.com','mailto:69672452@qq.com']

    def get_directory(self):
        try:
            directorys = requests.get(self.base_path, headers=self.headers)
        except requests.exceptions.RequestException as error:
            self.log.error(error)

        if directorys.status_code < 200 or directorys.status_code >= 300:
            self.log.error('Error calling ACME endpoint:', directorys.reason)
        else:
            result = directorys.json()
            return result

    def get_nonce(self,path):
        nonce = requests.head(path).headers[self.nonec]
        return nonce

    def check_account_key_file(self):
        """ Verify that the Account Key File exists and prompt to create if it does not exist """
        if os.path.exists(self.AccountKeyFile) is False:
            myhelper.create_rsa_private_key(self.AccountKeyFile)

    def data_packaging(self,payload,body_top):
        payload_b64 = myhelper.b64(json.dumps(payload).encode("utf8"))
        body_top_b64 = myhelper.b64(json.dumps(body_top).encode("utf8"))
        # Create the message digest (signature)
        data = "{0}.{1}".format(body_top_b64, payload_b64).encode("utf8")
        signature = myhelper.sign(data, self.AccountKeyFile)
        if signature == None:
            self.new_account()
            signature = myhelper.sign(data,self.AccountKeyFile)
        # Create the HTML request body
        jose = {"protected": body_top_b64,"payload": payload_b64,"signature": myhelper.b64(signature)}
        return jose

    def new_account(self):
        self.check_account_key_file()
        new_accuount = self.get_directory()
        accuount_url = new_accuount[self.account_path]
        nonce = self.get_nonce(new_accuount[self.nonec_path])
        # Get the URL for the terms of service
        terms_service = new_accuount.get("meta", {}).get("termsOfService", "")
        self.log.info('Terms of Service:%s'%terms_service)
        # Create the account request
        if terms_service != "":
            payload = {"termsOfServiceAgreed": True,"contact": [self.EmailAddresses]}
            self.log.info(payload)
        body_top = {"alg": "RS256","jwk": myhelper.get_jwk(self.AccountKeyFile),"url": accuount_url,"nonce": nonce}
        jose = self.data_packaging(payload,body_top)
        try:
            self.log.info('Calling endpoint:%s'%accuount_url)
            resp = requests.post(accuount_url, json=jose, headers=self.headers)
        except requests.exceptions.RequestException as error:
            resp = error.response
            self.log.error(resp)
        except Exception as ex:
            self.log.error(ex)
        except BaseException as ex:
            self.log.error(ex)
        if resp.status_code < 200 or resp.status_code >= 300:
            self.log.info('Error calling ACME endpoint:%s'%resp.reason)
            self.log.error('Status Code:%s'%resp.status_code)
            myhelper.process_error_message(resp.text)
        if 'Location' in resp.headers:
            self.log.info('Account URL:%s'%resp.headers['Location'])
        else:
            self.log.error('Error: Response headers did not contain the header "Location"')
            return "System error, please contact the system administrator!"

    def get_account_url(self):
        dir_noce=self.get_directory()
        # Create the account request
        payload = {"termsOfServiceAgreed": True, "contact": self.EmailAddresses}
        nonce=self.get_nonce(dir_noce[self.nonec_path])
        self.check_account_key_file()
        jwk = myhelper.get_jwk(self.AccountKeyFile)
        body_top = {"alg": "RS256","jwk":jwk ,"url": dir_noce[self.account_path],"nonce": nonce}
        jose = self.data_packaging(payload,body_top)
        # Make the ACME request
        try:
            resp = requests.post(dir_noce[self.account_path], json=jose, headers=self.headers)
        except requests.exceptions.RequestException as error:
            resp = error.response
            self.log.error(resp)
        except Exception as error:
            self.log.error(error)

        if resp.status_code < 200 or resp.status_code >= 300:
            print resp.reason
            self.log.error('Error calling ACME endpoint:%s'%resp.reason)
            self.log.error('Status Code:%s'%resp.status_code)
        else:
            if 'Location' in resp.headers:
                print
                self.log.info('Account URL:%s'%resp.headers['Location'])
                nonce = resp.headers[self.nonec]
                account_url = resp.headers['Location']
                return nonce, account_url
            else:
                self.log.info('INFO: Response headers did not contain the header "Location",Start new accounts.')
                self.new_account()
                self.get_account_url()
                self.log.info('INFO: The new account is created and returned to the account URL.')
                return "System error, please contact the system administrator!"

    def get_account_info(self):
        self.check_account_key_file()
        """ Get the Account Information """
        accounts=self.get_account_url()
        # Create the account request
        if accounts != None:
            payload = {}
            body_top = {"alg": "RS256","kid": accounts[1],"nonce": accounts[0],"url": accounts[1]}
            jose = self.data_packaging(payload,body_top)
            try:
                resp = requests.post(accounts[1], json=jose, headers=self.headers)
            except requests.exceptions.RequestException as error:
                resp = error.response
                self.log.error(resp)
            except Exception as error:
                self.log.error(error)

            if resp.status_code < 200 or resp.status_code >= 300:
                self.log.error('Error calling ACME endpoint:%s'%resp.reason)
                self.log.error('Status Code:%s'%resp.status_code)
                return "System error, please contact the system administrator!"
            else:
                info = json.loads(resp.text)
                info["url"]=resp.url
                nonce = resp.headers[self.nonec]
                info["nonce"] = nonce
                return info
        else:
            return "System error, please contact the system administrator!"

    def account_deactivate(self):
        """ Call ACME API to Deactivate Account """
        accounts=self.get_account_url()
        # Create the account request
        payload = {'status': 'deactivated'}
        body_top = {"alg": "RS256","kid": accounts[1],"nonce": accounts[0],"url": accounts[1]}
        jose = self.data_packaging(payload,body_top)
        host = accounts[1].split("//")[-1].split("/")[0].split('?')[0]
        self.headers['Host'] = host
        # Make the ACME request
        try:
            print('Calling endpoint:', accounts[1])
            resp = requests.post(accounts[1], json=jose, headers=self.headers)
        except requests.exceptions.RequestException as error:
            resp = error.response
            self.log.error(resp)
        except Exception as error:
            self.log.error(error)

        if resp.status_code < 200 or resp.status_code >= 300:
            self.log.error('Error calling ACME endpoint:', resp.reason)
            self.log.error('Status Code:%s'%resp.status_code)
            return "System error, please contact the system administrator!"
        else:
            info = json.loads(resp)
            return info

    def account_update(self):
        accounts=self.get_account_url()
        # Create the account request
        payload = {"contact": self.EmailAddresses}
        body_top = {"alg": "RS256","kid": accounts[1],"nonce": accounts[0],"url": accounts[1]}
        host = accounts[1].split("//")[-1].split("/")[0].split('?')[0]
        self.headers['Host'] = host
        jose = self.data_packaging(payload,body_top)
        # Make the ACME request
        try:
            resp = requests.post(accounts[1], json=jose, headers=self.headers)
        except requests.exceptions.RequestException as error:
            resp = error.response
            self.log.error(resp)
        except Exception as error:
            self.log.error(error)
        if resp.status_code < 200 or resp.status_code >= 300:
            self.log.error('Error calling ACME endpoint:%s'%resp.reason)
            self.log.error('Status Code:%s'%resp.status_code)
            return "System error, please contact the system administrator!"
        else:
            info = json.loads(resp)
            return info

    def new_order(self,domain):
        """ Request an SSL certificate from the ACME server """
        if domain != None:
            domain_dir = myhelper.DomainDewildcards(domain[0])
            key_name = '%s%scertificate%s%s%sprivte.key'%(basemethod.get_root_path(),basemethod.systemc_dir_flag(),basemethod.systemc_dir_flag(),domain_dir,basemethod.systemc_dir_flag())
            csr_name = '%s%scertificate%s%s%scertificate.csr'%(basemethod.get_root_path(),basemethod.systemc_dir_flag(),basemethod.systemc_dir_flag(),domain_dir,basemethod.systemc_dir_flag())
            import os
            if os.path.exists(csr_name) is False:
                myhelper.create_domains_csr(key_name,csr_name,domain[0],self.EmailAddresses)
            domains = myhelper.get_domains_from_csr(csr_name)
            # Create the account request
            accounts = self.get_account_url()
            dir = self.get_directory()
            order_url = dir[self.order_path]
            self.log.info("Request to the ACME server an order to validate domains.")
            payload = {"identifiers": [{"type": "dns", "value": domain} for domain in domains]}
            body_top = {"alg": "RS256","kid": accounts[1],"nonce": accounts[0],"url": dir[self.order_path]}
            jose = self.data_packaging(payload,body_top)
            # Make the ACME request
            try:
                resp = requests.post(order_url, json=jose, headers=self.headers)
            except requests.exceptions.RequestException as error:
                resp = error.response
                self.log.error(resp)
            except Exception as error:
                self.log.error(error)
            if resp.status_code < 200 or resp.status_code >= 300:
                self.log.error('Error calling ACME endpoint:%s'%resp.reason)
                self.log.error('Status Code:%s'%resp.status_code)
                return "System error, please contact the system administrator!"
            else:
                # nonce = resp.headers[self.nonec]
                if resp.status_code == 201:
                    order_location = resp.headers['Location']
                    return order_location
            return 'create csr file  error'


    def old_order(self):
        accounts = self.get_account_url()
        self.log.info("Request to the ACME server an order to validate domains.")
        order_url = '%s/%s'%(accounts[1],self.account_order)
        payload = {}
        body_top = {"alg": "RS256", "kid": accounts[1], "nonce": accounts[0], "url": order_url}
        jose = self.data_packaging(payload, body_top)
        self.log.info("Request URL:%s"%order_url)
        try:
            resp = requests.post(order_url,json=jose,headers=self.headers)
        except requests.exceptions.RequestException as error:
            resp = error.response
            self.log.error(resp)
            return error
        except Exception as error:
            self.log.error(error)
            return error
        if resp.status_code < 200 or resp.status_code >= 300:
            self.log.error('Error calling ACME endpoint:%s' % resp.reason)
            self.log.error('Status Code:%s' % resp.status_code)
            return "System error, please contact the system administrator!"
        return resp

    def get_auth(self,order_info):
        if order_info != None:
            try:
                resp = requests.get(order_info, headers=self.headers)
            except requests.exceptions.RequestException as error:
                resp = error.response
                self.log.error(resp)
                return  None
            except Exception as error:
                self.log.error(error)
                return None
            if resp.status_code < 200 or resp.status_code >= 300:
                self.log.error('Error calling ACME endpoint:%s'%resp.reason)
                self.log.error('Status Code:%s'%resp.status_code)
                self.log.error("System error, please contact the system administrator!")
            else:
                get_auth = json.loads(resp.text)
                return get_auth
        self.log.error("System error, please contact the system administrator!")
        return None

    def get_challenges(self,auth_link):
        try:
            resp = requests.get(auth_link[0], headers=self.headers)
        except requests.exceptions.RequestException as error:
            resp = error.response
            self.log.error(resp)
            return None
        except Exception as error:
            self.log.error(error)
            return None
        if resp.status_code < 200 or resp.status_code >= 300:
            self.log.error('Error calling ACME endpoint:%s'%resp.reason)
            self.log.error('Status Code:%s'%resp.status_code)
            return "System error, please contact the system administrator!"
        get_challenges = json.loads(resp.text)
        return get_challenges

    def join_Char(self,one,two):
        return "{0}.{1}".format(one, two)

    def dns_auth_info(self,auth_info):
        if auth_info != None:
            LABLE = "_acme-challenge"
            challenge = self.get_challenges(auth_info["authorizations"])
            if challenge != None and challenge["identifier"] and challenge["challenges"]:
                domain_name = challenge["identifier"]["value"]
                token=challenge["challenges"][0]["token"]
                account_key = myhelper.get_jwk(self.AccountKeyFile)
                keyAuthorization = self.join_Char(token,myhelper.b64(myhelper.JWK_Thumbprint(account_key)))
                TXT = myhelper.b64(myhelper.hash_256_digest(keyAuthorization))
                name = self.join_Char(LABLE, domain_name)
                return ["DNS parse name: %s type: TXT value: %s <br> Please wait for the DNS parsing to take effect."%(name,TXT),json.dumps(auth_info),challenge["challenges"][0]["url"],TXT]
            self.log.error("[Error]: DNS auth error, data request exception.")
        return "System error, please contact the system administrator!"


    def dns_validation(self,TXT,domain,challenge,auth):
        domain = domain[0].split("*")[1]
        domain = '_acme-challenge%s' % domain
        for i in range(1,60):
            dns_query = myhelper.dns_query(domain).split("\"")[1]
            if dns_query == TXT:
                challenge_status = json.loads(requests.get(challenge).text)["status"]
                dns_challenge = self.dns_challenge(challenge)
                if dns_challenge != None or dns_challenge != 'System error, please contact the system administrator!':
                    challenge_res = json.loads(dns_challenge)
                    if challenge_res["status"] == "invalid":
                        self.auth_deactivated(auth["authorizations"][0])
                        self.log.error('[auth error] Authorization error, now stop authorization。')
                        return challenge_res
                    elif challenge_res["status"] == "valid":
                        finalize_res = self.finalize(auth)
                        cert_info = self.get_cert(finalize_res)
                        return cert_info
                    self.log.info(dns_challenge)
        else:
            return 'DNS validation failed.info：%s'%dns_query

    def dns_challenge(self,challenge_link):
        if challenge_link != None:
            new_accuount = self.get_directory()
            nonce = self.get_nonce(new_accuount[self.nonec_path])
            payload = {}
            account_url = self.get_account_url()[1]
            body_top = {"alg": "RS256","kid":account_url,"url": challenge_link,"nonce": nonce}
            jose = self.data_packaging(payload,body_top)
            try:
                resp = requests.post(challenge_link,json=jose,headers=self.headers)
                self.log.info(json.dumps(resp.text))
            except requests.exceptions.RequestException as error:
                resp = error.response
                self.log.error(resp)
                return None
            except Exception as error:
                self.log.error(error)
                return None
            if resp.status_code < 200 or resp.status_code >= 300:
                self.log.error('Error calling ACME endpoint:%s' % resp.reason)
                self.log.error('Status Code:%s' % resp.status_code)
                self.log.error("[ERROR] All info: %s"%json.dumps(resp.text))
                return "本次申请状态已失效，请重新输入域名点击提交按钮"
            if resp.status_code == 201:
                order_location = resp.headers['Location']
                return order_location
            return resp.text
        return "System error, please contact the system administrator!"
    
    def finalize(self,order_info):
        if order_info != None:
            order_info = json.loads(order_info)
            domain = order_info["identifiers"][0]["value"]
            csr_name = '%s%scertificate%s%s%scertificate.csr'%(basemethod.get_root_path(),basemethod.systemc_dir_flag(),basemethod.systemc_dir_flag(),myhelper.DomainDewildcards(domain),basemethod.systemc_dir_flag())
            csr = myhelper.load_csr_file(csr_name)
            new_accuount = self.get_directory()
            nonce = self.get_nonce(new_accuount[self.nonec_path])
            certificate_der = myhelper.csr_pem_to_der(csr)
            payload = {"csr":myhelper.b64(certificate_der)}
            account_url = self.get_account_url()[1]
            body_top = {"alg": "RS256", "kid": account_url, "url": order_info["finalize"], "nonce": nonce}
            jose = self.data_packaging(payload, body_top)
            try:
                resp = requests.post(order_info["finalize"], json=jose, headers=self.headers)
                self.log.info(json.dumps(resp.text))
            except requests.exceptions.RequestException as error:
                resp = error.response
                self.log.error(resp)
                return None
            except Exception as error:
                self.log.error(error)
                return None
            if resp.status_code < 200 or resp.status_code >= 300:
                self.log.error('Error calling ACME endpoint:%s' % resp.reason)
                self.log.error('Status Code:%s' % resp.status_code)
                self.log.error("[ERROR] All info: %s" % json.dumps(resp.text))
                return "请重新生提交证书申请按钮!"
            return json.loads(resp.text)
        self.log.error('[Error] order info is None!')
        return "System error, please contact the system administrator!"

    def get_cert(self,cert_down):
        if cert_down != None or cert_down != "System error, please contact the system administrator!" or cert_down["status"] == "valid" and cert_down["certificate"]:
            self.headers.update({"Accept":"application/pem-certificate-chain"})
            try:
                resp = requests.get(cert_down["certificate"], headers=self.headers)
                self.log.info(json.dumps(resp.text))
            except requests.exceptions.RequestException as error:
                resp = error.response
                self.log.error(resp)
                return None
            except Exception as error:
                self.log.error(error)
                return None
            if resp.status_code < 200 or resp.status_code >= 300:
                self.log.error('Error calling ACME endpoint:%s' % resp.reason)
                self.log.error('Status Code:%s' % resp.status_code)
                self.log.error("[ERROR] All info: %s" % json.dumps(resp.text))
                return "本次申请状态已失效，请重新输入域名点击验证按钮"
            domain_name = cert_down['identifiers'][0]['value']
            domain_dir = myhelper.DomainDewildcards(domain_name)
            certificate_name = '%s%scertificate%s%s%scertificate.pem'%(basemethod.get_root_path(),basemethod.systemc_dir_flag(),basemethod.systemc_dir_flag(),domain_dir,basemethod.systemc_dir_flag())
            key_name = '%s%scertificate%s%s%sprivte.key'%(basemethod.get_root_path(),basemethod.systemc_dir_flag(),basemethod.systemc_dir_flag(),domain_dir,basemethod.systemc_dir_flag())

            myhelper.wirte_ssl_certificate(certificate_name,resp.text)
            return domain_name,certificate_name,key_name,resp.text
        return "System error, please contact the system administrator!"

    def auth_deactivated(self,auth_link):
        if auth_link != None:
            new_accuount = self.get_directory()
            nonce = self.get_nonce(new_accuount[self.nonec_path])
            payload = {"status":"deactivated"}
            account_url = self.get_account_url()[1]
            body_top = {"alg": "RS256","kid":account_url,"url": auth_link,"nonce": nonce}
            jose = self.data_packaging(payload,body_top)
            try:
                resp = requests.post(auth_link,json=jose,headers=self.headers)
                self.log.info(json.dumps(resp.text))
            except requests.exceptions.RequestException as error:
                resp = error.response
                self.log.error(resp)
                return None
            except Exception as error:
                self.log.error(error)
                return None
            if resp.status_code < 200 or resp.status_code >= 300:
                self.log.error('Error calling ACME endpoint:%s' % resp.reason)
                self.log.error('Status Code:%s' % resp.status_code)
                self.log.error("[ERROR] All info: %s"%json.dumps(resp.text))
                return "本次申请状态已失效，请重新输入域名点击提交按钮"
            if resp.status_code == 201:
                order_location = resp.headers['Location']
                return order_location
            return resp.text
        return "System error, please contact the system administrator!"
    
    def revokecert(self):
        pass
    def keychange(self):
        pass