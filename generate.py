
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


def generateLyrics(modelOrder, rowLength=10):

	vocabulary = vocab.getVocab()
	documents = getDocuments()

	lyrics = {}
	def formatLyrics():
		formattedText = ''
		for lyricPart, lyric in lyrics.iteritems():
			formattedText += u'{}\n\n{}\n\n'.format(lyricPart, lyric)
		return formattedText


	lyrics = ''
	for partName in getRandomSongStructure():
		partDocs = getPart(documents, partName=partName)
		model = trainModelOfOrder(vocabulary=vocabulary, documents=partDocs, order=modelOrder)
		if model is None: continue
		# lyrics[partName] = model.generate(length=rowLength)
		lyrics += u'{}\n\n{}\n\n'.format(partName, model.generate(length=rowLength))

	# return formatLyrics()
	return lyrics

