
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
	#Replace with fumction that uses search
	with codecs.open('genius-lyrics-search/exampleoutput.json', 'r', encoding='utf8') as documents:
		return json.loads(documents.read())

def getPart(docs, partName=''):
	parts = []
	for doc in docs:
		# parts += [p for p in doc['lyrics'].get(part) if part in doc['lyrics']]

		if partName not in doc['lyrics'].keys():
			continue

		for part in doc['lyrics'][partName]:
			parts.append(part)

	return parts

def modelTrain():
	voc = vocab.getVocab()
	docs = getDocuments()

	introDocs = getPart(docs, partName=u'verse')
	bigram.Bigram.train(voc, introDocs)

def main():
	modelTrain()

if __name__ == '__main__':
	main()
