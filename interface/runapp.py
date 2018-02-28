
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import codecs
import json

from vocab import vocab
# models
from models import bigram
from models import trigram
from models import quadrigram

def getDocuments():
	#Replace with function that uses search
	with codecs.open('genius_lyrics_search/output.json', 'r', encoding='utf8') as documents:
		return json.loads(documents.read())

def getIllegalEndWords():
	with codecs.open('interface/dontEndOn.json', 'r', encoding='utf8') as l:
		return json.loads(l.read())

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
	dontEnd = getIllegalEndWords()

	verseDocs = getPart(docs, partName=u'verse')

	if order == 2:
		return bigram.Bigram.train(voc, verseDocs)
	elif order == 3:
		return trigram.Trigram.train(voc, verseDocs)
	elif order == 4:
		return quadrigram.Quadrigram.train(voc, verseDocs, dontEnd)

def run():
	print 'Running app...'

	order = None
	while not isinstance(order, int):
		order = raw_input('Use models of order (2, 3, 4): ')
		try:
			if int(order) not in [2, 3, 4]: continue
			order = int(order)
		except: continue

	model = modelTrain(order=order)
	print '\nGenerated:\ns', model.generate(length=7, rows=10)
