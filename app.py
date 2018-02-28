
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

import interface

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
	interface.run()

	# testRows= 5
	# order = None
	# while not isinstance(order, int):
	# 	order = raw_input('order: ')
	# 	try: order = int(order)
	# 	except: continue

	# # # bi test
	# # print '\nBigram'
	# # print '\n'.join([ bi.generate(length=10) for i in range(0, testRows) ])

	# # # tri test
	# # print '\nTrigram'
	# # print '\n'.join([ tri.generate(length=10) for i in range(0, testRows) ])

	# # # quad test
	# # print '\nQuadrigram'
	# # print '\n'.join([ quad.generate(length=10) for i in range(0, testRows) ])

	# model = modelTrain(order=order)
	# while True:
	# 	generated = '\n'.join([ model.generate(length=20) for i in range(0, testRows) ])
	# 	print generated
	# 	raw_input()

if __name__ == '__main__':
	main()
