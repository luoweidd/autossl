############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-15
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Examples - Get Nonce"""

# This example will call the ACME API directory and obtain a nonce value
# Reference: https://ietf-wg-acme.github.io/acme/draft-ietf-acme-acme.html#rfc.section.6.4

import	sys
import	requests
import	helper

path = 'https://acme-staging-v02.api.letsencrypt.org/directory'

headers = {
	'User-Agent': 'neoprime.io-acme-client/1.0',
	'Accept-Language': 'en',
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

# This is a sigle line statement that you would normally use
# nonce = requests.head(acme_config['newNonce']).headers['Replay-Nonce']

url = acme_config['newNonce']

# Notice here we call the HTTP HEAD method instead of GET

def get_nonce():
	print('')
	print('Returned Headers:')
	print('****************************************')
	r = requests.head(url)
	helper.print_dict(r.headers)

	print('')
	print('Returned Nonce Value:')
	print('****************************************')
	nonce = r.headers['Replay-Nonce']
	print('Nonce:', nonce)
