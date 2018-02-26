
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

	verseDocs = getPart(docs, partName=u'verse')
	return bigram.Bigram.train(voc, verseDocs)

def buildSentence(model, length=4):
	# TODO: rewrite to actually work

	sentence = ''
	word = 'BOS'
	while raw_input() == 'y':
		word = model.predict(word)
		sentence += u' {}'.format(word)
		print '>> ', sentence



def main():
	model = modelTrain()
	buildSentence(model)

if __name__ == '__main__':
	main()
