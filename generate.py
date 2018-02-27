
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import codecs
import json
import random
import vocab
from bigram import Bigram
from trigram import Trigram
from quadrigram import Quadrigram

DEFAULT_DOC_FILE = './genius-lyrics-search/exampleoutput.json'
SONG_STRUCTURE_FILE = './songstructures.json'

def getDocuments(docFile=DEFAULT_DOC_FILE):
	#Replace with function that uses search
	with codecs.open(docFile, 'r', encoding='utf8') as documents:
		return json.loads(documents.read())

def getPart(docs, partName=''):
	parts = []
	for doc in docs:

		if partName not in doc['lyrics'].keys():
			continue

		for part in doc['lyrics'][partName]:
			parts.append(part)

	return parts

def trainModelOfOrder(vocabulary, documents, order=0):
	model = None
	if order == 2:
		model = Bigram
	elif order == 3:
		model = Trigram
	elif order == 4:
		model = Quadrigram

	if model is not None:
		return model.train(vocabulary=vocabulary, documents=documents)
	return model

def getRandomSongStructure(structureFile=SONG_STRUCTURE_FILE):
	with codecs.open(structureFile, 'r', encoding='utf8') as f:
		structures = json.loads(f.read())
		rand = random.randint(0, len(structures)-1)
		return structures[rand]

def generateLyrics(modelOrder):

	vocabulary = vocab.getVocab()
	documents = getDocuments(docFile='./genius-lyrics-search/hundredPages.json')

	def randomRowLength(offset=0):
		return offset + random.randint(4, 6)

	def formatParagraph(model, partName=''):
		first  = model.generate(length=10).split()
		second = model.generate(length=10).split()

		formatted = []
		# formatted.append(first[:randomRowLength()])
		# formatted.append(second[5:randomRowLength(offset=5)])
		# formatted.append(first[10:randomRowLength(offset=10)])
		# formatted.append(second[14:randomRowLength(offset=14)])
		formatted.append(first[:5])
		formatted.append(first[5:])
		formatted.append(second[:5])
		formatted.append(second[5:])
		return u'{}\n\n{}\n\n'.format(partName, u'\n'.join([' '.join(f) for f in formatted]))

	lyrics = u''
	for partName in getRandomSongStructure():
		partDocs = getPart(documents, partName=partName)
		if not len(partDocs): continue

		model = trainModelOfOrder(vocabulary=vocabulary, documents=partDocs, order=modelOrder)
		if model is None: continue
		# lyrics += u'{}\n\n{}\n\n'.format(partName, model.generate(length))

		lyrics += formatParagraph(model, partName=partName)


	return lyrics

