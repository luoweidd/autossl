############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-15
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Examples - Get Directory"""

# This example will call the ACME API directory and display the returned data
# Reference: https://ietf-wg-acme.github.io/acme/draft-ietf-acme-acme.html#rfc.section.7.1.1

import	sys
import	requests
import	helper

path = 'https://acme-staging-v02.api.letsencrypt.org/directory'

headers = {
	'User-Agent': 'neoprime.io-acme-client/1.0',
	'Accept-Language': 'en'
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

# The output should be json. If not something is wrong
try:
	acme_config = directory.json()
except Exception as ex:
	print("Error: Cannot load returned data:", ex)
	sys.exit(1)

print('')
print('Returned Data:')
print('****************************************')
print(directory.text)

acme_config = directory.json()

print('')
print('Formatted JSON:')
print('****************************************')
helper.print_dict(acme_config, 0)
