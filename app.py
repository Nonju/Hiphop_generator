
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Entry point for Hip-hop generator app

Written using python2.7
"""

from generate import generateLyrics

def main():

	testRows= 5
	order = None
	while not isinstance(order, int):
		order = raw_input('order: ')
		try:
			if int(order) not in [2, 3, 4]: continue
			order = int(order)
		except: continue

	while True:
		print generateLyrics(modelOrder=order)
		raw_input()
		print '-' * 42

if __name__ == '__main__':
	main()
