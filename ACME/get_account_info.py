############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-22
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Examples - Get Account Information """

############################################################
# This example will call the ACME API directory and get the account information
# Reference: https://ietf-wg-acme.github.io/acme/draft-ietf-acme-acme.html#rfc.section.7.3.3
#
# This program uses the AccountKeyFile set in acme.ini to return information about the ACME account.
############################################################

import	sys
import	json
import	requests
import	helper
import	myhelper

############################################################
# Start - Global Variables

g_debug = 0

acme_path = ''
AccountKeyFile = ''
EmailAddresses = []
headers = {}

# End - Global Variables
############################################################

############################################################
# Load the configuration from acme.ini
############################################################

def load_acme_parameters(debug=0):
	""" Load the configuration from acme.ini """

	global acme_path
	global AccountKeyFile
	global EmailAddresses
	global headers

	config = myhelper.load_acme_config(filename='acme.ini')

	if debug is not 0:
		print(config.get('acme-neoprime', 'accountkeyfile'))
		print(config.get('acme-neoprime', 'csrfile'))
		print(config.get('acme-neoprime', 'chainfile'))
		print(config.get('acme-neoprime', 'acmedirectory'))
		print(config.get('acme-neoprime', 'contacts'))
		print(config.get('acme-neoprime', 'language'))

	acme_path = config.get('acme-neoprime', 'acmedirectory')

	AccountKeyFile = config.get('acme-neoprime', 'accountkeyfile')

	EmailAddresses = config.get('acme-neoprime', 'contacts').split(';')

	headers['User-Agent'] = config.get('acme-neoprime', 'UserAgent')
	headers['Accept-Language'] = config.get('acme-neoprime', 'language')
	headers['Content-Type'] = 'application/jose+json'

	return config

############################################################
#
############################################################

def get_account_url(url, nonce):
	""" Get the Account URL based upon the account key """

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

	if g_debug:
		print(body_top)

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

	if g_debug:
		print(jose)

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

	# Get the nonce for the next command request
	nonce = resp.headers['Replay-Nonce']

	account_url = resp.headers['Location']

	return nonce, account_url

############################################################
#
############################################################

def get_account_info(nonce, url, location):
	""" Get the Account Information """

	# Create the account request
	payload = {}

	payload_b64 = myhelper.b64(json.dumps(payload).encode("utf8"))

	body_top = {
		"alg": "RS256",
		"kid": location,
		"nonce": nonce,
		"url": location
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

	if g_debug:
		print(jose)

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

	nonce = resp.headers['Replay-Nonce']

	# resp.text is the returned JSON data describing the account

	return nonce, resp.text

############################################################
#
############################################################

def load_acme_urls(path):
	""" Load the ACME Directory of URLS """
	try:
		print('Calling endpoint:', path)
		resp = requests.get(acme_path, headers=headers)
	except requests.exceptions.RequestException as error:
		print(error)
		sys.exit(1)

	if resp.status_code < 200 or resp.status_code >= 300:
		print('Error calling ACME endpoint:', resp.reason)
		print(resp.text)
		sys.exit(1)

	return resp.json()

############################################################
#
############################################################

def acme_get_nonce(urls):
	""" Get the ACME Nonce that is used for the first request """
	global	headers

	path = urls['newNonce']

	try:
		print('Calling endpoint:', path)
		resp = requests.head(path, headers=headers)
	except requests.exceptions.RequestException as error:
		print(error)
		return False

	if resp.status_code < 200 or resp.status_code >= 300:
		print('Error calling ACME endpoint:', resp.reason)
		print(resp.text)
		return False

	return resp.headers['Replay-Nonce']

############################################################
# Main Program Function
############################################################

def main(debug=0):
	""" Main Program Function """
	acme_urls = load_acme_urls(acme_path)

	url = acme_urls["newAccount"]

	nonce = acme_get_nonce(acme_urls)

	if nonce is False:
		sys.exit(1)

	nonce, account_url = get_account_url(url, nonce)

	# resp is the returned JSON data describing the account
	nonce, resp = get_account_info(nonce, account_url, account_url)

	info = json.loads(resp)

	if debug is not 0:
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

def is_json(data):
	try:
		json.loads(data)
	except ValueError as e:
		return False
	return True

acme_config = load_acme_parameters(g_debug)

main(g_debug)
