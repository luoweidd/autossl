############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-15
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################
############################################################
# Version 0.92
# Date Created: 2019-06-05
# Last Update:  2019-06-05
# https://www.xxxxx.xxx
# Copyright (c) 2018, luowei, LLC
# Author: luowei
############################################################

""" Let's Encrypt ACME Version 2 Examples - Get Account URL """

# This example will call the ACME API directory and get the account url for the AccountKeyFile
# Reference: https://ietf-wg-acme.github.io/acme/draft-ietf-acme-acme.html#rfc.section.7.3.3

import	sys
import	base64
import	binascii
import	copy
import	json
import	re
import	requests
import	helper
import	myhelper
from new_account import main

path = 'https://acme-staging-v02.api.letsencrypt.org/directory'

AccountKeyFile = 'account.key'

EmailAddresses = ['mailto:123456@qq.com.com', 'mailto:987654@qq.com']

headers = {
	'User-Agent': 'neoprime.io-acme-client/1.0',
	'Accept-Language': 'en',
	'Content-Type': 'application/jose+json'
}

try:
	print('Calling endpoint:', path)
	directory = requests.get(path, headers=headers)
except requests.exceptions.RequestException as error:
	print(error)
	sys.exit(1)

if directory.status_code < 200 or directory.status_code >= 300:
	print('Error calling ACME endpoint:', directory.reason)
	sys.exit(1)

# The following statements are to understand the output
acme_config = directory.json()

url = acme_config["newAccount"]

nonce = requests.head(acme_config['newNonce']).headers['Replay-Nonce']

# Create the account request
payload = {}

payload["termsOfServiceAgreed"] = True
payload["contact"] = EmailAddresses

payload_b64 = myhelper.b64(json.dumps(payload).encode("utf8"))

body_top = {
	"alg": "RS256",
	"jwk": myhelper.get_jwk(AccountKeyFile),
	"url": url,
	"nonce": nonce
}

body_top_b64 = myhelper.b64(json.dumps(body_top).encode("utf8"))

#
# Create the message digest
#

data = "{0}.{1}".format(body_top_b64, payload_b64).encode("utf8")

signature = myhelper.sign(data, AccountKeyFile)

#
# Create the HTML request body
#

jose = {
	"protected": body_top_b64,
	"payload": payload_b64,
	"signature": myhelper.b64(signature)
}

#
# Make the ACME request
#

try:
	print('Calling endpoint:', url)
	resp = requests.post(url, json=jose, headers=headers)
except requests.exceptions.RequestException as error:
	resp = error.response
	print(resp)
except Exception as error:
	print(error)

print('')

if resp.status_code < 200 or resp.status_code >= 300:
	print('Error calling ACME endpoint:', resp.reason)
	print('Status Code:', resp.status_code)
	sys.exit(1)

def GetAccountURL():
	if 'Location' in resp.headers:
		print('Account URL:', resp.headers['Location'])
		nonce = resp.headers['Replay-Nonce']
		account_url = resp.headers['Location']
		return nonce,account_url
	else:
		print('Error: Response headers did not contain the header "Location"')
		main()
		GetAccountURL()