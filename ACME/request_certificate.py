############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-15
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Examples - Get an SSL Certificate from the ACME v2 Server """

############################################################
# This example will call the ACME server to request and download an SSL certificate based upon a CSR
# Reference: https://ietf-wg-acme.github.io/acme/draft-ietf-acme-acme.html#rfc.section.7.4.1
############################################################

import	sys
import	json
import	logging
import	requests
import	helper
import	myhelper

############################################################
# Start - Global Variables

g_debug = 0

acme_path = 'https://acme-staging-v02.api.letsencrypt.org/directory'
AccountKeyFile = 'account.key'
AccountKeyJson = 'account.json'
EmailAddresses = ['mailtoto:123456@qq.com,mailto:98765@qq.com']
headers = {
	'User-Agent': 'neoprime.io-acme-client/2.0',
	'Accept-Language': 'en',
	'Content-Type': 'application/jose+json'
}

LOGGER = logging.getLogger('neoprime')
LOGGER.addHandler(logging.StreamHandler())

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

	config = myhelper.load_acme_config(filename='ACME/acme.ini')

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
# Request an SSL certificate from the ACME server
############################################################

def request_certificate(config, urls, nonce, location):
	""" Request an SSL certificate from the ACME server """

	url = urls["newOrder"]

	csrFile = config.get('acme-neoprime', 'csrfile')
	chainFile = config.get('acme-neoprime', 'chainfile')

	print('CSR:', csrFile)
	print('CHAIN:', chainFile)
	print('URL:', url)
	print('Account URL:', location)

	#
	log = LOGGER

	#
	domains = myhelper.get_domains_from_csr(csrFile)

	# Create the account request
	log.info("Request to the ACME server an order to validate domains.")
	payload = {"identifiers": [{"type": "dns", "value": domain} for domain in domains]}

	print(payload)

	payload_b64 = myhelper.b64(json.dumps(payload).encode("utf8"))

	body_top = {
		"alg": "RS256",
		"kid": location,
		"nonce": nonce,
		"url": url
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

	nonce = resp.headers['Replay-Nonce']

	if resp.status_code == 201:
		order_location = resp.headers['Location']

	# resp.text is the returned JSON data describing the new order

	return nonce, resp.text, order_location

# ############################################################
# # Main Program Function
# ############################################################
#
# def main(config, debug=0):
# 	""" Main Program Function """
# 	acme_urls = load_acme_urls(acme_path)
#
# 	url = acme_urls["newAccount"]
#
# 	nonce = acme_get_nonce(acme_urls)
#
# 	if nonce is False:
# 		sys.exit(1)
#
# 	nonce, account_url = get_account_url(url, nonce)
#
# 	# resp is the returned JSON data describing the account
# 	nonce, resp = get_account_info(nonce, account_url, account_url)
#
# 	info = json.loads(resp)
#
# 	if debug is not 0:
# 		print('')
# 		print('Returned Data:')
# 		print('##################################################')
# 		#print(info)
# 		helper.print_dict(info)
# 		print('##################################################')
#
# 	print('')
# 	print('ID:        ', info['id'])
# 	print('Contact:   ', info['contact'])
# 	print('Initial IP:', info['initialIp'])
# 	print('Created At:', info['createdAt'])
# 	print('Status:   ', info['status'])
#
# 	nonce, resp, order_location = request_certificate(config, acme_urls, nonce, account_url)
#
# 	print('Order Location:', order_location)
# 	print('')
# 	print(resp)
#
# 	# Save the response, the next example program will process this
# 	# in a real program, we would process the response now
#
# 	print('Saving certificate request response in cert_request.data')
# 	with open('cert_request.data', "w+") as f:
# 		f.write(resp)
# 	return {"nonce":nonce,"resp":resp,"order_location":order_location}

############################################################
# Request an SSL certificate from the ACME server
############################################################

# acme_config = load_acme_parameters(g_debug)
#
# main(acme_config, g_debug)


def cert_request_authorizations(g_debug=0):
	""" Main Program Function """
	acme_urls = load_acme_urls(acme_path)
	acme_config = load_acme_parameters(g_debug)
	url = acme_urls["newAccount"]

	nonce = acme_get_nonce(acme_urls)

	if nonce is False:
		sys.exit(1)

	nonce, account_url = get_account_url(url, nonce)

	# resp is the returned JSON data describing the account
	nonce, resp = get_account_info(nonce, account_url, account_url)

	info = json.loads(resp)

	if g_debug is not 0:
		print('')
		print('Returned Data:')
		print('##################################################')
		# print(info)
		helper.print_dict(info)
		print('##################################################')

	print('')
	print('ID:        ', info['id'])
	print('Contact:   ', info['contact'])
	print('Initial IP:', info['initialIp'])
	print('Created At:', info['createdAt'])
	print('Status:   ', info['status'])

	nonce, resp, order_location = request_certificate(acme_config, acme_urls, nonce, account_url)

	# print('Order Location:', order_location)
	# print('')
	# print(resp)

	# Save the response, the next example program will process this
	# in a real program, we would process the response now

	# print('Saving certificate request response in cert_request.data')
	# with open('cert_request.data', "w+") as f:
	# 	f.write(resp)
	return {"nonce": nonce, "resp": resp, "order_location": order_location}


############################################################
# Request an SSL certificate from the ACME server
############################################################


def authorizations_cert_request_info():
	urls = cert_request_authorizations(g_debug)
	url = urls["resp"]
	auth_url = json.loads(url)["authorizations"][0].encode('utf8')
	reps = requests.request('GET', auth_url)
	for authorizations_type in reps["challenges"]:
		if authorizations_type["type"] == "dns-01":
			return authorizations_type["token"]


def token_challenges():
	token = authorizations_cert_request_info()
	signature = myhelper.sign(token, AccountKeyFile)
	return signature


def dns_authorizations():
	urls = cert_request_authorizations(g_debug)
	url = urls["resp"]
	auth_url=json.loads(url)["authorizations"][0].encode('utf8')

	acme_urls = load_acme_urls(acme_path)
	account_url = acme_urls["newAccount"]
	nonce = acme_get_nonce(acme_urls)
	location = get_account_url(account_url,nonce)

	print('Calling endpoint:', auth_url)
	get_resp = requests.get(auth_url, headers=headers)
	challenges = json.loads(get_resp.content)["challenges"][2]
	print(challenges)
	challenges_url= challenges["url"]
	challenges_token = challenges["token"]

	payload = {}
	payload_b64 = myhelper.b64(json.dumps(payload).encode("utf8"))

	nonce_b = acme_get_nonce(acme_urls)
	body_top = {
		"alg": "RS256",
		"kid": location[1],
		"nonce": nonce_b,
		"url": challenges_url
	}

	body_top_b64 = myhelper.b64(json.dumps(body_top).encode("utf8"))

	#
	# Create the message digest
	#

	data = "{0}.{1}".format(body_top_b64, payload_b64).encode("utf8")

	signature = myhelper.sign(data, AccountKeyFile)

	jose = {
		"protected": body_top_b64,
		"payload": payload_b64,
		"signature": myhelper.b64(signature)
	}

	try:
		resp = requests.post(auth_url,json=jose, headers=headers)
	except requests.exceptions.RequestException as error:
		resp = error.response
		print(resp)
	except Exception as error:
		print(error)

	if resp.status_code < 200 or resp.status_code >= 300:
		print('Error calling ACME endpoint:', resp.reason)
		print('Status Code:', resp.status_code)
		myhelper.process_error_message(resp.text)
		# sys.exit(1)

	# resp.text is the returned JSON data describing the new order

	return resp

	def download_cert(url):
		resp = requests.get(url)
		return resp

dns_authorizations()
token_challenges
