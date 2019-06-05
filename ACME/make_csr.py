############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-22
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Examples - Create CSR (Certificate Signing Request) """

import	OpenSSL

def create_csr(pkey, domain_name, email_address):
	""" Generate a certificate signing request """

	# create certifcate request
	cert = OpenSSL.crypto.X509Req()
	cert.get_subject().emailAddress = email_address
	cert.get_subject().CN = domain_name

	key_usage = [b"Digital Signature", b"Non Repudiation", b"Key Encipherment"]

	san_list = ["DNS:" + domain_name]

	cert.add_extensions([
		OpenSSL.crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
		OpenSSL.crypto.X509Extension(b"keyUsage", False, b",".join(key_usage)),
		OpenSSL.crypto.X509Extension(b"subjectAltName", False, ", ".join(san_list).encode("utf-8"))
	])

	cert.set_pubkey(pkey)
	cert.sign(pkey, 'sha256')

	return cert

# Load the privte Key
def csr_file_key(KEY_FILE,domain,emailAddress):
	data = open(KEY_FILE, 'rt').read()

	csr_pkey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, data)

	csr_cert = create_csr(csr_pkey, domain, emailAddress)

	with open('./%s/%s.csr'%(domain,domain), 'wt') as f:
		data = OpenSSL.crypto.dump_certificate_request(OpenSSL.crypto.FILETYPE_PEM, csr_cert)
		f.write(data.decode('utf-8'))

# domain='3123123.com'
# emailaddres='12312141@qq.com'
# csr_file_key('./%s/%s.key'%(domain,domain),domain,emailaddres)