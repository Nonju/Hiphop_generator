
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import codecs
import json
import random

from vocab import vocab
from models import bigram
from models import trigram
from models import quadrigram

DEFAULT_DOC_FILE = './genius_lyrics_search/output.json'
SONG_STRUCTURE_FILE = './textgeneration/songstructures.json'
DONT_END_ON_FILE = './interface/dontEndOn.json'

def getDocuments(docFile=DEFAULT_DOC_FILE):
	with codecs.open(docFile, 'r', encoding='utf8') as documents:
		return json.loads(documents.read())

def getIllegalEndWords(dontEndOnFile=DONT_END_ON_FILE):
	with codecs.open(DONT_END_ON_FILE, 'r', encoding='utf8') as l:
		return json.loads(l.read())

def getPart(docs, partName=''):
	parts = []
	for doc in docs:
		if partName == 'title':
			parts.append(doc[partName].split(' '))
		if partName not in doc['lyrics'].keys():
			continue

		for part in doc['lyrics'][partName]:
			parts.append(part)

	return parts

def trainModelOfOrder(vocabulary, documents, order=0):
	model = None
	if order == 2:
		model = bigram.Bigram.train(vocabulary=vocabulary, documents=documents)
	elif order == 3:
		model = trigram.Trigram.train(vocabulary=vocabulary, documents=documents)
	elif order == 4:
		dontEndOn = getIllegalEndWords()
		model = quadrigram.Quadrigram.train(vocabulary=vocabulary, documents=documents, invalidWords=dontEndOn)

	return model

def getRandomSongStructure(structureFile=SONG_STRUCTURE_FILE):
	with codecs.open(structureFile, 'r', encoding='utf8') as f:
		structures = json.loads(f.read())
		rand = random.randint(0, len(structures)-1)
		return structures[rand]

def generateLyrics(modelOrder):

	vocabulary = vocab.getVocab()
	documents = getDocuments()

	def formatParagraph(model, partName='', partRows=10):
		return u'\n\n<{}>\n{}\n\n'.format(partName, model.generate(length=7, rows=partRows))

	lyrics = u''
	for part in getRandomSongStructure():
		partName = part.get('name', '')
		partRows = part.get('rows', 10)
		partDocs = getPart(documents, partName=partName)
		if not len(partDocs): continue

		model = trainModelOfOrder(vocabulary=vocabulary, documents=partDocs, order=modelOrder)
		if model is None: continue

		lyrics += formatParagraph(model, partName=partName, partRows=partRows)


	return lyrics

def generateTitle(lyrics):

	vocabulary = vocab.getVocab()
	documents = getDocuments()

	def formatParagraph(model, partName='', partRows=10):
		return u'\n\n<{}>\n{}\n\n'.format(partName, model.generate(length=7, rows=partRows))
	partDocs = getPart(documents, partName='title')
	model = trainModelOfOrder(vocabulary=vocabulary, documents=partDocs, order=2)
	
	length = random.randint(4,6)
	title = model.generate(length, 1)


	return title