############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-15
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Examples - New Account"""

# This example will call the ACME API directory and create a new account
# Reference: https://ietf-wg-acme.github.io/acme/draft-ietf-acme-acme.html#rfc.section.7.3.2

import	os
import	sys
import	json
import	requests
import	myhelper

# Staging URL
path = 'https://acme-staging-v02.api.letsencrypt.org/directory'

# Production URL
# path = 'https://acme-v02.api.letsencrypt.org/directory'

AccountKeyFile = 'account.key'
g_debug=0

EmailAddresses = ['mailto:123456@qq.com', 'mailto:987654@qq.com']

def check_account_key_file():
	""" Verify that the Account Key File exists and prompt to create if it does not exist """
	if os.path.exists(AccountKeyFile) is not False:
		return True

	print('Error: File does not exist: {0}'.format(AccountKeyFile))

	if myhelper.Confirm('Create new account private key (y/n): ') is False:
		print('Cancelled')
		return False

	myhelper.create_rsa_private_key(AccountKeyFile)

	if os.path.exists(AccountKeyFile) is False:
		print('Error: File does not exist: {0}'.format(AccountKeyFile))
		return False

	return True

def get_directory():
	""" Get the ACME Directory """
	headers = {
		'User-Agent': 'neoprime.io-acme-client/1.0',
		'Accept-Language': 'en',
	}

	try:
		print('Calling endpoint:', path)
		directory = requests.get(path, headers=headers)
	except requests.exceptions.RequestException as error:
		print(error)
		return False

	if directory.status_code < 200 or directory.status_code >= 300:
		print('Error calling ACME endpoint:', directory.reason)
		print(directory.text)
		return False

	# The following statements are to understand the output
	acme_config = directory.json()

	return acme_config

def main():
	""" Main Program Function """
	headers = {
		'User-Agent': 'neoprime.io-acme-client/1.0',
		'Accept-Language': 'en',
		'Content-Type': 'application/jose+json'
	}

	if check_account_key_file() is False:
		sys.exit(1)

	acme_config = get_directory()

	if acme_config is False:
		sys.exit(1)

	url = acme_config["newAccount"]

	# Get the URL for the terms of service
	terms_service = acme_config.get("meta", {}).get("termsOfService", "")
	print('Terms of Service:', terms_service)

	nonce = requests.head(acme_config['newNonce']).headers['Replay-Nonce']
	print('Nonce:', nonce)
	print("")

	# Create the account request
	payload = {}

	if terms_service != "":
		payload["termsOfServiceAgreed"] = True

	payload["contact"] = EmailAddresses

	if g_debug:
		print(payload)

	payload_b64 = myhelper.b64(json.dumps(payload).encode("utf8"))

	body_top = {
		"alg": "RS256",
		"jwk": myhelper.get_jwk(AccountKeyFile),
		"url": url,
		"nonce": nonce
	}

	if g_debug:
		print(body_top)

	body_top_b64 = myhelper.b64(json.dumps(body_top).encode("utf8"))

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

	try:
		print('Calling endpoint:', url)
		resp = requests.post(url, json=jose, headers=headers)
	except requests.exceptions.RequestException as error:
		resp = error.response
		print(resp)
	except Exception as ex:
		print(ex)
	except BaseException as ex:
		print(ex)

	if resp.status_code < 200 or resp.status_code >= 300:
		print('Error calling ACME endpoint:', resp.reason)
		print('Status Code:', resp.status_code)
		myhelper.process_error_message(resp.text)
		sys.exit(1)

	print('')
	if 'Location' in resp.headers:
		print('Account URL:', resp.headers['Location'])
	else:
		print('Error: Response headers did not contain the header "Location"')

main()

sys.exit(0)
