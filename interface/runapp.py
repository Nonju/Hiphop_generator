
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from textgeneration import generator

def run():
	print 'Running app...'

	order = None
	while not isinstance(order, int):
		order = raw_input('Use models of order (2, 3, 4): ')
		try:
			if int(order) not in [2, 3, 4]: continue
			order = int(order)
		except: continue

	while True:
		title = raw_input('Generate Title? (y / n): ')
		if title in ['y','Y','n','N']:
			break

	# lyrics = generator.generateLyrics(modelOrder=order)
	if title in ['Y','y']: 
		title = generator.generateTitle(2)
		print title
	print generator.generateLyrics(modelOrder=order)

