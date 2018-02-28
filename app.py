
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Entry point for Hip-hop generator app

Written using python2.7
"""

import codecs
import json

from vocab import vocab
# models
from models import bigram
from models import trigram
from models import quadrigram
from generate import generateLyrics

def getDocuments():
	#Replace with function that uses search
	with codecs.open('genius-lyrics-search/output.json', 'r', encoding='utf8') as documents:
		return json.loads(documents.read())

def getPart(docs, partName=''):
	parts = []
	for doc in docs:

		if partName not in doc['lyrics'].keys():
			continue

		for part in doc['lyrics'][partName]:
			parts.append(part)

	return parts

def modelTrain(order=4): # Currently training of verses
	voc = vocab.getVocab()
	docs = getDocuments()

	verseDocs = getPart(docs, partName=u'verse')
	# return bigram.Bigram.train(voc, verseDocs)

	if order == 2:
		return bigram.Bigram.train(voc, verseDocs)
	elif order == 3:
		return trigram.Trigram.train(voc, verseDocs)
	elif order == 4:
		return quadrigram.Quadrigram.train(voc, verseDocs)

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
