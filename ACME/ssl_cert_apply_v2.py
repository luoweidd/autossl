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
import os
from base.mylog import loglog


class ssl_cert_v2:

    logs = loglog()
    log = logs.logger
    base_path = 'https://acme-staging-v02.api.letsencrypt.org/directory'

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
    order_path="newNonce"
    Authz_path="newAuthz"
    revokeCert="revokeCert"
    keyChange="keyChange"

    AccountKeyFile = 'account.key'
    EmailAddresses = ['mailto:123456@qq.com.com', 'mailto:987654@qq.com']

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
        if os.path.exists(self.AccountKeyFile) is not False:
            return True

        self.log.error('Error: File does not exist: {0}'.format(self.AccountKeyFile))

        if myhelper.Confirm('Create new account private key (y/n): ') is False:
            self.log.error('Cancelled')
            return False

        myhelper.create_rsa_private_key(self.AccountKeyFile)

        if os.path.exists(self.AccountKeyFile) is False:
            self.log.error('Error: File does not exist: {0}'.format(self.AccountKeyFile))
            return False

        return True

    def make_account_private_key(self):
        filename = '_private.key'
        myhelper.create_rsa_private_key(filename)

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
        if self.check_account_key_file() is False:
            self.make_account_private_key()
        new_accuount = self.get_directory()
        accuount_url = new_accuount[self.account_path]
        nonce = self.get_nonce(new_accuount[self.nonec_path])
        # Get the URL for the terms of service
        terms_service = new_accuount.get("meta", {}).get("termsOfService", "")
        self.log.info('Terms of Service:', terms_service)
        # Create the account request
        if terms_service != "":
            payload = {"termsOfServiceAgreed": True,"contact": self.EmailAddresses}
            self.log.info(payload)
        body_top = {"alg": "RS256","jwk": myhelper.get_jwk(self.AccountKeyFile),"url": accuount_url,"nonce": nonce}
        jose = self.data_packaging(payload,body_top)
        try:
            self.log.info('Calling endpoint:', accuount_url)
            resp = requests.post(accuount_url, json=jose, headers=self.headers)
        except requests.exceptions.RequestException as error:
            resp = error.response
            self.log.error(resp)
        except Exception as ex:
            self.log.error(ex)
        except BaseException as ex:
            self.log.error(ex)
        if resp.status_code < 200 or resp.status_code >= 300:
            self.log.info('Error calling ACME endpoint:', resp.reason)
            self.log.error('Status Code:', resp.status_code)
            myhelper.process_error_message(resp.text)
        if 'Location' in resp.headers:
            self.log.info('Account URL:', resp.headers['Location'])
        else:
            self.log.error('Error: Response headers did not contain the header "Location"')
            return "System error, please contact the system administrator!"

    def get_account_url(self):
        dir_noce=self.get_directory()
        # Create the account request
        payload = {"termsOfServiceAgreed": True, "contact": self.EmailAddresses}
        nonce=self.get_nonce(dir_noce[self.nonec_path])
        body_top = {"alg": "RS256","jwk": myhelper.get_jwk(self.AccountKeyFile),"url": dir_noce[self.account_path],"nonce": nonce}
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

    def new_order(self,csrfile):
        """ Request an SSL certificate from the ACME server """
        accounts=self.get_account_url()
        domains = myhelper.get_domains_from_csr(csrfile)
        # Create the account request
        self.log.info("Request to the ACME server an order to validate domains.")
        payload = {"identifiers": [{"type": "dns", "value": domain} for domain in domains]}
        body_top = {"alg": "RS256","kid": accounts[1],"nonce": accounts[0],"url": accounts[1]}
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
            nonce = resp.headers[self.nonec]
            if resp.status_code == 201:
                order_location = resp.headers['Location']
                return nonce,order_location
            return nonce,resp

    def new_authz(self):
        pass
    def revokecert(self):
        pass
    def keychange(self):
        pass