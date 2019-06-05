############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-15
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Examples - Terms of Service"""

# This example will call the ACME API directory and display the terms of service URL
# Reference: https://ietf-wg-acme.github.io/acme/draft-ietf-acme-acme.html#rfc.section.7.3

import	sys
import	requests

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

# Get the URL for the terms of service
terms_service = acme_config.get("meta", {}).get("termsOfService", "")

print('')
print('Terms of Service:', terms_service)
