
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import re

def tokenizeString(string=''):
	"""
	Returns tokenized string as 'list'
	Returns 'None' if invalid string
	"""
	string = string.lower()
	pattern = r"([A-Za-z']+)\s*"
	match = re.findall(pattern, string)

	if not len(match):
		return None
	return match

