############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-15
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Helper Routines"""

import platform
import sys

P2 = platform.sys.version_info.major < 3

def printf(format, *values):
    print(format % values )

def print_headers(indent, hdrs):
	spaces = ''
	for i in range(indent):
		spaces = spaces + '    '
	for index, name in enumerate(hdrs):
		if isinstance(hdrs[name], dict):
			printf("%s%s:", spaces, name)
			print_headers(indent + 1, hdrs[name])
			continue
		printf("%s%s: %s", spaces, name, hdrs[name])

def gethex(x):
	s = '0123456789ABCDEF'
	str = ''
	if P2 == True:
		a = (ord(x) & 0xf0) >> 4
	else:
		a = (x & 0xf0) >> 4
	str += s[a];
	if P2 == True:
		a = ord(x) & 0xf
	else:
		a = x & 0xf
	str += s[a];
	return str

def getascii(s):
	if P2 == True:
		x = ord(s)
	else:
		x = s

	if x >= 0x20 and x <= 127:
		return chr(x)

	return '.'

def dohex_flush(index, line):
	if index == 0:
		return;

	if index < 8:
		for x in range(index, 8):
			sys.stdout.write('   ')
		index = 8
		sys.stdout.write('- ')

	if index < 16:
		for x in range(index, 16):
			sys.stdout.write('   ')
		sys.stdout.write(line)
		print('')

def dohex(data):
	s = '0123456789ABCDEF'
	line = ''
	index = 0
	off = 0
	for x in data:
		if index == 0:
			sys.stdout.write('{0:04x}'.format(off))
			sys.stdout.write(': ')

		s = gethex(x) + " "
		sys.stdout.write(s)

		line += getascii(x)

		index += 1
		off += 1

		if index == 8:
			line += " - "
			sys.stdout.write('- ')

		if index == 16:
			sys.stdout.write('  ')
			sys.stdout.write(line)
			index = 0
			line = ''
			print('')

	dohex_flush(index, line)

def dohex_off_len(data, off, len):
	s = '0123456789ABCDEF'
	line = ''
	index = 0
#	total = len(data)

#	if total > (off + len):
#		total = off + len

	total = off + len

	for x in range(off, total):
		if index == 0:
			sys.stdout.write('{0:04x}'.format(off))
			sys.stdout.write(': ')

		s = gethex(data[x]) + " "
		sys.stdout.write(s)

		line += getascii(data[x])

		index += 1
		off += 1

		if index == 8:
			line += " - "
			sys.stdout.write('- ')

		if index == 16:
			sys.stdout.write('  ')
			sys.stdout.write(line)
			index = 0
			line = ''
			print('')

	dohex_flush(index, line)
