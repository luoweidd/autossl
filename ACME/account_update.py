############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-22
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Examples - Update Account """

# This example will call the ACME API directory and update the account information
# Reference: https://ietf-wg-acme.github.io/acme/draft-ietf-acme-acme.html#rfc.section.7.3.2

import	sys
import	json
import	requests
import	helper
import	myhelper

debug = 0

path = 'https://acme-staging-v02.api.letsencrypt.org/directory'

AccountKeyFile = 'account.key'

EmailAddresses = ['mailto:someone@example.com', 'someone2@example.com']

headers = {
	'User-Agent': 'neoprime.io-acme-client/1.0',
	'Accept-Language': 'en',
	'Content-Type': 'application/jose+json'
}

def get_account_url(url, nonce):
	# Create the account request
	payload = {}

	payload["termsOfServiceAgreed"] = True
	payload["contact"] = EmailAddresses
	payload["onlyReturnExisting"] = True

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

	if resp.status_code < 200 or resp.status_code >= 300:
		print('Error calling ACME endpoint:', resp.reason)
		print('Status Code:', resp.status_code)
		myhelper.process_error_message(resp.text)
		sys.exit(1)

	if 'Location' in resp.headers:
		print('Account URL:', resp.headers['Location'])
	else:
		print('Error: Response headers did not contain the header "Location"')

	nonce = resp.headers['Replay-Nonce']

	return nonce, resp.headers['Location']

def account_update(nonce, url, location):
	# Create the account request
	payload = {}

	#payload["termsOfServiceAgreed"] = True
	payload["contact"] = EmailAddresses

	payload_b64 = myhelper.b64(json.dumps(payload).encode("utf8"))

	body_top = {
		"alg": "RS256",
		"kid": location,
		"nonce": nonce,
		"url": location
	}

	body_top_b64 = myhelper.b64(json.dumps(body_top).encode("utf8"))

	#
	# Create the message digest (signature)
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

	host = location.split("//")[-1].split("/")[0].split('?')[0]

	headers['Host'] = host

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

	#print(resp.request.headers)
	#print(resp.headers)
	#print(resp.text)

	if resp.status_code < 200 or resp.status_code >= 300:
		print('Error calling ACME endpoint:', resp.reason)
		print('Status Code:', resp.status_code)
		myhelper.process_error_message(resp.text)
		sys.exit(1)

	nonce = resp.headers['Replay-Nonce']

	return nonce, resp.text

try:
	print('Calling endpoint:', path)
	resp = requests.get(path, headers=headers)
except requests.exceptions.RequestException as error:
	print(error)
	sys.exit(1)

if resp.status_code < 200 or resp.status_code >= 300:
	print('Error calling ACME endpoint:', resp.reason)
	print(resp.text)
	sys.exit(1)

# The following statements are to understand the output
acme_config = resp.json()

url = acme_config["newAccount"]

nonce = requests.head(acme_config['newNonce']).headers['Replay-Nonce']

nonce, location = get_account_url(url, nonce)

nonce, resp = account_update(nonce, location, location)

info = json.loads(resp)

if debug is 1:
	print('')
	print('Returned Data:')
	print('##################################################')
	#print(info)
	helper.print_dict(info)
	print('##################################################')

print('')
print('ID:        ', info['id'])
print('Contact:   ', info['contact'])
print('Initial IP:', info['initialIp'])
print('Created At:', info['createdAt'])
print('Status:   ', info['status'])
