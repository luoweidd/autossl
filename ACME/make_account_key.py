############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-15
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Examples - Create Account Key """

from Crypto.PublicKey import RSA

def make_account_private():
	filename = '_private.key'

	key = RSA.generate(4096)

	with open(filename, 'w') as f:
		f.write(key.exportKey().decode('utf-8'))
