#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Generates vocabulary from avaialbe lyricparts

Retrieves existing vocab
"""

import codecs
import json

DEFAULT_DATA_FILE  = './genius_lyrics_search/output.json'
VOCAB_FILE = './vocab/vocab.json'

def generateVocab():
	with codecs.open(DEFAULT_DATA_FILE, 'r', encoding='utf8') as dataFile:
		songData = json.loads(dataFile.read())

	# TODO: replace with yield ?? 
	vocab = set()
	for song in songData:
		for part in song['lyrics']:
			for line in song['lyrics'][part]:
				vocab.update(line.split())

	with codecs.open(VOCAB_FILE, 'w', encoding='utf8') as vocabFile:
		vocabFile.write(json.dumps(list(vocab), indent=2, sort_keys=True))


def getVocab():
	with codecs.open(VOCAB_FILE, 'r', encoding='utf8') as vocabFile:
		return json.loads(vocabFile.read())

def main():
	generate = raw_input('generate (yes/no): ')
	print 'Generates:', generate
	if generate in [ 'yes', 'y' ]:
		generateVocab()

if __name__ == '__main__':
	main()

