############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-15
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Helper Routines"""

import	base64
import	binascii
import	configparser
import	json
import	subprocess,os
import	OpenSSL
import  logging
from Crypto.Util.asn1 import DerSequence
from Crypto.PublicKey import RSA
from Crypto.Hash.SHA256 import SHA256Hash

log=logging.getLogger('"lw-ghy-acme"')

# helper function base64 encode as defined in acme spec
def b64(b):
	try:
		return base64.urlsafe_b64encode(b).decode("utf8").rstrip("=")
	except Exception as e:
		print e
		return None

# helper function to run openssl command
def run_openssl(command, options, communicate=None):
	openssl = subprocess.Popen(
		["openssl", command] + options,
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE)

	out, err = openssl.communicate(communicate)

	if openssl.returncode != 0:
		raise IOError("OpenSSL Error: {0}".format(err))

	return out

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

def make_certificate_key(domainname):
    filename = '*./%s/%s.key'%(domainname,domainname)
    key = RSA.generate(4096)
    if not os.path.exists(domainname):
        os.makedirs('*./%s'%domainname,mode=0775)
    with open(filename,'w') as f:
        f.write(key.exportKey().decode('utf-8'))

def get_domains_from_csr(csrFile):
	""" Return the domain names from a CSR """

	domains = set([])
	with open(csrFile, 'r') as f:
		data = f.read()

	cert = OpenSSL.crypto.load_certificate_request(OpenSSL.crypto.FILETYPE_PEM, data)

	subject = cert.get_subject()

	domains.add(subject.CN)

	for ext in cert.get_extensions():
		if ext.get_short_name() != b'subjectAltName':
			continue

		data = ext.__str__()

		names = [x.strip() for x in data.split(',')]

		for name in names:
			domains.add(name[4:])

	if not domains:
		raise ValueError("No domains to validate in the provided CSR.")

	return domains

def process_error_message(msg):
	""" Process the error from an ACME call """
	#print(msg)
	#print('msg:', msg)
	info = json.loads(msg)
	print('Error Type:', info['type'])
	print('Detail:    ', info['detail'])

def load_private_key(keyfile):
	try:
		with open(keyfile, 'r') as f:
			data = f.read()

		if data.startswith('-----BEGIN '):
			pkey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, data)
		else:
			pkey = OpenSSL.crypto.load_pkcs12(data).get_privatekey()

		return pkey
	except IOError as e:
		print e
		return None

def int2hex(val):
	hex_val = "{0:x}".format(int(val))

	# add a zero if the hex_val length is an odd number
	if len(hex_val) % 2:
		hex_val = '0' + hex_val

	# returns a hex string representing "val"
	return hex_val

def get_public_key_from_private_key(pkey):
	try:
		private_key_der = DerSequence()
		private_key_der.decode(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, pkey))

		modulus = int2hex(private_key_der[1])
		exp = int2hex(private_key_der[2])

		return modulus, exp
	except TypeError as e:
		print e
		return None

def get_jwk(file):
	""" Create the JWK token """

	# Load the RSA Private Key from the file (RSA PKCS #1)
	try:
		pkey = load_private_key(file)

		# Get the modulus and public exponent from the private key
		modulus, pub_exp = get_public_key_from_private_key(pkey)

		n = binascii.unhexlify(modulus)		# convert to binary data
		e = binascii.unhexlify(pub_exp)		# convert to binary data

		jwk = {
			"e": b64(e),
			"kty": "RSA",
			"n": b64(n)
		}

		return jwk
	except Exception as e:
		return None

def JWK_Thumbprint(key_dict):
	'''
	Computing the input parameter object has-256 digest
	:param key_dict: Arbitrarily object
	:return: has-256 digest
	'''
	key_json = json.dumps(key_dict,separators=(',',':')).encode("utf8")
	hash_265 = SHA256Hash(key_json).digest()
	return hash_265

def sign(data, keyfile):
	try:
		""" Create the ACME API Signature """

		# Load the RSA Private Key from the file (RSA PKCS #1)
		pkey = load_private_key(keyfile)

		# Create the signature
		sig = OpenSSL.crypto.sign(pkey, data, "sha256")

		return sig
	except Exception as e:
		log.error(e)
		return None

def Confirm(msg):
	# ans = raw_input(msg)
	# if ans in ['y', 'Y']:
	# 	return True

	return True

def create_rsa_private_key(filename):
	key = RSA.generate(4096)

	with open(filename, 'w') as f:
		f.write(key.exportKey().decode('utf-8'))

	return True


def create_csr(csr_pkey, domain_name, email_address):
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

	cert.set_pubkey(csr_pkey)
	cert.sign(csr_pkey, 'sha256')

	return cert


# def make_csrfile(domain_name, email_address):
# 	data = open(KEY_FILE, 'rt').read()
#
# 	csr_pkey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, data)
#
# 	csr_cert = create_csr(csr_pkey, domain_name, email_address)
#
# 	with open(CSR_FILE, 'wt') as f:
# 		data = OpenSSL.crypto.dump_certificate_request(OpenSSL.crypto.FILETYPE_PEM, csr_cert)
# 		f.write(data.decode('utf-8'))

def make_certificate_key(domain_name):
    filename = '%s/%s.key'%(domain_name,domain_name)
    key = RSA.generate(4096)
    if not os.path.exists(domain_name):
        os.makedirs('%s'%domain_name,mode=0775)
    with open(filename,'w') as f:
        f.write(key.exportKey().decode('utf-8'))

