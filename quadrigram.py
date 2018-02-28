
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import random

class Quadrigram:

	BOS = 'BOS'
	EOS = 'EOS'
	vocabulary = set()
	illegalEndWords = set()
	documents = {}

	def cleanSentence(self, sentence):
		cleanSentences = []
		for i in range(1, len(sentence)-1):
			cleanSentences.append(sentence[i])
			if sentence[i] == '\n':
				if sentence[i-1] == sentence[i+1]:
					del cleanSentences[-2]
		return cleanSentences

	def getBOSfromEOS(self, eosWord):
		BOSes = [ context for context in self.pc.keys() if self.BOS in context ]
		EOSesInBOSes = [ bos for bos in BOSes if eosWord in bos ]
		if len(EOSesInBOSes) <= 0: return []
		key = EOSesInBOSes[ random.randint(0, len(EOSesInBOSes)-1) ]
		value = self.pc[key].keys()
		if len(value) > 1:
			value[ random.randint(0, len(value)-1) ]
		sentence = value
		sentence.append(self.randomByContext((key[1], key[2], sentence[-1])))
		sentence.append(self.randomByContext((key[2], sentence[-2], sentence[-1])))
		if self.EOS in sentence:
			sentence[-1] = '\n'
		return sentence

	def getRandomBOS(self):
		BOSes = [ context for context in self.pc.keys() if self.BOS in context ]
		return BOSes[ random.randint(0, len(BOSes)-1) ]

	def randomByContext(self, context):
		# TODO: check if can select word in better way that 'random'
		c = self.pc[context]
		possible = self.pc[context].keys()
		return possible[random.randint(0, len(possible)-1)]

	def randomSentenceBOS(self, sentence, bosContext=None):
		if bosContext == None:
			bosContext = self.getRandomBOS()
		sentence.append(bosContext[1])
		sentence.append(bosContext[2])
		predicted = self.randomByContext(bosContext)
		return sentence, predicted
	
	def illegalEnd(self, sentence):
		word = sentence[-2]
		del sentence[-2]	
		foundBOS = self.getBOSfromEOS(word)
		if len(foundBOS) > 0:
			print 'end word', word		
			sentence.append(word)
			sentence += foundBOS
		else:
			sentence, predicted = self.randomSentenceBOS(sentence)
			sentence.append(predicted)

		return sentence 

	def generate(self, length=7, rows=2):
		modLength = length + random.randint(0,length / 2)
		sentence = []
		lastBOSword = 0
		r = 0
		l = 0
		while r < rows :
			lastBOSword += 1
			if len(sentence) == 0 or sentence[-1] == self.EOS:
				sentence, predicted = self.randomSentenceBOS(sentence)
			elif sentence[-1] == '\n':
				if sentence[-2] in self.illegalEndWords:
					sentence = self.illegalEnd(sentence)				
					continue
				bosContext = self.getBOSfromEOS(sentence[-2])
				if len(bosContext) == 0:
					sentence, predicted = self.randomSentenceBOS(sentence)
				else:
					sentence += bosContext
					continue

			else:
				predicted = self.randomByContext((sentence[-3], sentence[-2], sentence[-1]))

			sentence.append(predicted)
			if lastBOSword >= length and sentence[-1] in self.eosWords:
				sentence.append('\n')
				lastBOSword = 0
				r += 1
				continue

			if l >= modLength and False:
				sentence.append('\n')				
				lastBOSword = 0			
				r += 1
			l +=1
		sentence = self.cleanSentence(sentence)
		return ' '.join(sentence)
	
	@classmethod
	def train(cls, vocabulary, documents, dontEnd):
		documents = documents[:]
		quadrigram = cls()
		quadrigram.eosWords = set()
		quadrigram.illegalEndWords = dontEnd
		quadrigram.vocabulary = vocabulary
		quadrigram.documents = documents

		# determine context / word probabilities
		contextOccurrenceCount = {}
		for doc in documents:
			doc.insert(0, cls.BOS)
			doc.append(cls.EOS)

			for i in range(2, len(doc)-1):
				context = (doc[i-2], doc[i-1], doc[i])
				word = doc[i+1]

				if context not in contextOccurrenceCount:
					contextOccurrenceCount[context] = {}

				if word not in contextOccurrenceCount[context]:
					contextOccurrenceCount[context][word] = 1
				else:
					contextOccurrenceCount[context][word] += 1		
		
		def sumContextOccurences(context):
			s = 0
			for occurences, count in context.iteritems():
				s += count
			return s

		quadrigram.pc = {}
		for context, occurences in contextOccurrenceCount.iteritems():
			quadrigram.pc[context] = {}

			total = sumContextOccurences(contextOccurrenceCount[context])
			for word, count in occurences.iteritems():
				quadrigram.pc[context][word] = float(count) / float(total)

		quadrigram.eosWords.update([ eos[-1] for eos in  quadrigram.pc.keys() if cls.EOS in quadrigram.pc[eos] ])
		print quadrigram.eosWords
		return quadrigram
