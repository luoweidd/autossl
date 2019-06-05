############################################################
# Version 0.91
# Date Created: 2018-06-15
# Last Update:  2018-06-15
# https://www.neoprime.io
# Copyright (c) 2018, NeoPrime, LLC
# Author: John Hanley
############################################################

""" Let's Encrypt ACME Version 2 Helper Routines"""

def get_indent(indent):
	if indent < 0:
		indent = 0

	if indent > 10:
		indent = 10

	if indent is 0:
		return ''

	s = ''
	for _x in range(indent):
		s += '    '

	return s

def print_dict(arg, indent=0):
	for k in arg:
		value = arg[k]

		if isinstance(value, dict):
			print(get_indent(indent) + k + ':')
			print_dict(value, indent + 1)
		else:
			print(get_indent(indent) + k + ': ' + str(arg[k]))
