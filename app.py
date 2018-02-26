
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Entry point for Hip-hop generator app

Written using python2.7
"""

import vocab
# from .models import bigram
import codecs
import json

import bigram

def getDocuments():
	#Replace with function that uses search
	with codecs.open('genius-lyrics-search/exampleoutput.json', 'r', encoding='utf8') as documents:
		return json.loads(documents.read())

def getPart(docs, partName=''):
	parts = []
	for doc in docs:

		if partName not in doc['lyrics'].keys():
			continue

		for part in doc['lyrics'][partName]:
			parts.append(part)

	return parts

def modelTrain(): # Currently training of verses
	voc = vocab.getVocab()
	docs = getDocuments()

	verseDocs = getPart(docs, partName=u'verse')
	return bigram.Bigram.train(voc, verseDocs)

def main():
	model = modelTrain()
	print 'Sentence:', model.generate(length=20)

if __name__ == '__main__':
	main()
